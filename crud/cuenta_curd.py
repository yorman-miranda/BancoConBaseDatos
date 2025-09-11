

from ..entities.cuenta import Cuenta
from ..database.database import get_session_context

class CuentaCRUD:
    """
    CRUD para la entidad Cuenta.
    Permite crear, leer, actualizar y eliminar cuentas bancarias.
    """

    @staticmethod
    def create(numeroCuenta, saldo, estado, tipoCuenta, idCliente):
        """
        Crea una nueva cuenta bancaria en la base de datos.
        """
        with get_session_context() as session:
            cuenta = Cuenta(
                numeroCuenta=numeroCuenta,
                saldo=saldo,
                estado=estado,
                tipoCuenta=tipoCuenta,
                idCliente=idCliente
            )
            session.add(cuenta)
            session.flush()
            session.refresh(cuenta)
            return cuenta

    @staticmethod
    def get_by_id(cuenta_id):
        """
        Obtiene una cuenta bancaria por su ID.
        """
        with get_session_context() as session:
            return session.query(Cuenta).filter_by(idCuenta=cuenta_id).first()

    @staticmethod
    def get_all():
        """
        Obtiene todas las cuentas bancarias registradas.
        """
        with get_session_context() as session:
            return session.query(Cuenta).all()

    @staticmethod
    def update(cuenta_id, **kwargs):
        """
        Actualiza los datos de una cuenta bancaria.
        """
        with get_session_context() as session:
            cuenta = session.query(Cuenta).filter_by(idCuenta=cuenta_id).first()
            if not cuenta:
                return None
            for key, value in kwargs.items():
                if hasattr(cuenta, key):
                    setattr(cuenta, key, value)
            session.flush()
            session.refresh(cuenta)
            return cuenta

    @staticmethod
    def delete(cuenta_id):
        """
        Elimina una cuenta bancaria de la base de datos.
        """
        with get_session_context() as session:
            cuenta = session.query(Cuenta).filter_by(idCuenta=cuenta_id).first()
            if not cuenta:
                return False
            session.delete(cuenta)
            return True
