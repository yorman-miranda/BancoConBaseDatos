
from entities.cliente import Cliente
from database.config import get_session_context

class ClienteCRUD:
    """
    CRUD para la entidad Cliente.
    Permite crear, leer, actualizar y eliminar clientes.
    """

    @staticmethod
    def create(nombre, documento, telefono, direccion, email, idUsuario, idSucursal=None):
        """
        Crea un nuevo cliente en la base de datos.
        """
        with get_session_context() as session:
            cliente = Cliente(
                nombre=nombre,
                documento=documento,
                telefono=telefono,
                direccion=direccion,
                email=email,
                idUsuario=idUsuario,
                idSucursal=idSucursal
            )
            session.add(cliente)
            session.flush()
            session.refresh(cliente)
            return cliente

    @staticmethod
    def get_by_id(cliente_id):
        """
        Obtiene un cliente por su ID.
        """
        with get_session_context() as session:
            return session.query(Cliente).filter_by(idCliente=cliente_id).first()

    @staticmethod
    def get_all():
        """
        Obtiene todos los clientes registrados.
        """
        with get_session_context() as session:
            return session.query(Cliente).all()

    @staticmethod
    def update(cliente_id, **kwargs):
        """
        Actualiza los datos de un cliente.
        """
        with get_session_context() as session:
            cliente = session.query(Cliente).filter_by(idCliente=cliente_id).first()
            if not cliente:
                return None
            for key, value in kwargs.items():
                if hasattr(cliente, key):
                    setattr(cliente, key, value)
            session.flush()
            session.refresh(cliente)
            return cliente

    @staticmethod
    def delete(cliente_id):
        """
        Elimina un cliente de la base de datos.
        """
        with get_session_context() as session:
            cliente = session.query(Cliente).filter_by(idCliente=cliente_id).first()
            if not cliente:
                return False
            session.delete(cliente)
            return True
