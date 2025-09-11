

from ..entities.sucursal import Sucursal
from ..database.database import get_session_context

class SucursalCRUD:
    """
    CRUD para la entidad Sucursal.
    Permite crear, leer, actualizar y eliminar sucursales.
    """

    @staticmethod
    def create(nombreSucursal, ciudad, direccion, telefono):
        """
        Crea una nueva sucursal en la base de datos.
        """
        with get_session_context() as session:
            sucursal = Sucursal(
                nombreSucursal=nombreSucursal,
                ciudad=ciudad,
                direccion=direccion,
                telefono=telefono
            )
            session.add(sucursal)
            session.flush()
            session.refresh(sucursal)
            return sucursal

    @staticmethod
    def get_by_id(sucursal_id):
        """
        Obtiene una sucursal por su ID.
        """
        with get_session_context() as session:
            return session.query(Sucursal).filter_by(idSucursal=sucursal_id).first()

    @staticmethod
    def get_all():
        """
        Obtiene todas las sucursales registradas.
        """
        with get_session_context() as session:
            return session.query(Sucursal).all()

    @staticmethod
    def update(sucursal_id, **kwargs):
        """
        Actualiza los datos de una sucursal.
        """
        with get_session_context() as session:
            sucursal = session.query(Sucursal).filter_by(idSucursal=sucursal_id).first()
            if not sucursal:
                return None
            for key, value in kwargs.items():
                if hasattr(sucursal, key):
                    setattr(sucursal, key, value)
            session.flush()
            session.refresh(sucursal)
            return sucursal

    @staticmethod
    def delete(sucursal_id):
        """
        Elimina una sucursal de la base de datos.
        """
        with get_session_context() as session:
            sucursal = session.query(Sucursal).filter_by(idSucursal=sucursal_id).first()
            if not sucursal:
                return False
            session.delete(sucursal)
            return True
