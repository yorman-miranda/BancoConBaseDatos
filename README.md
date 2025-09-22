# /* Sistema Bancario - Documentación/* 
##  📋 Descripción del Proyecto
Sistema bancario completo desarrollado en Python con arquitectura modular, base de datos PostgreSQL y interfaz de línea de comandos. El sistema gestiona usuarios, clientes, empleados, sucursales, cuentas bancarias y transacciones financieras.

## 🏗️ Arquitectura del Sistema

sistema_bancario/
├── entities/           # Modelos de base de datos <br>
├── crud/              # Operaciones CRUD <br>
├── database/          # Configuración de base de datos <br>
├── auth/             # Autenticación y seguridad <br> 
├── banco.py          # Lógica de negocio <br>  
└── menu.py          # Interfaz principal <br>


🎯 Roles del Sistema
### 1. Administrador

- Crear empleados y sucursales
- Gestionar usuarios del sistema
- Ver reportes generales
- Acceso completo al sistema

### 2. Empleado

- Gestión de clientes
- Apertura de cuentas bancarias
- Operaciones bancarias para clientes
- Consultas de sucursal

### 3. Cliente

- Gestión de cuentas propias
- Operaciones bancarias personales
- Consulta de movimientos
- Información personal

# 🚀 Instalación y Configuración

### Prerrequisitos
Python 3.8+

#### 1. Clona el repositorio
- en VsCode abrir terminal: Control-shit-ñ
- elegir parte donde se quiere clonar:  `cd [URL]` donde se va a guardar y presionar  `enter`
- copiar `git clone URL` del repositorio y presionar `enter`

#### 2. Instalar dependencias

`pip install sqlalchemy` 
`pip install psycopg2-binary`
`pip install python-dotenv`

#### 3. Ejecutar el sistema 

ingresar a la terminal: `python MenuPrincipal.py`

## 📊 Estructura de la Base de Datos
### Tablas Principales
#### users - Usuarios del sistema

- idUser (UUID, PK)
- firstName, lastName (String)
- username (String, Unique)
- password (String, Hash)
- activo (Boolean)
- es_admin (Boolean)
- Campos de auditoría

#### clientes - Clientes del banco

- idCliente (UUID, PK)
- nombre, documento (String, Unique)
- telefono, email, direccion
- idUsuario (FK → users)
- idSucursal (FK → sucursales)

#### empleados - Empleados del banco

- idEmpleado (UUID, PK)
- nombre, apellido, cargo
- idSucursal (FK → sucursales)
- idUsuario (FK → users)

#### sucursales - Sucursales bancarias

- idSucursal (UUID, PK)
- nombreSucursal, ciudad
- direccion, telefono
- cuentas - Cuentas bancarias
- idCuenta (UUID, PK)
- numeroCuenta (String, Unique)
- saldo (Float)
- tipoCuenta (AHORRO/CORRIENTE/CREDITO)
- estado (ACTIVA/BLOQUEADA/SUSPENDIDA)
- idCliente (FK → clientes)

#### transacciones - Transacciones bancarias

- idTransaccion (UUID, PK)
- tipo (String)
- monto (Float)
- fecha (DateTime)
- idCuenta (FK → cuentas)

### 💻 Uso del Sistema

#### Flujo Principal
- Inicialización
- Verificación de conexión a BD
- Creación de tablas
- Creación de usuario admin por defecto
- Autenticación
- Login con username/password
- Detección automática de rol
- Redirección a menú correspondiente
- Operaciones por Rol

## Comandos del Administrador

#### Usuario: admin
#### Contraseña: admin_1234
- Crear empleados y asignar sucursales
- Gestionar sucursales bancarias
- Ver reportes del sistema
- Monitorear usuarios activos
- Comandos del Empleado
- Registrar nuevos clientes
- Abrir cuentas bancarias
- Realizar operaciones para clientes
- Consultar información de sucursal

## Comandos del Cliente

- Gestionar cuentas propias
- Realizar depósitos/retiros/transferencias
- Consultar saldos y movimientos
- Ver información personal

## 🔄 Operaciones Bancarias Implementadas
- Transacciones
- Depósitos: Incremento seguro de saldo
- Retiros: Validación de fondos disponibles
- Transferencias: Transacciones atómicas entre cuentas
- Validaciones
- Saldo suficiente para retiros
- Estados de cuenta (ACTIVA/BLOQUEADA)
- Integridad referencial
- Transacciones atómicas

## 🛠️ Tecnologías Utilizadas
- Python 3.8+: Lenguaje principal
- SQLAlchemy: ORM para base de datos
- PostgreSQL: Base de datos relacional
- psycopg2: Adaptador PostgreSQL para Python
- python-dotenv: Manejo de variables de entorno

## 📁 Estructura de Archivos
bash
sistema_bancario/ <br>
├── entities/ <br>
│   ├── user.py <br>
│   ├── cliente.py <br>
│   ├── empleado.py <br>
│   ├── sucursal.py <br>
│   ├── cuenta.py <br>
│   └── transaccion.py <br>
├── crud/ <br> 
│   ├── user_crud.py <br>
│   ├── cliente_crud.py <br>
│   ├── empleado_crud.py <br>
│   ├── sucursal_crud.py <br>
│   ├── cuenta_crud.py <br>
│   └── transaccion_crud.py <br>
├── database/ <br>
│   ├── config.py <br>
│   └── base.py <br>
├── auth/ <br>
│   └── security.py <br>
├── banco.py <br>
├── MEnu2.py <br>
└── .env <br>


