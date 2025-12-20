from typing import Generator

from sqlmodel import Session, SQLModel, create_engine


class Database:
    """A utility class to manage database connections"""

    engine = create_engine(url="sqlite:///data/finance.db")

    @classmethod
    def connect(cls) -> None:
        """Create all tables in the database

        This method initializes the database and ensures that all tables
        defined by SQLModel models are created in the database. If the
        tables already exist, no changes will be made.

        Args:
            cls: The class itself. This is automatically passed by Python.
        """
        SQLModel.metadata.create_all(cls.engine)

    @classmethod
    def disconnect(cls) -> None:
        """Close the database connection

        This method disposes of the engine, effectively closing any active
        connections to the database. It is important to call this method when
        finished interacting with the database to avoid connection leaks.

        Args:
            cls: The class itself. This is automatically passed by Python.
        """
        cls.engine.dispose()

    @classmethod
    def get_session(cls) -> Generator[Session, None, None]:
        """Get a database session

        This method creates and returns a new session object that can be used
        to interact with the database. It is important to close the session
        after use to release resources. This method uses a context manager to
        ensure that the session is closed automatically when done.

        Args:
            cls: The class itself. This is automatically passed by Python.

        Yields:
            Session: A SQLAlchemy session instance connected to the database.

        Example:
            with Database.get_session() as session:
                # Use session for database operations
                session.query(...).all()
                # Session will be closed automatically after the block
        """
        with Session(cls.engine) as session:
            try:
                yield session
            finally:
                session.close()
