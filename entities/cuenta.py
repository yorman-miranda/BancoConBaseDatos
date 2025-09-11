
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.database import Base

class Cuenta(Base):
    """
    Entidad Cuenta: representa una cuenta bancaria
    que pertenece a un cliente. Puede ser de tipo
    ahorro, corriente o crédito.
    """
    __tablename__ = "cuentas"

    idCuenta = Column(Integer, primary_key=True, autoincrement=True)
    numeroCuenta = Column(String(20), unique=True, nullable=False)
    saldo = Column(Float, default=0.0)
    fechaApertura = Column(DateTime, default=datetime.now)
    estado = Column(String(20), nullable=False)     
    tipoCuenta = Column(String(20), nullable=False)

    idCliente = Column(Integer, ForeignKey("clientes.idCliente"))
    cliente = relationship("Cliente")

    def __repr__(self):
        return f"<Cuenta {self.numeroCuenta} ({self.tipoCuenta}) - Saldo: {self.saldo}>"
