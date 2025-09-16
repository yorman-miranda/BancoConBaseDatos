
#!/usr/bin/env python3
"""
Script simple para probar la conexión sin importaciones complejas
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DB_HOST = os.getenv("DB_HOST", "ep-empty-hall-adpyub1b-pooler.c-2.us-east-1.aws.neon.tech")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "neondb")
DB_USERNAME = os.getenv("DB_USERNAME", "neondb_owner")
DB_PASSWORD = os.getenv("DB_PASSWORD", "npg_PSuZYwob10ON")

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print("=== PRUEBA SIMPLE DE CONEXIÓN ===")
print(f"URL: {DATABASE_URL.replace(DB_PASSWORD, '***')}")

try:
    engine = create_engine(DATABASE_URL, echo=True)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))
        version = result.scalar()
        print(f"✅ Conexión exitosa! PostgreSQL version: {version}")
        
        # Listar tablas
        result = connection.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        tables = result.fetchall()
        
        print("\n📊 Tablas en la base de datos:")
        if tables:
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print("  (No hay tablas)")
            
except Exception as e:
    print(f"❌ Error de conexión: {e}")