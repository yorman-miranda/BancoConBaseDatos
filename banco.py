from database.config import get_session
from crud.cuenta_curd import CuentaCRUD
from crud.transaccion_crud import TransaccionCRUD
from sqlalchemy.exc import SQLAlchemyError
import uuid
from typing import Tuple


class Banco:
    """Clase con la lógica de negocio para las operaciones bancarias (Depósito, Retiro, Transferencia)."""

    @staticmethod
    def realizar_deposito(
        numero_cuenta: str, monto: float, id_usuario_operador: uuid.UUID
    ) -> Tuple[bool, str]:
        """Realiza un depósito en una cuenta, actualiza el saldo y registra la transacción."""
        if monto <= 0:
            return False, "El monto del depósito debe ser positivo."

        session = get_session()
        try:
            # 1. Obtener la cuenta y bloquear la fila (con_for_update)
            cuenta = CuentaCRUD.get_by_numero(
                numero_cuenta, session=session, for_update=True
            )
            if not cuenta:
                return False, f"Cuenta con número {numero_cuenta} no encontrada."

            if cuenta.estado != "ACTIVA":
                return (
                    False,
                    f"La cuenta está {cuenta.estado}. No se permiten depósitos.",
                )

            # 2. Actualizar Saldo (Llamada al método interno de CuentaCRUD)
            cuenta_actualizada = CuentaCRUD._update_balance(
                session=session,
                cuenta_id=cuenta.idCuenta,
                monto_cambio=monto,  # Monto positivo
                id_usuario_edicion=id_usuario_operador,
            )

            # 3. Registrar Transacción
            TransaccionCRUD.create_with_session(
                session=session,
                tipo="DEPOSITO",
                monto=monto,
                idCuenta=cuenta_actualizada.idCuenta,
                id_usuario_creacion=id_usuario_operador,
            )

            session.commit()
            return (
                True,
                f"Depósito de {monto:,.2f} realizado exitosamente en la cuenta {numero_cuenta}. Nuevo saldo: {cuenta_actualizada.saldo:,.2f}",
            )

        except ValueError as e:
            session.rollback()
            return False, str(e)
        except SQLAlchemyError as e:
            session.rollback()
            return False, f"Error de base de datos al depositar: {e}"
        finally:
            session.close()

    @staticmethod
    def realizar_retiro(
        numero_cuenta: str, monto: float, id_usuario_operador: uuid.UUID
    ) -> Tuple[bool, str]:
        """Realiza un retiro de una cuenta, actualiza el saldo y registra la transacción."""
        if monto <= 0:
            return False, "El monto del retiro debe ser positivo."

        session = get_session()
        try:
            # 1. Obtener y bloquear la cuenta
            cuenta = CuentaCRUD.get_by_numero(
                numero_cuenta, session=session, for_update=True
            )
            if not cuenta:
                return False, f"Cuenta con número {numero_cuenta} no encontrada."

            if cuenta.estado != "ACTIVA":
                return False, f"La cuenta está {cuenta.estado}. No se permiten retiros."

            # 2. Actualizar Saldo (monto negativo para restar, validación de saldo ocurre dentro de _update_balance)
            cuenta_actualizada = CuentaCRUD._update_balance(
                session=session,
                cuenta_id=cuenta.idCuenta,
                monto_cambio=-monto,  # Monto negativo
                id_usuario_edicion=id_usuario_operador,
            )

            # 3. Registrar Transacción
            TransaccionCRUD.create_with_session(
                session=session,
                tipo="RETIRO",
                monto=monto,
                idCuenta=cuenta_actualizada.idCuenta,
                id_usuario_creacion=id_usuario_operador,
            )

            session.commit()
            return (
                True,
                f"Retiro de {monto:,.2f} realizado exitosamente de la cuenta {numero_cuenta}. Nuevo saldo: {cuenta_actualizada.saldo:,.2f}",
            )

        except ValueError as e:
            session.rollback()
            return False, str(e)
        except SQLAlchemyError as e:
            session.rollback()
            return False, f"Error de base de datos al retirar: {e}"
        finally:
            session.close()

    @staticmethod
    def realizar_transferencia(
        cuenta_origen: str,
        cuenta_destino: str,
        monto: float,
        id_usuario_operador: uuid.UUID,
    ) -> Tuple[bool, str]:
        """Realiza una transferencia entre dos cuentas."""
        if monto <= 0:
            return False, "El monto de la transferencia debe ser positivo."
        if cuenta_origen == cuenta_destino:
            return False, "Las cuentas de origen y destino no pueden ser las mismas."

        session = get_session()
        try:
            # 1. Obtener y bloquear ambas cuentas para la transacción
            cuenta_o = CuentaCRUD.get_by_numero(
                cuenta_origen, session=session, for_update=True
            )
            cuenta_d = CuentaCRUD.get_by_numero(
                cuenta_destino, session=session, for_update=True
            )

            if not cuenta_o:
                return False, f"Cuenta de origen {cuenta_origen} no encontrada."
            if not cuenta_d:
                return False, f"Cuenta de destino {cuenta_destino} no encontrada."

            if cuenta_o.estado != "ACTIVA" or cuenta_d.estado != "ACTIVA":
                return (
                    False,
                    "Una de las cuentas no está activa para realizar la transferencia.",
                )

            # 2. Retiro de Origen (valida saldo)
            CuentaCRUD._update_balance(
                session=session,
                cuenta_id=cuenta_o.idCuenta,
                monto_cambio=-monto,
                id_usuario_edicion=id_usuario_operador,
            )

            # 3. Depósito en Destino
            cuenta_d_act = CuentaCRUD._update_balance(
                session=session,
                cuenta_id=cuenta_d.idCuenta,
                monto_cambio=monto,
                id_usuario_edicion=id_usuario_operador,
            )

            # 4. Registrar Transacciones (una para el débito, una para el crédito)
            TransaccionCRUD.create_with_session(
                session=session,
                tipo=f"TRANSFERENCIA DEBITO A {cuenta_destino}",
                monto=monto,
                idCuenta=cuenta_o.idCuenta,
                id_usuario_creacion=id_usuario_operador,
            )
            TransaccionCRUD.create_with_session(
                session=session,
                tipo=f"TRANSFERENCIA CREDITO DE {cuenta_origen}",
                monto=monto,
                idCuenta=cuenta_d_act.idCuenta,
                id_usuario_creacion=id_usuario_operador,
            )

            session.commit()
            return (
                True,
                f"Transferencia de {monto:,.2f} de {cuenta_origen} a {cuenta_destino} realizada con éxito. Nuevo Saldo Origen: {cuenta_o.saldo:,.2f}",
            )

        except ValueError as e:
            session.rollback()
            return False, str(e)
        except SQLAlchemyError as e:
            session.rollback()
            return False, f"Error de base de datos al transferir: {e}"
        finally:
            session.close()
