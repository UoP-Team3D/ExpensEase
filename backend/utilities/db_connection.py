import psycopg2
import os
from urllib.parse import urlparse
import logging

def get_db_connection():
    """
    Establishes a connection to the database using the DATABASE_URL environment variable.

    The DATABASE_URL should be in the format: 'postgresql://username:password@host:port/dbname'.
    If the port is not specified, the default PostgreSQL port 5432 is used. Typically it will just be 5432 unless you specified otherwise

    Raises:
        EnvironmentError: If the DATABASE_URL is not set, cannot be parsed, 
        ValueError: If the DATABASE_URL format is invalid
        ConnectionError: If database connection failed
        RuntimeError: Any other unexpected issue occurs

    Returns:
        psycopg2.connection: A connection object to the PostgreSQL database.
    """
    logger = logging.getLogger(__name__)

    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        logger.error(f"Couldn't find DATABASE_URL environment variable! Check the .env file for it.")
        raise EnvironmentError("DATABASE_URL environment variable not set")

    try:
        parsed_url = urlparse(database_url)

        dbname = parsed_url.path[1:]  # Remove the leading slash "/dbname"
        user = parsed_url.username
        password = parsed_url.password
        host = parsed_url.hostname
        port = parsed_url.port or 5432  # Use the default port if not specified

        if not all([dbname, user, password, host]):
            logger.error(f"DATABASE_URL is formatted incorrectly. Should be in the format 'postgresql://username:password@host:port/dbname'")
            raise ValueError("Invalid DATABASE_URL format")

        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        return connection

    except psycopg2.Error as e:
        logger.error(f"Database connection failed! Ensure your ExpensEase database is setup correctly and re-try.")
        raise ConnectionError(f"Database connection failed: {e}")
    except Exception as e:
        logger.error(f"Unknown error happened! The error: {e}")
        raise RuntimeError(f"An error occurred: {e}")
