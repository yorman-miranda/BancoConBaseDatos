"""
Sistema Bancario - Menú Principal con Roles Claros
==================================================
"""

import sys
from datetime import datetime
import uuid
from typing import Type, List


from database.config import create_tables, check_connection, get_session
from auth.security import PasswordManager

from banco import Banco

from crud.cliente_crud import ClienteCRUD
from crud.cuenta_crud import CuentaCRUD
from crud.empleado_crud import EmpleadoCRUD
from crud.sucursal_crud import SucursalCRUD
from crud.transaccion_crud import TransaccionCRUD
from crud.user_crud import UserCRUD

from entities.user import User
from entities.cliente import Cliente
from entities.cuenta import Cuenta
from entities.empleado import Empleado
from entities.sucursal import Sucursal


ADMIN_USERNAME = "admin"
ADMIN_PASS = "admin_1234"


def crear_admin_inicial():
    """Crea el primer usuario administrador si no existe."""
    if UserCRUD.get_by_username(ADMIN_USERNAME):
        return

    try:
        admin_id = uuid.uuid4()
        hashed_password = PasswordManager.hash_password(ADMIN_PASS)

        session = get_session()
        try:
            user = User(
                idUser=admin_id,
                firstName="Super",
                lastName="Admin",
                username=ADMIN_USERNAME,
                password=hashed_password,
                id_usuario_creacion=admin_id,
                activo=True,
                es_admin=True,
                fecha_creacion=datetime.now(),
            )
            session.add(user)
            session.commit()
            print(f"✅ Administrador '{ADMIN_USERNAME}' creado exitosamente.")
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    except Exception as e:
        print(f"❌ Error al crear el administrador inicial: {e}")


class MenuSistemaBancario:
    def __init__(self):
        self.current_user = None
        self.current_user_id = None
        self.es_admin = False
        self.es_empleado = False
        self.es_cliente = False
        self.cliente_asociado = None
        self.empleado_asociado = None
        self.inicializar_sistema()

    def inicializar_sistema(self):
        """Inicializa la base de datos, verifica conexión y crea el admin."""
        print("\n=== Inicializando sistema bancario ===")
        if not check_connection():
            print("Error: No se pudo conectar a la base de datos")
            sys.exit(1)

        create_tables()
        crear_admin_inicial()
        print("Sistema inicializado correctamente.")
        self.menu_inicio()

    def determinar_rol_usuario(self, user):
        """Determina el rol del usuario (admin, empleado, cliente)"""
        try:

            self.es_admin = getattr(user, "es_admin", False)

            if self.es_admin:
                print("✅ Usuario identificado como Administrador")
                return

            session = get_session()
            try:
                empleado = (
                    session.query(Empleado).filter_by(idUsuario=user.idUser).first()
                )
                if empleado:
                    self.es_empleado = True
                    self.empleado_asociado = empleado
                    print("✅ Usuario identificado como Empleado")
            except Exception as e:
                print(f"Advertencia al buscar empleado: {e}")
            finally:
                session.close()

            session = get_session()
            try:
                cliente = (
                    session.query(Cliente).filter_by(idUsuario=user.idUser).first()
                )
                if cliente:
                    self.es_cliente = True
                    self.cliente_asociado = cliente
                    print("✅ Usuario identificado como Cliente")
            except Exception as e:
                print(f"Advertencia al buscar cliente: {e}")
            finally:
                session.close()

            if not any([self.es_admin, self.es_empleado, self.es_cliente]):
                print("⚠️  Usuario sin rol específico asignado")

        except Exception as e:
            print(f"Error al determinar roles: {e}")

    def menu_inicio(self):
        """Menú principal de inicio."""
        while True:
            print("\n=== SISTEMA BANCARIO ===")
            print("1. Ingresar")
            print("2. Registrarse como Cliente")
            print("3. Salir")

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.login()
                if self.current_user:
                    self.mostrar_menu_segun_rol()
            elif opcion == "2":
                self.registrarse_como_cliente()
            elif opcion == "3":
                print("¡Hasta pronto!")
                sys.exit(0)
            else:
                print("Opción no válida. Intente de nuevo.")

    def registrarse_como_cliente(self):
        """Registra un nuevo cliente (crea usuario + cliente)."""
        print("\n=== REGISTRO DE CLIENTE ===")
        try:

            first_name = input("Nombre: ").strip()
            last_name = input("Apellido: ").strip()
            documento = input("Documento: ").strip()
            telefono = input("Teléfono: ").strip()
            email = input("Email: ").strip()
            direccion = input("Dirección: ").strip()

            username = input("Nombre de usuario: ").strip()
            password = input("Contraseña: ").strip()

            if not all([first_name, last_name, documento, username, password]):
                print(
                    "❌ Campos obligatorios: nombre, apellido, documento, usuario, contraseña"
                )
                return

            if UserCRUD.get_by_username(username):
                print("❌ El nombre de usuario ya existe")
                return

            session = get_session()
            if session.query(Cliente).filter_by(documento=documento).first():
                print("❌ El documento ya está registrado")
                session.close()
                return
            session.close()

            admin_user = UserCRUD.get_by_username(ADMIN_USERNAME)
            if not admin_user:
                print("❌ Sistema no inicializado correctamente.")
                return

            user_data = {
                "firstName": first_name,
                "lastName": last_name,
                "username": username,
                "password": password,
                "id_usuario_creacion": admin_user.idUser,
                "activo": True,
                "es_admin": False,
            }

            nuevo_usuario = UserCRUD.create(**user_data)
            if not nuevo_usuario:
                print("❌ Error al crear usuario")
                return

            cliente_data = {
                "nombre": f"{first_name} {last_name}",
                "documento": documento,
                "telefono": telefono,
                "direccion": direccion,
                "email": email,
                "idUsuario": nuevo_usuario.idUser,
                "idSucursal": None,
                "id_usuario_creacion": admin_user.idUser,
            }

            cliente = ClienteCRUD.create(**cliente_data)
            if cliente:
                print("✅ Cliente registrado exitosamente. Ahora puede ingresar.")
            else:
                print("❌ Error al crear cliente")

        except Exception as e:
            print(f"❌ Error en el registro: {e}")

    def login(self):
        """Sistema de autenticación."""
        print("\n=== INICIO DE SESIÓN ===")
        username = input("Nombre de usuario: ").strip()
        password = input("Contraseña: ").strip()

        user = UserCRUD.authenticate(username, password)

        if user and user.activo:
            self.current_user = user
            self.current_user_id = user.idUser
            self.determinar_rol_usuario(user)

            print(f"\n¡Bienvenido, {user.firstName} {user.lastName}!")
            if self.es_admin:
                print("Rol: Administrador")
            elif self.es_empleado:
                print("Rol: Empleado")
            elif self.es_cliente:
                print("Rol: Cliente")
            else:
                print("Rol: Usuario Básico")
            return True
        else:
            print("❌ Credenciales inválidas o usuario inactivo.")
            return False

    def mostrar_menu_segun_rol(self):
        """Muestra el menú según el rol del usuario."""
        if self.es_admin:
            self.menu_administrador()
        elif self.es_empleado:
            self.menu_empleado()
        elif self.es_cliente:
            self.menu_cliente()
        else:
            print("❌ Usuario sin rol asignado. Contacte al administrador.")
            self.logout()

    def menu_administrador(self):
        """Menú para administradores."""
        while True:
            print(f"\n=== MENÚ ADMINISTRADOR ({self.current_user.username}) ===")
            print("1. Crear Empleado")
            print("2. Crear Sucursal")
            print("3. Ver Usuarios")
            print("4. Ver Reportes")
            print("9. Cerrar Sesión")
            print("0. Salir")

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.crear_empleado()
            elif opcion == "2":
                self.crear_sucursal()
            elif opcion == "3":
                self.ver_usuarios()
            elif opcion == "4":
                self.ver_reportes()
            elif opcion == "9":
                self.logout()
                break
            elif opcion == "0":
                print("¡Hasta pronto!")
                sys.exit(0)
            else:
                print("Opción no válida. Intente de nuevo.")

    def crear_empleado(self):
        """Crear un nuevo empleado (solo admin)."""
        print("\n--- CREAR EMPLEADO ---")
        try:

            first_name = input("Nombre: ").strip()
            last_name = input("Apellido: ").strip()
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            cargo = input("Cargo: ").strip()

            if UserCRUD.get_by_username(username):
                print("❌ El nombre de usuario ya existe")
                return

            user_data = {
                "firstName": first_name,
                "lastName": last_name,
                "username": username,
                "password": password,
                "id_usuario_creacion": self.current_user_id,
                "activo": True,
                "es_admin": False,
            }

            nuevo_usuario = UserCRUD.create(**user_data)
            if not nuevo_usuario:
                print("❌ Error al crear usuario")
                return

            print("\nSucursales disponibles:")
            sucursales = SucursalCRUD.get_all()
            if not sucursales:
                print("❌ No hay sucursales registradas. Primero cree una sucursal.")
                return

            for sucursal in sucursales:
                print(
                    f"ID: {sucursal.idSucursal} - {sucursal.nombreSucursal} ({sucursal.ciudad})"
                )

            sucursal_id = input("ID de la sucursal: ").strip()

            try:
                sucursal_uuid = uuid.UUID(sucursal_id)
            except ValueError:
                print("❌ ID de sucursal no válido")
                return

            empleado_data = {
                "nombre": first_name,
                "apellido": last_name,
                "cargo": cargo,
                "idSucursal": sucursal_uuid,
                "idUsuario": nuevo_usuario.idUser,
                "id_usuario_creacion": self.current_user_id,
            }

            empleado = EmpleadoCRUD.create(**empleado_data)
            if empleado:
                print("✅ Empleado creado exitosamente")
            else:
                print("❌ Error al crear empleado")

        except Exception as e:
            print(f"❌ Error al crear empleado: {e}")

    def crear_sucursal(self):
        """Crear una nueva sucursal (solo admin)."""
        print("\n--- CREAR SUCURSAL ---")
        try:
            nombre = input("Nombre de la sucursal: ").strip()
            ciudad = input("Ciudad: ").strip()
            direccion = input("Dirección: ").strip()
            telefono = input("Teléfono: ").strip()

            sucursal_data = {
                "nombreSucursal": nombre,
                "ciudad": ciudad,
                "direccion": direccion,
                "telefono": telefono,
                "id_usuario_creacion": self.current_user_id,
            }

            sucursal = SucursalCRUD.create(**sucursal_data)
            if sucursal:
                print("✅ Sucursal creada exitosamente")
            else:
                print("❌ Error al crear sucursal")

        except Exception as e:
            print(f"❌ Error al crear sucursal: {e}")

    def ver_usuarios(self):
        """Ver todos los usuarios del sistema."""
        print("\n--- USUARIOS DEL SISTEMA ---")
        try:
            usuarios = UserCRUD.get_all()
            if not usuarios:
                print("No hay usuarios registrados")
                return

            for usuario in usuarios:
                rol = "Administrador" if usuario.es_admin else "Empleado/Cliente"
                estado = "Activo" if usuario.activo else "Inactivo"
                print(
                    f"Usuario: {usuario.username} | {usuario.firstName} {usuario.lastName}"
                )
                print(f"   Rol: {rol} | Estado: {estado}")
                print("-" * 50)

        except Exception as e:
            print(f"❌ Error al listar usuarios: {e}")

    def ver_reportes(self):
        """Ver reportes básicos del sistema."""
        print("\n--- REPORTES DEL SISTEMA ---")
        try:
            session = get_session()

            total_usuarios = session.query(User).count()

            total_clientes = session.query(Cliente).count()

            total_empleados = session.query(Empleado).count()

            total_cuentas = session.query(Cuenta).count()

            total_sucursales = session.query(Sucursal).count()

            session.close()

            print(f"Total de usuarios: {total_usuarios}")
            print(f"Total de clientes: {total_clientes}")
            print(f"Total de empleados: {total_empleados}")
            print(f"Total de cuentas: {total_cuentas}")
            print(f"Total de sucursales: {total_sucursales}")

        except Exception as e:
            print(f"❌ Error al generar reportes: {e}")

    def menu_empleado(self):
        """Menú para empleados."""
        while True:
            print(f"\n=== MENÚ EMPLEADO ({self.current_user.username}) ===")
            print("1. Gestión de Clientes")
            print("2. Gestión de Cuentas")
            print("3. Operaciones Bancarias (Para clientes)")
            print("4. Consultar Información")
            print("9. Cerrar Sesión")
            print("0. Salir")

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.menu_gestion_clientes_empleado()
            elif opcion == "2":
                self.menu_gestion_cuentas_empleado()
            elif opcion == "3":
                self.menu_operaciones_bancarias_empleado()
            elif opcion == "4":
                self.menu_consultas_empleado()
            elif opcion == "9":
                self.logout()
                break
            elif opcion == "0":
                print("¡Hasta pronto!")
                sys.exit(0)
            else:
                print("Opción no válida. Intente de nuevo.")

    def menu_gestion_clientes_empleado(self):
        """Gestión de clientes para empleados."""
        while True:
            print("\n--- GESTIÓN DE CLIENTES (EMPLEADO) ---")
            print("1. Crear Cliente")
            print("2. Listar Clientes")
            print("3. Buscar Cliente por Documento")
            print("4. Asignar Cliente a Sucursal")
            print("5. Volver al Menú Anterior")

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.crear_cliente_empleado()
            elif opcion == "2":
                self.listar_clientes_empleado()
            elif opcion == "3":
                self.buscar_cliente_documento_empleado()
            elif opcion == "4":
                self.asignar_cliente_sucursal()
            elif opcion == "5":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def crear_cliente_empleado(self):
        """Empleado crea un nuevo cliente."""
        print("\n--- CREAR CLIENTE (EMPLEADO) ---")
        try:

            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            documento = input("Documento: ").strip()
            telefono = input("Teléfono: ").strip()
            email = input("Email: ").strip()
            direccion = input("Dirección: ").strip()

            if not all([nombre, apellido, documento]):
                print("❌ Nombre, apellido y documento son obligatorios")
                return

            session = get_session()
            if session.query(Cliente).filter_by(documento=documento).first():
                print("❌ El documento ya está registrado")
                session.close()
                return
            session.close()

            import random

            username = f"cli{documento[-4:]}{random.randint(100,999)}"
            password = "temp1234"

            user_data = {
                "firstName": nombre,
                "lastName": apellido,
                "username": username,
                "password": password,
                "id_usuario_creacion": self.current_user_id,
                "activo": True,
                "es_admin": False,
            }

            nuevo_usuario = UserCRUD.create(**user_data)
            if not nuevo_usuario:
                print("❌ Error al crear usuario para el cliente")
                return

            id_sucursal = (
                self.empleado_asociado.idSucursal if self.empleado_asociado else None
            )

            cliente_data = {
                "nombre": f"{nombre} {apellido}",
                "documento": documento,
                "telefono": telefono,
                "direccion": direccion,
                "email": email,
                "idUsuario": nuevo_usuario.idUser,
                "idSucursal": id_sucursal,
                "id_usuario_creacion": self.current_user_id,
            }

            cliente = ClienteCRUD.create(**cliente_data)
            if cliente:
                print("✅ Cliente creado exitosamente")
                print(f"   Usuario automático: {username}")
                print(f"   Contraseña temporal: {password}")
            else:
                print("❌ Error al crear cliente")

        except Exception as e:
            print(f"❌ Error al crear cliente: {e}")

    def listar_clientes_empleado(self):
        """Empleado lista todos los clientes."""
        print("\n--- LISTA DE CLIENTES ---")
        try:
            clientes = ClienteCRUD.get_all()
            if not clientes:
                print("No hay clientes registrados")
                return

            for cliente in clientes:
                print(f"Cliente: {cliente.nombre} | Doc: {cliente.documento}")
                print(f"   Tel: {cliente.telefono} | Email: {cliente.email}")
                print(f"   Dirección: {cliente.direccion}")
                print("-" * 50)

        except Exception as e:
            print(f"❌ Error al listar clientes: {e}")

    def buscar_cliente_documento_empleado(self):
        """Empleado busca cliente por documento."""
        print("\n--- BUSCAR CLIENTE ---")
        documento = input("Ingrese el documento del cliente: ").strip()

        try:
            session = get_session()
            cliente = session.query(Cliente).filter_by(documento=documento).first()
            if cliente:
                print(f"✅ Cliente encontrado:")
                print(f"   Nombre: {cliente.nombre}")
                print(f"   Documento: {cliente.documento}")
                print(f"   Teléfono: {cliente.telefono}")
                print(f"   Email: {cliente.email}")

                cuentas = (
                    session.query(Cuenta).filter_by(idCliente=cliente.idCliente).all()
                )
                if cuentas:
                    print("   Cuentas:")
                    for cuenta in cuentas:
                        print(
                            f"     - {cuenta.numeroCuenta} ({cuenta.tipoCuenta}): {cuenta.saldo:,.2f}"
                        )
            else:
                print("❌ Cliente no encontrado")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            session.close()

    def asignar_cliente_sucursal(self):
        """Asignar cliente a una sucursal."""
        print("\n--- ASIGNAR CLIENTE A SUCURSAL ---")
        try:
            documento = input("Documento del cliente: ").strip()

            session = get_session()
            cliente = session.query(Cliente).filter_by(documento=documento).first()
            if not cliente:
                print("❌ Cliente no encontrado")
                session.close()
                return

            sucursales = session.query(Sucursal).all()
            if not sucursales:
                print("❌ No hay sucursales registradas")
                session.close()
                return

            print("\nSucursales disponibles:")
            for sucursal in sucursales:
                print(f"ID: {sucursal.idSucursal} - {sucursal.nombreSucursal}")

            sucursal_id = input("ID de la sucursal: ").strip()
            try:
                sucursal_uuid = uuid.UUID(sucursal_id)
            except ValueError:
                print("❌ ID de sucursal no válido")
                session.close()
                return

            cliente.idSucursal = sucursal_uuid
            cliente.id_usuario_edicion = self.current_user_id
            session.commit()
            print("✅ Cliente asignado a sucursal exitosamente")

        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            session.close()

    def menu_gestion_cuentas_empleado(self):
        """Gestión de cuentas para empleados."""
        while True:
            print("\n--- GESTIÓN DE CUENTAS (EMPLEADO) ---")
            print("1. Crear Cuenta para Cliente")
            print("2. Listar Todas las Cuentas")
            print("3. Consultar Cuenta por Número")
            print("4. Actualizar Estado de Cuenta")
            print("5. Volver al Menú Anterior")

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.crear_cuenta_empleado()
            elif opcion == "2":
                self.listar_cuentas_empleado()
            elif opcion == "3":
                self.consultar_cuenta_empleado()
            elif opcion == "4":
                self.actualizar_estado_cuenta()
            elif opcion == "5":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def crear_cuenta_empleado(self):
        """Empleado crea cuenta para un cliente."""
        print("\n--- CREAR CUENTA PARA CLIENTE ---")
        try:
            documento_cliente = input("Documento del cliente: ").strip()

            session = get_session()
            cliente = (
                session.query(Cliente).filter_by(documento=documento_cliente).first()
            )
            if not cliente:
                print("❌ Cliente no encontrado")
                session.close()
                return
            session.close()

            print("Tipos de cuenta disponibles:")
            print("1. Ahorro")
            print("2. Corriente")
            print("3. Crédito")

            tipo_opcion = input("Seleccione el tipo de cuenta (1-3): ").strip()
            tipos = {"1": "AHORRO", "2": "CORRIENTE", "3": "CREDITO"}

            if tipo_opcion not in tipos:
                print("❌ Tipo de cuenta no válido")
                return

            tipo_cuenta = tipos[tipo_opcion]
            saldo_inicial = float(input("Saldo inicial: ") or 0)

            import random

            numero_cuenta = f"CTE{random.randint(100000, 999999)}"

            cuenta_data = {
                "numeroCuenta": numero_cuenta,
                "saldo": saldo_inicial,
                "estado": "ACTIVA",
                "tipoCuenta": tipo_cuenta,
                "idCliente": cliente.idCliente,
                "id_usuario_creacion": self.current_user_id,
            }

            cuenta = CuentaCRUD.create(**cuenta_data)
            if cuenta:
                print(
                    f"✅ Cuenta {tipo_cuenta} creada correctamente para {cliente.nombre}"
                )
                print(f"   Número de cuenta: {numero_cuenta}")
            else:
                print("❌ Error al crear cuenta")

        except ValueError:
            print("❌ Error: El saldo debe ser un número válido")
        except Exception as e:
            print(f"❌ Error: {e}")

    def listar_cuentas_empleado(self):
        """Empleado lista todas las cuentas."""
        print("\n--- LISTA DE CUENTAS ---")
        try:
            cuentas = CuentaCRUD.get_all()
            if not cuentas:
                print("No hay cuentas registradas")
                return

            for cuenta in cuentas:

                session = get_session()
                cliente = (
                    session.query(Cliente).filter_by(idCliente=cuenta.idCliente).first()
                )
                cliente_nombre = cliente.nombre if cliente else "Cliente no encontrado"
                session.close()

                print(f"Cuenta: {cuenta.numeroCuenta} | Cliente: {cliente_nombre}")
                print(
                    f"   Saldo: {cuenta.saldo:,.2f} | Tipo: {cuenta.tipoCuenta} | Estado: {cuenta.estado}"
                )
                print("-" * 50)

        except Exception as e:
            print(f"❌ Error al listar cuentas: {e}")

    def consultar_cuenta_empleado(self):
        """Empleado consulta cuenta por número."""
        print("\n--- CONSULTAR CUENTA ---")
        numero_cuenta = input("Número de cuenta: ").strip()

        try:
            cuenta = CuentaCRUD.get_by_numero(numero_cuenta)
            if cuenta:

                session = get_session()
                cliente = (
                    session.query(Cliente).filter_by(idCliente=cuenta.idCliente).first()
                )
                session.close()

                print(f"✅ Información de la cuenta:")
                print(f"   Número: {cuenta.numeroCuenta}")
                print(f"   Saldo: {cuenta.saldo:,.2f}")
                print(f"   Tipo: {cuenta.tipoCuenta}")
                print(f"   Estado: {cuenta.estado}")
                if cliente:
                    print(f"   Cliente: {cliente.nombre} ({cliente.documento})")

                transacciones = TransaccionCRUD.get_by_cuenta(cuenta.idCuenta)
                if transacciones:
                    print("   Últimas transacciones:")
                    for trans in transacciones[:5]:
                        print(f"     {trans.fecha} | {trans.tipo} | {trans.monto:,.2f}")
            else:
                print("❌ Cuenta no encontrada")
        except Exception as e:
            print(f"❌ Error: {e}")

    def actualizar_estado_cuenta(self):
        """Actualizar estado de una cuenta."""
        print("\n--- ACTUALIZAR ESTADO DE CUENTA ---")
        try:
            numero_cuenta = input("Número de cuenta: ").strip()

            cuenta = CuentaCRUD.get_by_numero(numero_cuenta)
            if not cuenta:
                print("❌ Cuenta no encontrada")
                return

            print(f"Estado actual: {cuenta.estado}")
            print("Estados disponibles: ACTIVA, BLOQUEADA, SUSPENDIDA")
            nuevo_estado = input("Nuevo estado: ").strip().upper()

            if nuevo_estado not in ["ACTIVA", "BLOQUEADA", "SUSPENDIDA"]:
                print("❌ Estado no válido")
                return

            session = get_session()
            cuenta_db = (
                session.query(Cuenta).filter_by(numeroCuenta=numero_cuenta).first()
            )
            if cuenta_db:
                cuenta_db.estado = nuevo_estado
                cuenta_db.id_usuario_edicion = self.current_user_id
                session.commit()
                print("✅ Estado de cuenta actualizado exitosamente")
            session.close()

        except Exception as e:
            print(f"❌ Error: {e}")

    def menu_operaciones_bancarias_empleado(self):
        """Operaciones bancarias que los empleados pueden realizar para clientes."""
        while True:
            print("\n--- OPERACIONES BANCARIAS (EMPLEADO) ---")
            print("1. Realizar Depósito para Cliente")
            print("2. Realizar Retiro para Cliente")
            print("3. Realizar Transferencia entre Cuentas")
            print("4. Ver Historial de Transacciones")
            print("5. Volver al Menú Anterior")

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.realizar_deposito_empleado()
            elif opcion == "2":
                self.realizar_retiro_empleado()
            elif opcion == "3":
                self.realizar_transferencia_empleado()
            elif opcion == "4":
                self.ver_historial_transacciones_empleado()
            elif opcion == "5":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def realizar_deposito_empleado(self):
        """Empleado realiza depósito para un cliente."""
        print("\n--- REALIZAR DEPÓSITO (EMPLEADO) ---")
        try:
            numero_cuenta = input("Número de cuenta: ").strip()
            monto = float(input("Monto a depositar: "))

            exito, mensaje = Banco.realizar_deposito(
                numero_cuenta, monto, self.current_user_id
            )
            print("✅ ÉXITO:" if exito else "❌ ERROR:")
            print(mensaje)

        except ValueError:
            print("❌ Error: El monto debe ser un número válido")
        except Exception as e:
            print(f"❌ Error: {e}")

    def realizar_retiro_empleado(self):
        """Empleado realiza retiro para un cliente."""
        print("\n--- REALIZAR RETIRO (EMPLEADO) ---")
        try:
            numero_cuenta = input("Número de cuenta: ").strip()
            monto = float(input("Monto a retirar: "))

            exito, mensaje = Banco.realizar_retiro(
                numero_cuenta, monto, self.current_user_id
            )
            print("✅ ÉXITO:" if exito else "❌ ERROR:")
            print(mensaje)

        except ValueError:
            print("❌ Error: El monto debe ser un número válido")
        except Exception as e:
            print(f"❌ Error: {e}")

    def realizar_transferencia_empleado(self):
        """Empleado realiza transferencia entre cuentas."""
        print("\n--- REALIZAR TRANSFERENCIA (EMPLEADO) ---")
        try:
            cuenta_origen = input("Cuenta origen: ").strip()
            cuenta_destino = input("Cuenta destino: ").strip()
            monto = float(input("Monto a transferir: "))

            exito, mensaje = Banco.realizar_transferencia(
                cuenta_origen, cuenta_destino, monto, self.current_user_id
            )
            print("✅ ÉXITO:" if exito else "❌ ERROR:")
            print(mensaje)

        except ValueError:
            print("❌ Error: El monto debe ser un número válido")
        except Exception as e:
            print(f"❌ Error: {e}")

    def ver_historial_transacciones_empleado(self):
        """Empleado ve historial de transacciones de una cuenta."""
        print("\n--- HISTORIAL DE TRANSACCIONES ---")
        numero_cuenta = input("Número de cuenta: ").strip()

        try:
            cuenta = CuentaCRUD.get_by_numero(numero_cuenta)
            if not cuenta:
                print("❌ Cuenta no encontrada")
                return

            transacciones = TransaccionCRUD.get_by_cuenta(cuenta.idCuenta)
            if not transacciones:
                print("ℹ️  No hay transacciones para esta cuenta")
                return

            session = get_session()
            cliente = (
                session.query(Cliente).filter_by(idCliente=cuenta.idCliente).first()
            )
            session.close()

            print(f"\nHistorial de la cuenta {numero_cuenta}")
            if cliente:
                print(f"Cliente: {cliente.nombre} ({cliente.documento})")

            for trans in transacciones:
                print(f"{trans.fecha} | {trans.tipo} | {trans.monto:,.2f}")

        except Exception as e:
            print(f"❌ Error: {e}")

    def menu_consultas_empleado(self):
        """Consultas de información para empleados."""
        while True:
            print("\n--- CONSULTAS E INFORMACIÓN (EMPLEADO) ---")
            print("1. Ver Información de Mi Sucursal")
            print("2. Ver Clientes de Mi Sucursal")
            print("3. Ver Cuentas de Mi Sucursal")
            print("4. Volver al Menú Anterior")

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.ver_info_sucursal()
            elif opcion == "2":
                self.ver_clientes_sucursal()
            elif opcion == "3":
                self.ver_cuentas_sucursal()
            elif opcion == "4":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def ver_info_sucursal(self):
        """Ver información de la sucursal del empleado."""
        if not self.empleado_asociado or not self.empleado_asociado.idSucursal:
            print("❌ No está asignado a ninguna sucursal")
            return

        try:
            session = get_session()
            sucursal = (
                session.query(Sucursal)
                .filter_by(idSucursal=self.empleado_asociado.idSucursal)
                .first()
            )
            if sucursal:
                print(f"\n--- INFORMACIÓN DE SUCURSAL ---")
                print(f"Nombre: {sucursal.nombreSucursal}")
                print(f"Ciudad: {sucursal.ciudad}")
                print(f"Dirección: {sucursal.direccion}")
                print(f"Teléfono: {sucursal.telefono}")

                empleados_count = (
                    session.query(Empleado)
                    .filter_by(idSucursal=sucursal.idSucursal)
                    .count()
                )
                print(f"Total de empleados: {empleados_count}")

                clientes_count = (
                    session.query(Cliente)
                    .filter_by(idSucursal=sucursal.idSucursal)
                    .count()
                )
                print(f"Total de clientes: {clientes_count}")
            else:
                print("❌ Sucursal no encontrada")
            session.close()
        except Exception as e:
            print(f"❌ Error: {e}")

    def ver_clientes_sucursal(self):
        """Ver clientes de la sucursal del empleado."""
        if not self.empleado_asociado or not self.empleado_asociado.idSucursal:
            print("❌ No está asignado a ninguna sucursal")
            return

        try:
            session = get_session()
            clientes = (
                session.query(Cliente)
                .filter_by(idSucursal=self.empleado_asociado.idSucursal)
                .all()
            )

            if not clientes:
                print("No hay clientes asignados a esta sucursal")
                session.close()
                return

            print(f"\n--- CLIENTES DE LA SUCURSAL ---")
            for cliente in clientes:
                print(f"Cliente: {cliente.nombre} | Doc: {cliente.documento}")
                print(f"   Tel: {cliente.telefono} | Email: {cliente.email}")

                cuentas_count = (
                    session.query(Cuenta).filter_by(idCliente=cliente.idCliente).count()
                )
                print(f"   Cuentas: {cuentas_count}")
                print("-" * 50)

            session.close()
        except Exception as e:
            print(f"❌ Error: {e}")

    def ver_cuentas_sucursal(self):
        """Ver cuentas de la sucursal del empleado."""
        if not self.empleado_asociado or not self.empleado_asociado.idSucursal:
            print("❌ No está asignado a ninguna sucursal")
            return

        try:
            session = get_session()

            clientes = (
                session.query(Cliente)
                .filter_by(idSucursal=self.empleado_asociado.idSucursal)
                .all()
            )

            if not clientes:
                print("No hay clientes en esta sucursal")
                session.close()
                return

            print(f"\n--- CUENTAS DE LA SUCURSAL ---")
            total_saldo = 0
            for cliente in clientes:
                cuentas = (
                    session.query(Cuenta).filter_by(idCliente=cliente.idCliente).all()
                )
                for cuenta in cuentas:
                    total_saldo += cuenta.saldo
                    print(f"Cliente: {cliente.nombre} | Cuenta: {cuenta.numeroCuenta}")
                    print(
                        f"   Tipo: {cuenta.tipoCuenta} | Saldo: {cuenta.saldo:,.2f} | Estado: {cuenta.estado}"
                    )
                    print("-" * 50)

            print(f"Saldo total de la sucursal: {total_saldo:,.2f}")
            session.close()
        except Exception as e:
            print(f"❌ Error: {e}")

    def menu_cliente(self):
        """Menú para clientes."""
        while True:
            print(f"\n=== MENÚ CLIENTE ({self.current_user.username}) ===")
            print("1. Mis Cuentas")
            print("2. Operaciones Bancarias")
            print("3. Ver Movimientos")
            print("4. Mi Información")
            print("9. Cerrar Sesión")
            print("0. Salir")

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.menu_mis_cuentas()
            elif opcion == "2":
                self.menu_operaciones_cliente()
            elif opcion == "3":
                self.ver_mis_movimientos()
            elif opcion == "4":
                self.ver_mi_informacion()
            elif opcion == "9":
                self.logout()
                break
            elif opcion == "0":
                print("¡Hasta pronto!")
                sys.exit(0)
            else:
                print("Opción no válida. Intente de nuevo.")

    def menu_mis_cuentas(self):
        """Menú de cuentas del cliente."""
        while True:
            print("\n--- MIS CUENTAS ---")
            print("1. Crear Nueva Cuenta")
            print("2. Ver Mis Cuentas")
            print("3. Consultar Saldo")
            print("4. Volver al Menú Principal")

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.crear_cuenta_cliente()
            elif opcion == "2":
                self.ver_mis_cuentas()
            elif opcion == "3":
                self.consultar_saldo_cliente()
            elif opcion == "4":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def crear_cuenta_cliente(self):
        """Un cliente crea una nueva cuenta para sí mismo."""
        print("\n--- CREAR NUEVA CUENTA ---")
        try:
            print("Tipos de cuenta disponibles:")
            print("1. Ahorro")
            print("2. Corriente")
            print("3. Crédito")

            tipo_opcion = input("Seleccione el tipo de cuenta (1-3): ").strip()
            tipos = {"1": "AHORRO", "2": "CORRIENTE", "3": "CREDITO"}

            if tipo_opcion not in tipos:
                print("❌ Tipo de cuenta no válido")
                return

            tipo_cuenta = tipos[tipo_opcion]
            saldo_inicial = float(input("Saldo inicial: ") or 0)

            import random

            numero_cuenta = f"CTE{random.randint(100000, 999999)}"

            cuenta_data = {
                "numeroCuenta": numero_cuenta,
                "saldo": saldo_inicial,
                "estado": "ACTIVA",
                "tipoCuenta": tipo_cuenta,
                "idCliente": self.cliente_asociado.idCliente,
                "id_usuario_creacion": self.current_user_id,
            }

            cuenta = CuentaCRUD.create(**cuenta_data)
            if cuenta:
                print(f"✅ Cuenta {tipo_cuenta} creada correctamente")
                print(f"   Número de cuenta: {numero_cuenta}")
            else:
                print("❌ Error al crear cuenta")

        except ValueError:
            print("❌ Error: El saldo debe ser un número válido")
        except Exception as e:
            print(f"❌ Error: {e}")

    def ver_mis_cuentas(self):
        """El cliente ve sus propias cuentas."""
        print("\n--- MIS CUENTAS ---")
        try:
            session = get_session()
            cuentas = (
                session.query(Cuenta)
                .filter_by(idCliente=self.cliente_asociado.idCliente)
                .all()
            )

            if not cuentas:
                print("No tiene cuentas registradas")
                return

            for cuenta in cuentas:
                print(f"Cuenta: {cuenta.numeroCuenta} | Saldo: {cuenta.saldo:,.2f}")
                print(f"   Tipo: {cuenta.tipoCuenta} | Estado: {cuenta.estado}")
                print("-" * 50)

        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            session.close()

    def consultar_saldo_cliente(self):
        """Cliente consulta saldo de una cuenta específica."""
        print("\n--- CONSULTAR SALDO ---")
        try:
            self.ver_mis_cuentas()
            numero_cuenta = input("Número de cuenta: ").strip()

            # Verificar que la cuenta pertenece al cliente
            session = get_session()
            cuenta = (
                session.query(Cuenta)
                .filter_by(
                    numeroCuenta=numero_cuenta,
                    idCliente=self.cliente_asociado.idCliente,
                )
                .first()
            )
            session.close()

            if not cuenta:
                print("❌ Cuenta no encontrada o no pertenece a usted")
                return

            print(f"💰 Saldo de la cuenta {numero_cuenta}: {cuenta.saldo:,.2f}")

        except Exception as e:
            print(f"❌ Error: {e}")

    def menu_operaciones_cliente(self):
        """Menú de operaciones para clientes."""
        while True:
            print("\n--- OPERACIONES BANCARIAS ---")
            print("1. Realizar Depósito")
            print("2. Realizar Retiro")
            print("3. Realizar Transferencia")
            print("4. Volver al Menú Principal")

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.realizar_deposito_cliente()
            elif opcion == "2":
                self.realizar_retiro_cliente()
            elif opcion == "3":
                self.realizar_transferencia_cliente()
            elif opcion == "4":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def realizar_deposito_cliente(self):
        """Un cliente realiza depósito en su propia cuenta."""
        print("\n--- REALIZAR DEPÓSITO ---")
        try:
            self.ver_mis_cuentas()
            numero_cuenta = input("Número de cuenta: ").strip()
            monto = float(input("Monto a depositar: "))

            session = get_session()
            cuenta = (
                session.query(Cuenta)
                .filter_by(
                    numeroCuenta=numero_cuenta,
                    idCliente=self.cliente_asociado.idCliente,
                )
                .first()
            )
            session.close()

            if not cuenta:
                print("❌ Cuenta no encontrada o no pertenece a usted")
                return

            exito, mensaje = Banco.realizar_deposito(
                numero_cuenta, monto, self.current_user_id
            )
            print("✅ ÉXITO:" if exito else "❌ ERROR:")
            print(mensaje)

        except ValueError:
            print("❌ Error: El monto debe ser un número válido")
        except Exception as e:
            print(f"❌ Error: {e}")

    def realizar_retiro_cliente(self):
        """Un cliente realiza retiro de su propia cuenta."""
        print("\n--- REALIZAR RETIRO ---")
        try:
            self.ver_mis_cuentas()
            numero_cuenta = input("Número de cuenta: ").strip()
            monto = float(input("Monto a retirar: "))

            session = get_session()
            cuenta = (
                session.query(Cuenta)
                .filter_by(
                    numeroCuenta=numero_cuenta,
                    idCliente=self.cliente_asociado.idCliente,
                )
                .first()
            )
            session.close()

            if not cuenta:
                print("❌ Cuenta no encontrada o no pertenece a usted")
                return

            exito, mensaje = Banco.realizar_retiro(
                numero_cuenta, monto, self.current_user_id
            )
            print("✅ ÉXITO:" if exito else "❌ ERROR:")
            print(mensaje)

        except ValueError:
            print("❌ Error: El monto debe ser un número válido")
        except Exception as e:
            print(f"❌ Error: {e}")

    def realizar_transferencia_cliente(self):
        """Un cliente realiza transferencia desde su cuenta."""
        print("\n--- REALIZAR TRANSFERENCIA ---")
        try:
            self.ver_mis_cuentas()
            cuenta_origen = input("Cuenta origen (su cuenta): ").strip()

            session = get_session()
            cuenta_o = (
                session.query(Cuenta)
                .filter_by(
                    numeroCuenta=cuenta_origen,
                    idCliente=self.cliente_asociado.idCliente,
                )
                .first()
            )
            session.close()

            if not cuenta_o:
                print("❌ Cuenta origen no encontrada o no pertenece a usted")
                return

            cuenta_destino = input("Cuenta destino: ").strip()
            monto = float(input("Monto a transferir: "))

            exito, mensaje = Banco.realizar_transferencia(
                cuenta_origen, cuenta_destino, monto, self.current_user_id
            )
            print("✅ ÉXITO:" if exito else "❌ ERROR:")
            print(mensaje)

        except ValueError:
            print("❌ Error: El monto debe ser un número válido")
        except Exception as e:
            print(f"❌ Error: {e}")

    def ver_mis_movimientos(self):
        """El cliente ve los movimientos de sus cuentas."""
        print("\n--- MIS MOVIMIENTOS ---")
        try:
            session = get_session()
            cuentas = (
                session.query(Cuenta)
                .filter_by(idCliente=self.cliente_asociado.idCliente)
                .all()
            )

            for cuenta in cuentas:
                print(f"\nCuenta: {cuenta.numeroCuenta} ({cuenta.tipoCuenta})")
                transacciones = TransaccionCRUD.get_by_cuenta(cuenta.idCuenta)

                if not transacciones:
                    print("   No hay movimientos")
                    continue

                for trans in transacciones:
                    print(f"   {trans.fecha} | {trans.tipo} | {trans.monto:,.2f}")

        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            session.close()

    def ver_mi_informacion(self):
        """El cliente ve su información personal."""
        print("\n--- MI INFORMACIÓN ---")
        try:
            cliente = self.cliente_asociado
            print(f"Nombre: {cliente.nombre}")
            print(f"Documento: {cliente.documento}")
            print(f"Teléfono: {cliente.telefono}")
            print(f"Email: {cliente.email}")
            print(f"Dirección: {cliente.direccion}")

        except Exception as e:
            print(f"❌ Error: {e}")

    def logout(self):
        """Cierra la sesión actual."""
        self.current_user = None
        self.current_user_id = None
        self.es_admin = False
        self.es_empleado = False
        self.es_cliente = False
        self.cliente_asociado = None
        self.empleado_asociado = None
        print("\nSesión cerrada. Vuelva pronto.")


def main():
    """Función principal que inicia el sistema"""
    try:
        menu = MenuSistemaBancario()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
    except Exception as e:
        print(f"Error inesperado: {e}")


if __name__ == "__main__":
    main()
