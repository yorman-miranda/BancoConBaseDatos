
from sqlalchemy import Column, Integer, String
from ..database.database import Base

class Sucursal(Base):
    """
    Entidad Sucursal: representa una oficina o
    sucursal física del banco.
    """
    __tablename__ = "sucursales"

    idSucursal = Column(Integer, primary_key=True, autoincrement=True)
    nombreSucursal = Column(String(100), nullable=False)
    ciudad = Column(String(100), nullable=False)
    direccion = Column(String(200), nullable=False)
    telefono = Column(String(20))

    def __repr__(self):
        return f"<Sucursal {self.nombreSucursal} ({self.ciudad})>"
