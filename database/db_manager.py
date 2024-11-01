import logging

import psycopg2
from psycopg2.extras import execute_batch

from config.config import AppConfig, DatabaseConfig, load_config

logger = logging.getLogger(__name__)
app_config: AppConfig = load_config()


class DatabaseManager:
    def __init__(self, config: DatabaseConfig = app_config.database):
        """
        Initialize the DatabaseManager with the given database configuration.

        :param config: The database configuration settings. Defaults to the
                   application database configuration.
         :type config: DatabaseConfig
        """
        self.config = config

    def get_connection(self):
        """
        Establish a connection to the database.

        :return: A psycopg2 connection object.
        :raises Exception: If there is a problem connecting to the database.
        """
        try:
            session = psycopg2.connect(
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.user,
                password=self.config.password,
            )
        except Exception as e:
            logger.exception(f"Error connecting to database: {str(e)}")
            raise Exception(f"Error connecting to database: {str(e)}")

        return session

    def create_tables(self):
        """
        Create the tables in the database.

        :raises Exception: If there is an error creating the tables.
        """
        conn = self.get_connection()
        with conn.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS employees (
                        id SERIAL PRIMARY KEY,
                        full_name TEXT NOT NULL,
                        birth_date DATE NOT NULL,
                        gender TEXT NOT NULL
                    )
                """
                )
                conn.commit()
                conn.close()
                logger.info("Tables created successfully")
            except Exception as e:
                logger.exception(f"Error creating tables: {str(e)}")

    def create_indexes(self):
        """
        Create indexes in the database.

        :raises Exception: If there is an error creating the indexes.
        """
        conn = self.get_connection()
        with conn.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    CREATE INDEX IF NOT EXISTS idx_gender_name 
                    ON employees(gender, full_name)
                    
                """
                )

                logger.info("Indexes created successfully")
            except Exception as e:
                logger.exception(f"Error creating indexes: {str(e)}")

        conn.commit()
        conn.close()
