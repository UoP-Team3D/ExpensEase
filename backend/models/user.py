import psycopg2
import bcrypt
import logging

class User:
    """
    User class to handle user-related operations in the database.

    Attributes:
        db_connection: A psycopg2 connection object to the PostgreSQL database.

    Methods:
        register_user: Registers a new user in the database.
        login: Logs in an existing user.
    """

    def __init__(self, db_connection):
        """
        Initializes the User class with a database connection.

        Args:
            db_connection: A psycopg2 connection object to the PostgreSQL database.
        """
        self.logger = logging.getLogger(__name__)
        self.db_connection = db_connection

    def register_user(self, username, email, first_name, last_name, plain_password, pin):
        """
        Registers a new user in the database.

        Args:
            username: A string representing the user's username.
            email: A string representing the user's email.
            first_name: A string representing the user's first name.
            last_name: A string representing the user's last name.
            plain_password: A string representing the user's plaintext password.
            pin: A string representing the user's four digit personal identification number.

        Returns:
            The user ID of the newly created user.

        Raises:
            psycopg2.Error: If there is an error executing database operations.
        """
        # Hash the plain password using bcrypt
        hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())

        try:
            with self.db_connection.cursor() as cursor:
                check_query = """
                SELECT 1 FROM public."Users" WHERE username = %s or email = %s
                """
                cursor.execute(check_query, (username, email))
                
                if cursor.fetchone():
                    raise ValueError("Username or email already exists.")

                query = """
                INSERT INTO public."Users" (username, email, first_name, last_name, password, pin)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING user_id;
                """
                
                # Execute the query (psycopg2 handles sanitization of the sql input)
                cursor.execute(query, (username, email, first_name, last_name, hashed_password.decode('utf-8'), pin))
                user_id = cursor.fetchone()[0]
                self.db_connection.commit()
                return user_id
        except psycopg2.Error as e:
            self.db_connection.rollback()
            self.logger.error(f"Error whilst trying to create a new user! {e}")
            raise

    def login(self, username, plain_password):
        """
        Authenticates a user by their username and password.

        Args:
            username: The user's username
            plain_password: The user's (unhashed) password

        Returns:
            A tuple containing (True, user_id) if authentication is successful, or 
            (False, None) if authentication fails.

        Raises:
            psycopg2.Error: If there is an error executing database operations.
        """
        try:
            with self.db_connection.cursor() as cursor:
                # Query to get the user's hashed password and user_id from the database
                query = """
                SELECT user_id, password FROM public."Users" WHERE username = %s;
                """
                cursor.execute(query, (username,))
                result = cursor.fetchone()

                # If user is not found or password does not match
                if result is None or not bcrypt.checkpw(plain_password.encode('utf-8'), result[1].encode('utf-8')):
                    self.logger.warning(f"User {username} was not found, or the password did not match")
                    return False, None

                # If the user is found and password matches
                return True, result[0]

        except psycopg2.Error as e:
            self.db_connection.rollback()
            self.logger.error(f"Error during login: {e}")
            raise
    
    def change_password(self, user_id, password, new_password):
        """
        Changes the user's password.

        Args:
            user_id: The user's ID
            password: The user's current password
            new_password: The user's new password

        Returns:
            True if the password change was successful, False otherwise.

        Raises:
            psycopg2.Error: If there is an error executing database operations.
        """
        try:
            with self.db_connection.cursor() as cursor:
                # Query to get the user's hashed password from the database
                query = """
                SELECT password FROM public."Users" WHERE user_id = %s;
                """
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()

                # If user is not found or password does not match
                if result is None or not bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
                    self.logger.warning(f"User {user_id} was not found, or the password did not match")
                    return False

                # Hash the new password using bcrypt
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

                # Update the user's password in the database
                update_query = """
                UPDATE public."Users" SET password = %s WHERE user_id = %s;
                """
                cursor.execute(update_query, (hashed_password.decode('utf-8'), user_id))
                self.db_connection.commit()
                return True

        except psycopg2.Error as e:
            self.db_connection.rollback()
            self.logger.error(f"Error during password change: {e}")
            raise
    
    def delete_user(self, user_id):
        """
        Deletes a user from the database.

        Args:
            user_id: The user's ID

        Returns:
            True if the user was successfully deleted, False otherwise.

        Raises:
            psycopg2.Error: If there is an error executing database operations.
        """
        try:
            with self.db_connection.cursor() as cursor:
                # Delete the user from the database
                tables = ["Budget", "Category", "Expense", "Users"]
                for table in tables:
                    query = f"""
                    DELETE FROM public."{table}" WHERE user_id = %s;
                    """
                    cursor.execute(query, (user_id,))
               
                self.db_connection.commit()
                return True

        except psycopg2.Error as e:
            self.db_connection.rollback()
            self.logger.error(f"Error during user deletion: {e}")
            raise
    
    def update_email(self, new_email, user_id):
        """
        Updates the user's email address.

        Args:
            new_email: The user's new email address

        Returns:
            True if the email address was successfully updated, False otherwise.

        Raises:
            psycopg2.Error: If there is an error executing database operations.
        """
        try:
            with self.db_connection.cursor() as cursor:
                # Update the user's email address in the database
                query = """
                UPDATE public."Users" SET email = %s WHERE user_id = %s;
                """
                cursor.execute(query, (new_email, user_id))
                self.db_connection.commit()
                return True

        except psycopg2.Error as e:
            self.db_connection.rollback()
            self.logger.error(f"Error during email update: {e}")
            raise
