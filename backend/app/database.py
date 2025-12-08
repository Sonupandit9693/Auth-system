import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from app.config import settings

class Database():
    """
    database connection manager
    """

    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=settings.DATABASE_HOST,
                port=settings.DATABASE_PORT,
                database=settings.DATABASE_NAME,
                user=settings.DATABASE_USER,
                password=settings.DATABASE_PASSWORD,
                cursor_factory=RealDictCursor
            )

            print(f"database: conneted sucessfully")
            return self.connection
        except Exception as e:
            print(f"databae connection failed: {e}")
            raise

    def disconnect(self):
        if self.connection:
            self.connect.close()
            print(f"databse: disconnetd")

    def get_connection(self):
        if not self.connection or self.connection.closed:
            self.connect()

        return self.connection

db = Database() #TODO: global database instance

@contextmanager
def get_db_connection():
    #TODO: contex manager for database connection
    conn = db.get_connection()
    try:
        yield conn
    finally:
        pass


def get_db_cursor():
    conn = db.get_connection()
    return conn.cursor()