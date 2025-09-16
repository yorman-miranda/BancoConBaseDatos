
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class User(Base):
    """
    Entidad User: representa un usuario del sistema.
    Incluye datos personales, credenciales de acceso
    y campos de auditoría.
    """
    __tablename__ = "users"

    idUser = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    createdBy = Column(Integer, ForeignKey("users.idUser"), nullable=False)
    updatedBy = Column(Integer, ForeignKey("users.idUser"), nullable=True)
    createdAt = Column(DateTime, default=datetime.now, nullable=False)
    updatedAt = Column(DateTime, default=None, onupdate=datetime.now)

    def __repr__(self):
        return f"<User {self.firstName} {self.lastName} ({self.username})>"