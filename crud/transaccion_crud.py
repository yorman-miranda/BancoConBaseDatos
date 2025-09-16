

from entities.transaccion import Transaccion
from database.config import get_session_context

class TransaccionCRUD:
    """
    CRUD para la entidad Transacción.
    Permite crear, leer, actualizar y eliminar transacciones.
    """

    @staticmethod
    def create(tipo, monto, idCuenta):
        """
        Crea una nueva transacción en la base de datos.
        """
        with get_session_context() as session:
            transaccion = Transaccion(
                tipo=tipo,
                monto=monto,
                idCuenta=idCuenta
            )
            session.add(transaccion)
            session.flush()
            session.refresh(transaccion)
            return transaccion

    @staticmethod
    def get_by_id(transaccion_id):
        """
        Obtiene una transacción por su ID.
        """
        with get_session_context() as session:
            return session.query(Transaccion).filter_by(idTransaccion=transaccion_id).first()

    @staticmethod
    def get_all():
        """
        Obtiene todas las transacciones registradas.
        """
        with get_session_context() as session:
            return session.query(Transaccion).all()

    @staticmethod
    def update(transaccion_id, **kwargs):
        """
        Actualiza los datos de una transacción.
        """
        with get_session_context() as session:
            transaccion = session.query(Transaccion).filter_by(idTransaccion=transaccion_id).first()
            if not transaccion:
                return None
            for key, value in kwargs.items():
                if hasattr(transaccion, key):
                    setattr(transaccion, key, value)
            session.flush()
            session.refresh(transaccion)
            return transaccion

    @staticmethod
    def delete(transaccion_id):
        """
        Elimina una transacción de la base de datos.
        """
        with get_session_context() as session:
            transaccion = session.query(Transaccion).filter_by(idTransaccion=transaccion_id).first()
            if not transaccion:
                return False
            session.delete(transaccion)
            return True
