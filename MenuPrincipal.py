
"""
Sistema Bancario - Menú Principal
=================================
Este módulo proporciona una interfaz de línea de comandos
para gestionar todas las entidades del sistema bancario.
"""

import sys
from datetime import datetime
from crud.cliente_crud import ClienteCRUD
from crud.cuenta_curd import CuentaCRUD
from crud.empleado_crud import EmpleadoCRUD
from crud.sucursal_crud import SucursalCRUD
from crud.transaccion_crud import TransaccionCRUD
from crud.user_crud import UserCRUD
from database.config import create_tables, check_connection 
# from entities import *


class MenuSistemaBancario:
    def __init__(self):
        self.inicializar_sistema()
        
    def inicializar_sistema(self):
        """Inicializa la base de datos y verifica la conexión"""
        print("Inicializando sistema bancario...")
        if not check_connection():
            print("Error: No se pudo conectar a la base de datos")
            sys.exit(1)
        
        # Crear tablas si no existen
        create_tables()
        print("Sistema inicializado correctamente\n")
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal del sistema"""
        while True:
            print("\n=== SISTEMA BANCARIO ===")
            print("1. Gestión de Clientes")
            print("2. Gestión de Cuentas")
            print("3. Gestión de Empleados")
            print("4. Gestión de Sucursales")
            print("5. Gestión de Transacciones")
            print("6. Gestión de Usuarios")
            print("7. Salir")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self.menu_clientes()
            elif opcion == "2":
                self.menu_cuentas()
            elif opcion == "3":
                self.menu_empleados()
            elif opcion == "4":
                self.menu_sucursales()
            elif opcion == "5":
                self.menu_transacciones()
            elif opcion == "6":
                self.menu_usuarios()
            elif opcion == "7":
                print("¡Hasta pronto!")
                break
            else:
                print("Opción no válida. Intente nuevamente.")
    
    def menu_clientes(self):
        """Menú para gestión de clientes"""
        while True:
            print("\n--- GESTIÓN DE CLIENTES ---")
            print("1. Crear cliente")
            print("2. Listar todos los clientes")
            print("3. Buscar cliente por ID")
            print("4. Actualizar cliente")
            print("5. Eliminar cliente")
            print("6. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self.crear_cliente()
            elif opcion == "2":
                self.listar_clientes()
            elif opcion == "3":
                self.buscar_cliente()
            elif opcion == "4":
                self.actualizar_cliente()
            elif opcion == "5":
                self.eliminar_cliente()
            elif opcion == "6":
                break
            else:
                print("Opción no válida.")
    
    def crear_cliente(self):
        """Crea un nuevo cliente"""
        print("\n--- CREAR NUEVO CLIENTE ---")
        nombre = input("Nombre: ")
        documento = input("Documento: ")
        telefono = input("Teléfono: ")
        direccion = input("Dirección: ")
        email = input("Email: ")
        idUsuario = int(input("ID Usuario: "))
        idSucursal = input("ID Sucursal (opcional, presione Enter para omitir): ")
        
        idSucursal = int(idSucursal) if idSucursal else None
        
        try:
            cliente = ClienteCRUD.create(
                nombre=nombre,
                documento=documento,
                telefono=telefono,
                direccion=direccion,
                email=email,
                idUsuario=idUsuario,
                idSucursal=idSucursal
            )
            print(f"Cliente creado exitosamente: {cliente}")
        except Exception as e:
            print(f"Error al crear cliente: {e}")
    
    def listar_clientes(self):
        """Lista todos los clientes"""
        print("\n--- LISTA DE CLIENTES ---")
        try:
            clientes = ClienteCRUD.get_all()
            if not clientes:
                print("No hay clientes registrados.")
                return
            
            for cliente in clientes:
                print(f"ID: {cliente.idCliente}, Nombre: {cliente.nombre}, Documento: {cliente.documento}")
        except Exception as e:
            print(f"Error al listar clientes: {e}")
    
    def buscar_cliente(self):
        """Busca un cliente por ID"""
        try:
            cliente_id = int(input("Ingrese el ID del cliente: "))
            cliente = ClienteCRUD.get_by_id(cliente_id)
            
            if cliente:
                print(f"\nCliente encontrado:")
                print(f"ID: {cliente.idCliente}")
                print(f"Nombre: {cliente.nombre}")
                print(f"Documento: {cliente.documento}")
                print(f"Teléfono: {cliente.telefono}")
                print(f"Dirección: {cliente.direccion}")
                print(f"Email: {cliente.email}")
                print(f"ID Usuario: {cliente.idUsuario}")
                print(f"ID Sucursal: {cliente.idSucursal}")
            else:
                print("Cliente no encontrado.")
        except ValueError:
            print("ID debe ser un número entero.")
        except Exception as e:
            print(f"Error al buscar cliente: {e}")
    
    def actualizar_cliente(self):
        """Actualiza un cliente existente"""
        try:
            cliente_id = int(input("Ingrese el ID del cliente a actualizar: "))
            cliente = ClienteCRUD.get_by_id(cliente_id)
            
            if not cliente:
                print("Cliente no encontrado.")
                return
            
            print("\nDeje en blanco los campos que no desea modificar:")
            nombre = input(f"Nuevo nombre [{cliente.nombre}]: ") or cliente.nombre
            documento = input(f"Nuevo documento [{cliente.documento}]: ") or cliente.documento
            telefono = input(f"Nuevo teléfono [{cliente.telefono}]: ") or cliente.telefono
            direccion = input(f"Nueva dirección [{cliente.direccion}]: ") or cliente.direccion
            email = input(f"Nuevo email [{cliente.email}]: ") or cliente.email
            idUsuario = input(f"Nuevo ID Usuario [{cliente.idUsuario}]: ") or cliente.idUsuario
            idSucursal = input(f"Nuevo ID Sucursal [{cliente.idSucursal}]: ") or cliente.idSucursal
            
            # Convertir a tipos adecuados
            idUsuario = int(idUsuario) if idUsuario else cliente.idUsuario
            idSucursal = int(idSucursal) if idSucursal else cliente.idSucursal
            
            cliente_actualizado = ClienteCRUD.update(
                cliente_id,
                nombre=nombre,
                documento=documento,
                telefono=telefono,
                direccion=direccion,
                email=email,
                idUsuario=idUsuario,
                idSucursal=idSucursal
            )
            
            if cliente_actualizado:
                print("Cliente actualizado exitosamente.")
            else:
                print("Error al actualizar cliente.")
        except ValueError:
            print("ID debe ser un número entero.")
        except Exception as e:
            print(f"Error al actualizar cliente: {e}")
    
    def eliminar_cliente(self):
        """Elimina un cliente"""
        try:
            cliente_id = int(input("Ingrese el ID del cliente a eliminar: "))
            confirmacion = input(f"¿Está seguro de eliminar el cliente {cliente_id}? (s/n): ")
            
            if confirmacion.lower() == 's':
                resultado = ClienteCRUD.delete(cliente_id)
                if resultado:
                    print("Cliente eliminado exitosamente.")
                else:
                    print("Error al eliminar cliente o cliente no encontrado.")
        except ValueError:
            print("ID debe ser un número entero.")
        except Exception as e:
            print(f"Error al eliminar cliente: {e}")
    
    # Métodos similares para las otras entidades (cuentas, empleados, etc.)
    # Se implementarían siguiendo el mismo patrón que para clientes
    
    def menu_cuentas(self):
        """Menú para gestión de cuentas"""
        while True:
            print("\n--- GESTIÓN DE CUENTAS ---")
            print("1. Crear cuenta")
            print("2. Listar todas las cuentas")
            print("3. Buscar cuenta por ID")
            print("4. Actualizar cuenta")
            print("5. Eliminar cuenta")
            print("6. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self.crear_cuenta()
            elif opcion == "2":
                self.listar_cuentas()
            elif opcion == "3":
                self.buscar_cuenta()
            elif opcion == "4":
                self.actualizar_cuenta()
            elif opcion == "5":
                self.eliminar_cuenta()
            elif opcion == "6":
                break
            else:
                print("Opción no válida.")
    
    def crear_cuenta(self):
        """Crea una nueva cuenta"""
        print("\n--- CREAR NUEVA CUENTA ---")
        numeroCuenta = input("Número de cuenta: ")
        saldo = float(input("Saldo inicial: "))
        estado = input("Estado (activa/inactiva): ")
        tipoCuenta = input("Tipo de cuenta (ahorro/corriente/crédito): ")
        idCliente = int(input("ID Cliente: "))
        
        try:
            cuenta = CuentaCRUD.create(
                numeroCuenta=numeroCuenta,
                saldo=saldo,
                estado=estado,
                tipoCuenta=tipoCuenta,
                idCliente=idCliente
            )
            print(f"Cuenta creada exitosamente: {cuenta}")
        except Exception as e:
            print(f"Error al crear cuenta: {e}")
    
    def listar_cuentas(self):
        """Lista todas las cuentas"""
        print("\n--- LISTA DE CUENTAS ---")
        try:
            cuentas = CuentaCRUD.get_all()
            if not cuentas:
                print("No hay cuentas registradas.")
                return
            
            for cuenta in cuentas:
                print(f"ID: {cuenta.idCuenta}, Número: {cuenta.numeroCuenta}, Tipo: {cuenta.tipoCuenta}, Saldo: {cuenta.saldo}")
        except Exception as e:
            print(f"Error al listar cuentas: {e}")
    
    def buscar_cuenta(self):
        """Busca una cuenta por ID"""
        try:
            cuenta_id = int(input("Ingrese el ID de la cuenta: "))
            cuenta = CuentaCRUD.get_by_id(cuenta_id)
            
            if cuenta:
                print(f"\nCuenta encontrada:")
                print(f"ID: {cuenta.idCuenta}")
                print(f"Número: {cuenta.numeroCuenta}")
                print(f"Saldo: {cuenta.saldo}")
                print(f"Fecha Apertura: {cuenta.fechaApertura}")
                print(f"Estado: {cuenta.estado}")
                print(f"Tipo: {cuenta.tipoCuenta}")
                print(f"ID Cliente: {cuenta.idCliente}")
            else:
                print("Cuenta no encontrada.")
        except ValueError:
            print("ID debe ser un número entero.")
        except Exception as e:
            print(f"Error al buscar cuenta: {e}")
    
    # Los métodos para empleados, sucursales, transacciones y usuarios
    # seguirían un patrón similar. Por brevedad, no los implemento completamente aquí,
    # pero se implementarían de la misma manera que para clientes y cuentas.
    
    def menu_empleados(self):
        """Menú para gestión de empleados"""
        print("\n--- GESTIÓN DE EMPLEADOS ---")
        print("Funcionalidad en desarrollo...")
        # Implementar similar a menu_clientes()
    
    def menu_sucursales(self):
        """Menú para gestión de sucursales"""
        print("\n--- GESTIÓN DE SUCURSALES ---")
        print("Funcionalidad en desarrollo...")
        # Implementar similar a menu_clientes()
    
    def menu_transacciones(self):
        """Menú para gestión de transacciones"""
        print("\n--- GESTIÓN DE TRANSACCIONES ---")
        print("Funcionalidad en desarrollo...")
        # Implementar similar a menu_clientes()
    
    def menu_usuarios(self):
        """Menú para gestión de usuarios"""
        print("\n--- GESTIÓN DE USUARIOS ---")
        print("Funcionalidad en desarrollo...")
        # Implementar similar a menu_clientes()

def main():
    """Función principal que inicia el sistema"""
    try:
        menu = MenuSistemaBancario()
        
        menu.mostrar_menu_principal()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()