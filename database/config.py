# """
# Configuración de la base de datos PostgreSQL con Neon
# """

# import os

# from dotenv import load_dotenv
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# # Cargar variables de entorno
# load_dotenv()

# # Configuración de la base de datos Neon PostgreSQL
# # Obtener la URL completa de conexión desde las variables de entorno
# DATABASE_URL = os.getenv("psql 'postgresql://neondb_owner:npg_PSuZYwob10ON@ep-empty-hall-adpyub1b-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'")

# # Si no hay DATABASE_URL, construir desde variables individuales
# if not DATABASE_URL:
#     #DB_HOST = os.getenv("DB_HOST", "localhost")
#     DB_HOST = os.getenv("DB_HOST", "ep-empty-hall-adpyub1b-pooler.c-2.us-east-1.aws.neon.tech")
#     DB_PORT = os.getenv("DB_PORT", "5432")
#     DB_NAME = os.getenv("DB_NAME", "neondb")
#     DB_USERNAME = os.getenv("DB_USERNAME", "neondb_owner")
#     DB_PASSWORD = os.getenv("DB_PASSWORD", "npg_PSuZYwob10ON")

#     if DB_USERNAME and DB_PASSWORD:
#         DATABASE_URL = (
#         f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#         )
#     else:
#         raise ValueError(
#             "Se requiere DATABASE_URL o las credenciales individuales de la base de datos"
#         )

# # Crear el motor de SQLAlchemy
# engine = create_engine(
#     DATABASE_URL,
#     echo=True,  # Mostrar las consultas SQL en consola
#     pool_pre_ping=True,  # Verificar conexión antes de usar
#     pool_recycle=300,  # Reciclar conexiones cada 5 minutos
# )

# # Crear la sesión
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base para los modelos
# Base = declarative_base()


# def get_db():
#     """
#     Generador de sesiones de base de datos
#     """
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# def create_tables():
#     """
#     Crear todas las tablas definidas en los modelos
#     """
#     Base.metadata.create_all(bind=engine)


"""
Configuración completa de la base de datos PostgreSQL con Neon
"""

# import os
# from typing import Generator
# from dotenv import load_dotenv
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, Session
# from sqlalchemy.ext.declarative import declarative_base
# from contextlib import contextmanager
# import logging

# # Cargar variables de entorno
# load_dotenv()

# # Configurar logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Configuración de la base de datos Neon PostgreSQL
# DB_HOST = os.getenv("DB_HOST", "ep-empty-hall-adpyub1b-pooler.c-2.us-east-1.aws.neon.tech")
# DB_PORT = os.getenv("DB_PORT", "5432")
# DB_NAME = os.getenv("DB_NAME", "neondb")
# DB_USERNAME = os.getenv("DB_USERNAME", "neondb_owner")
# DB_PASSWORD = os.getenv("DB_PASSWORD", "npg_PSuZYwob10ON")

# # Construir la URL de conexión CORRECTAMENTE
# DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# # Configuraciones adicionales
# DB_ECHO = os.getenv("DB_ECHO", "True").lower() == "true"

# # Crear la clase base para los modelos
# Base = declarative_base()

# # Importar todos los modelos para que SQLAlchemy los detecte
# try:
#     from entities.user import User
#     from entities.cliente import Cliente
#     from entities.cuenta import Cuenta
#     from entities.empleado import Empleado
#     from entities.sucursal import Sucursal
#     from entities.transaccion import Transaccion
#     logger.info("Todos los modelos importados correctamente")
# except ImportError as e:
#     logger.warning(f"No se pudieron importar algunos modelos: {e}")

# # Configurar el motor de base de datos
# engine = create_engine(
#     DATABASE_URL,
#     echo=DB_ECHO,
#     pool_pre_ping=True,
#     pool_recycle=300,
# )

# # Crear la fábrica de sesiones
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def get_db() -> Generator[Session, None, None]:
#     """
#     Generador de sesiones de base de datos para FastAPI
#     """
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @contextmanager
# def get_session_context() -> Generator[Session, None, None]:
#     """
#     Context manager para manejar sesiones de base de datos
#     """
#     session = SessionLocal()
#     try:
#         yield session
#         session.commit()
#     except Exception as e:
#         logger.error(f"Error en la sesión: {e}")
#         session.rollback()
#         raise
#     finally:
#         session.close()

# def create_tables():
#     """
#     Crear todas las tablas definidas en los modelos
#     """
#     try:
#         logger.info("Creando tablas en la base de datos...")
#         Base.metadata.create_all(bind=engine)
#         logger.info("Tablas creadas exitosamente")
#     except Exception as e:
#         logger.error(f"Error al crear tablas: {e}")
#         raise

# def check_connection():
#     """
#     Verifica la conexión a la base de datos
#     """
#     try:
#         with engine.connect() as connection:
#             connection.execute("SELECT 1")
#         logger.info("Conexión a la base de datos exitosa")
#         return True
#     except Exception as e:
#         logger.error(f"Error de conexión a la base de datos: {e}")
#         return False

"""
Configuración completa de la base de datos PostgreSQL con Neon
"""

import os
import sys
from typing import Generator
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
import logging

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de la base de datos Neon PostgreSQL
DB_HOST = os.getenv("DB_HOST", "ep-empty-hall-adpyub1b-pooler.c-2.us-east-1.aws.neon.tech")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "neondb")
DB_USERNAME = os.getenv("DB_USERNAME", "neondb_owner")
DB_PASSWORD = os.getenv("DB_PASSWORD", "npg_PSuZYwob10ON")

# Construir la URL de conexión CORRECTAMENTE
DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Configuraciones adicionales
DB_ECHO = os.getenv("DB_ECHO", "True").lower() == "true"

# Crear la clase base para los modelos
Base = declarative_base()

# Añadir el directorio padre al path para importaciones absolutas
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Importar todos los modelos para que SQLAlchemy los detecte
try:
    # Importar usando rutas absolutas desde el directorio raíz
    from entities.user import User
    from entities.cliente import Cliente
    from entities.cuenta import Cuenta
    from entities.empleado import Empleado
    from entities.sucursal import Sucursal
    from entities.transaccion import Transaccion
    logger.info("✅ Todos los modelos importados correctamente")
except ImportError as e:
    logger.error(f"❌ Error al importar modelos: {e}")
    # Mostrar el path actual para debugging
    logger.error(f"Python path: {sys.path}")
    logger.error(f"Directorio actual: {os.getcwd()}")

# Configurar el motor de base de datos
engine = create_engine(
    DATABASE_URL,
    echo=DB_ECHO,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Crear la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    Generador de sesiones de base de datos para FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_session_context() -> Generator[Session, None, None]:
    """
    Context manager para manejar sesiones de base de datos
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        logger.error(f"Error en la sesión: {e}")
        session.rollback()
        raise
    finally:
        session.close()

def create_tables():
    """
    Crear todas las tablas definidas en los modelos
    """
    try:
        logger.info("Creando tablas en la base de datos...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tablas creadas exitosamente")
        
        # Verificar que las tablas se crearon
        with engine.connect() as conn:
            result = conn.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            tables = result.fetchall()
            
            logger.info("📊 Tablas en la base de datos:")
            if tables:
                for table in tables:
                    logger.info(f"  - {table[0]}")
            else:
                logger.warning("  (No se encontraron tablas)")
                
    except Exception as e:
        logger.error(f"❌ Error al crear tablas: {e}")
        raise

def check_connection():
    """
    Verifica la conexión a la base de datos
    """
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        logger.info("✅ Conexión a la base de datos exitosa")
        return True
    except Exception as e:
        logger.error(f"❌ Error de conexión a la base de datos: {e}")
        return False

# Función para probar la conexión y creación de tablas
def test_database():
    """Función completa de prueba de la base de datos"""
    print("=== PRUEBA DE CONEXIÓN A POSTGRESQL (NEON) ===")
    print(f"URL de conexión: {DATABASE_URL.replace(DB_PASSWORD, '***')}")
    
    if check_connection():
        print("✅ Conexión exitosa a PostgreSQL!")
        
        # Obtener versión de PostgreSQL
        with engine.connect() as conn:
            result = conn.execute("SELECT version()")
            version = result.scalar()
            print(f"📋 Versión de PostgreSQL: {version}")
            
            # Verificar base de datos actual
            result = conn.execute("SELECT current_database()")
            db_name = result.scalar()
            print(f"🗄️  Base de datos: {db_name}")
            
            # Listar tablas disponibles antes de crearlas
            print("\n📊 Tablas disponibles (antes):")
            result = conn.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            tables = result.fetchall()
            
            if tables:
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print("  (No hay tablas creadas aún)")
                
        # Crear tablas
        print("\n=== CREANDO TABLAS ===")
        create_tables()
        print("✅ Tablas creadas exitosamente")
        
    else:
        print("❌ No se pudo conectar a la base de datos")
        return False
    
    return True

if __name__ == "__main__":
    test_database()