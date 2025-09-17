
"""
Script para probar la creación de tablas
"""
from database.config import create_tables, check_connection

if __name__ == "__main__":
    print("Probando conexión y creación de tablas...")
    
    if check_connection():
        print("✓ Conexión exitosa")
        try:
            create_tables()
            print("✓ Tablas creadas exitosamente")
            print("\nTablas creadas:")
            from database.base import Base
            for table_name in Base.metadata.tables.keys():
                print(f"  - {table_name}")
        except Exception as e:
            print(f"✗ Error creando tablas: {e}")
    else:
        print("✗ Error de conexión")