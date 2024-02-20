import psycopg2

def get_db_connection():
    connection = psycopg2.connect(
        dbname="expensease",
        user="erdit",
        password="2002",
        host="localhost" 
    )
    return connection