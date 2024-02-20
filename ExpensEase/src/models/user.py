import psycopg2
import bcrypt

class User:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def register_user(self, username, email, first_name, last_name, plain_password, pin):
        hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
        
        with self.db_connection.cursor() as cursor:
            query = """
            INSERT INTO public."Users" (username, email, first_name, last_name, password, pin)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING user_id;
            """
            cursor.execute(query, (username, email, first_name, last_name, hashed_password.decode('utf-8'), pin))
            user_id = cursor.fetchone()[0]
            self.db_connection.commit()
            return user_id