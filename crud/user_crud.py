
from datetime import datetime
from entities.user import User
from database.config import get_session_context

class UserCRUD:
    """
    CRUD para la entidad User.
    Proporciona métodos para crear, leer, actualizar y eliminar usuarios.
    """

    @staticmethod
    def create(firstName, lastName, username, password, createdBy):
        """
        Crea un nuevo usuario en la base de datos.
        """
        with get_session_context() as session:
            user = User(
                firstName=firstName,
                lastName=lastName,
                username=username,
                password=password,
                createdBy=createdBy
            )
            session.add(user)
            session.flush()
            session.refresh(user)
            return user

    @staticmethod
    def get_by_id(user_id):
        """
        Obtiene un usuario por su ID.
        """
        with get_session_context() as session:
            return session.query(User).filter_by(idUser=user_id).first()

    @staticmethod
    def get_all():
        """
        Obtiene todos los usuarios registrados.
        """
        with get_session_context() as session:
            return session.query(User).all()

    @staticmethod
    def update(user_id, updatedBy, **kwargs):
        """
        Actualiza los datos de un usuario y registra quién lo modificó.
        """
        with get_session_context() as session:
            user = session.query(User).filter_by(idUser=user_id).first()
            if not user:
                return None

            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            user.updatedBy = updatedBy
            user.updatedAt = datetime.now()

            session.flush()
            session.refresh(user)
            return user

    @staticmethod
    def delete(user_id):
        """
        Elimina un usuario de la base de datos.
        """
        with get_session_context() as session:
            user = session.query(User).filter_by(idUser=user_id).first()
            if not user:
                return False
            session.delete(user)
            return True
