
from entities.empleado import Empleado
from database.config import get_session_context

class EmpleadoCRUD:
    """
    CRUD para la entidad Empleado.
    Permite crear, leer, actualizar y eliminar empleados.
    """

    @staticmethod
    def create(nombre, apellido, cargo, idSucursal):
        """
        Crea un nuevo empleado en la base de datos.
        """
        with get_session_context() as session:
            empleado = Empleado(
                nombre=nombre,
                apellido=apellido,
                cargo=cargo,
                idSucursal=idSucursal
            )
            session.add(empleado)
            session.flush()
            session.refresh(empleado)
            return empleado

    @staticmethod
    def get_by_id(empleado_id):
        """
        Obtiene un empleado por su ID.
        """
        with get_session_context() as session:
            return session.query(Empleado).filter_by(idEmpleado=empleado_id).first()

    @staticmethod
    def get_all():
        """
        Obtiene todos los empleados registrados.
        """
        with get_session_context() as session:
            return session.query(Empleado).all()

    @staticmethod
    def update(empleado_id, **kwargs):
        """
        Actualiza los datos de un empleado.
        """
        with get_session_context() as session:
            empleado = session.query(Empleado).filter_by(idEmpleado=empleado_id).first()
            if not empleado:
                return None
            for key, value in kwargs.items():
                if hasattr(empleado, key):
                    setattr(empleado, key, value)
            session.flush()
            session.refresh(empleado)
            return empleado

    @staticmethod
    def delete(empleado_id):
        """
        Elimina un empleado de la base de datos.
        """
        with get_session_context() as session:
            empleado = session.query(Empleado).filter_by(idEmpleado=empleado_id).first()
            if not empleado:
                return False
            session.delete(empleado)
            return True
