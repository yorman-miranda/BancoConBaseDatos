"""
Base declarativa única para todos los modelos SQLAlchemy.
Evita conflictos de múltiples instancias de declarative_base.
"""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()