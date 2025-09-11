"""
Entidad Cliente
===============

Este módulo define la entidad Cliente y sus modelos Pydantic.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database.database import Base

class Cliente(Base):
    """
    Entidad Cliente: representa un cliente del banco.
    Se asocia con un usuario del sistema y opcionalmente
    con una sucursal.
    """
    __tablename__ = "clientes"

    idCliente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    documento = Column(String(50), unique=True, nullable=False)
    telefono = Column(String(20))
    direccion = Column(String(200))
    email = Column(String(100))

    idUsuario = Column(Integer, ForeignKey("users.idUser"))
    idSucursal = Column(Integer, ForeignKey("sucursales.idSucursal"), nullable=True)

    usuario = relationship("User")
    sucursal = relationship("Sucursal")

    def __repr__(self):
        return f"<Cliente {self.nombre} ({self.documento})>"
