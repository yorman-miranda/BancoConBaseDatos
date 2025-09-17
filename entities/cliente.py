

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database.base import Base

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
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    idUsuario = Column(Integer, ForeignKey("users.idUser"))
    idSucursal = Column(Integer, ForeignKey("sucursales.idSucursal"), nullable=True)

    usuario = relationship("User")
    sucursal = relationship("Sucursal")

    def __repr__(self):
        return f"<Cliente {self.nombre} ({self.documento})>"