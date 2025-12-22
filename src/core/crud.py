from datetime import datetime

from sqlmodel import Session, select

from src.core.models import Categories, Items, Labels


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

    @staticmethod
    def get_label(session: Session):
        """Fetch all labels from the database

        Args:
            session (Session): The SQLAlchemy session used to interact with the database.

        Returns:
            list: A list of `Labels` objects retrieved from the database.
        """
        return session.exec(select(Labels)).all()

    @staticmethod
    def set_label(session: Session, name: str) -> bool:
        """Add a new label to the database

        Args:
            session (Session): The SQLAlchemy session used to interact with the database.
            name (str): The name of the new label to be added.

        Returns:
            bool: `True` if the label was successfully added, otherwise `False`.
        """
        try:
            stmt = Labels(name=name)
            session.add(stmt)
            session.commit()
            session.refresh(stmt)
            return True

        except Exception:
            return False

    @staticmethod
    def get_item(session: Session):
        """Fetch all items from the database

        Args:
            session (Session): The SQLAlchemy session used to interact with the database.

        Returns:
            list: A list of `Items` objects retrieved from the database.
        """
        return session.exec(select(Items)).all()

    @staticmethod
    def set_item(
        session: Session,
        date: datetime,
        category: int,
        name: str,
        label: int,
        total: int,
    ) -> bool:
        """Add a new item to the database

        Args:
            session (Session): The SQLAlchemy session used to interact with the database.
            name (str): The name of the new item to be added.

        Returns:
            bool: `True` if the item was successfully added, otherwise `False`.
        """
        try:
            stmt = Items(
                date=date, category_id=category, name=name, label_id=label, total=total
            )
            session.add(stmt)
            session.commit()
            session.refresh(stmt)
            return True

        except Exception:
            return False

    @staticmethod
    def delete_item(session: Session, item_id: int) -> bool:
        """Delete an item from database

        Args:
            session (Session): The SQLAlchemy session used to interact with the database.
            id (int): The id of item to be delete.

        Returns:
            bool: `True` if the item was successfully deleted, otherwise `False`.
        """
        try:
            stmt = select(Items).where(Items.id == item_id)
            item = session.exec(stmt).one()
            session.delete(item)
            session.commit()
            return True

        except:
            return False
