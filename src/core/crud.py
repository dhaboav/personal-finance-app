from sqlmodel import Session, select

from src.core.models import Categories


class Crud:
    """CRUD operations for database"""

    @staticmethod
    def get_category(session: Session):
        """Fetch all categories from the database

        Args:
            session (Session): The SQLAlchemy session used to interact with the database.

        Returns:
            list: A list of `Categories` objects retrieved from the database.
        """
        return session.exec(select(Categories)).all()

    @staticmethod
    def set_category(session: Session, name: str) -> bool:
        """Add a new category to the database

        Args:
            session (Session): The SQLAlchemy session used to interact with the database.
            name (str): The name of the new category to be added.

        Returns:
            bool: `True` if the category was successfully added, otherwise `False`.
        """
        try:
            stmt = Categories(name=name)
            session.add(stmt)
            session.commit()
            session.refresh(stmt)
            return True

        except Exception:
            return False
