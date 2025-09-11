

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.database import Base

class Transaccion(Base):
    """
    Entidad Transaccion: representa una operación
    realizada sobre una cuenta (depósito, retiro,
    transferencia, etc.).
    """
    __tablename__ = "transacciones"

    idTransaccion = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(50), nullable=False)
    monto = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.now)

    idCuenta = Column(Integer, ForeignKey("cuentas.idCuenta"))
    cuenta = relationship("Cuenta")

    def __repr__(self):
        return f"<Transacción {self.tipo} - Monto: {self.monto}>"
