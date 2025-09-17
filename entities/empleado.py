
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class Empleado(Base):
    """
    Entidad Empleado: representa a un trabajador
    asignado a una sucursal.
    """
    __tablename__ = "empleados"

    idEmpleado = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    cargo = Column(String(100), nullable=False)

    idSucursal = Column(Integer, ForeignKey("sucursales.idSucursal"))
    sucursal = relationship("Sucursal")

    def __repr__(self):
        return f"<Empleado {self.nombre} {self.apellido} - {self.cargo}>"
