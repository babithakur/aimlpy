"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 23/10/2024
"""

from sqlalchemy import create_engine, text
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

from cacs456ml.setting import Settings
from cacs456ml.util import loggerutil


class Base(DeclarativeBase):
    pass


logger = loggerutil.get_logger(__name__)


class DataSource:
    def __init__(self):
        """
        Initializes the DataSource with the given database URL
        """
        try:
            self.engine = create_engine(Settings.DB_URL,
                                        pool_size=20,
                                        max_overflow=30,
                                        pool_timeout=60,
                                        pool_recycle=3600)
            self.ping()
            self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.create_or_migrate_tables()
        except Exception as e:
            logger.exception(f"Database connection error: {e}")
            exit(1)

    def ping(self):
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                logger.info(f"Database connection established: {result.scalar()}")
        except Exception as e:
            logger.exception(f"Database connection error: {e}")

    def get_session(self) -> Session:
        """
        Creates a new SQLAlchemy session.
        Use this method to get a session for interacting with the database.
        """
        return self.Session()

    def close_session(self, session: Session):
        """
        Closes the given SQLAlchemy session.
        Use this method to close the session after the transaction is complete.
        """
        if session:
            session.close()

    # def create_tables(self):
    #     """
    #     Creates all tables in the database using the Base metadata.
    #     This method should be run once when you want to initialize the tables.
    #     """
    #     Base.metadata.create_all(bind=self.engine)

    def create_or_migrate_tables(self):
        """
        Create tables if they do not exist, or migrate (modify schema) if necessary.
        This method will handle both initial creation and migrations without dropping tables.
        """
        try:
            # Create tables if they do not exist
            self.create_tables()
            # Migrate tables (adding new columns, etc.)
            self.migrate_tables()
        except OperationalError as e:
            logger.exception(f"Error managing tables: {e}")
            exit(1)

    def create_tables(self):
        """
        Creates all tables in the database using the Base metadata if they do not exist.
        """
        try:
            # Check if tables already exist
            if not self.check_tables_exist():
                Base.metadata.create_all(bind=self.engine)
                logger.info("Tables created successfully.")
            else:
                logger.info("Tables already exist.")
        except OperationalError as e:
            logger.exception(f"Error creating tables: {e}")
            exit(1)

    def migrate_tables(self):
        """
        Checks for changes in schema (e.g., new columns) and adds them without dropping tables.
        """
        try:
            # Inspect the current state of the database and compare it with the models
            inspector = inspect(self.engine)
            for table in Base.metadata.tables.values():
                if table.name in inspector.get_table_names():
                    logger.info(f"Table '{table.name}' exists. Checking for schema changes...")
                    # Manually add missing columns or perform other migrations
                    self.add_columns_if_needed(table)
            logger.info("Tables migration completed successfully.")
        except OperationalError as e:
            logger.exception(f"Error migrating tables: {e}")
            exit(1)

    def check_tables_exist(self):
        """
        Checks if the tables already exist in the database.
        Returns True if tables exist, False otherwise.
        """
        try:
            inspector = inspect(self.engine)
            return len(inspector.get_table_names()) > 0
        except OperationalError:
            return False

    def add_columns_if_needed(self, table):
        """
        Add missing columns to the table if they are not already present.
        """
        try:
            inspector = inspect(self.engine)
            existing_columns = {col['name'] for col in inspector.get_columns(table.name)}

            with self.engine.connect() as connection:
                for column in table.columns:
                    if column.name not in existing_columns:
                        # Generate raw SQL for adding a column
                        column_type = column.type.compile(dialect=self.engine.dialect)  # Get column type
                        alter_stmt = f'ALTER TABLE "{table.name}" ADD COLUMN {column.name} {column_type}'

                        logger.info(f"Executing: {alter_stmt}")
                        connection.execute(text(alter_stmt))

                        logger.info(f"Column '{column.name}' added to table '{table.name}'.")
        except Exception as e:
            logger.exception(f"Error adding columns to table '{table.name}': {e}")
