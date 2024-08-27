import unittest
from db_model import DBManager
import mariadb

class TestDBConnection(unittest.TestCase):

    def setUp(self):
        # Set up the DBManager instance for testing
        self.db_manager = DBManager(
            poolName="test_pool",
            poolSize=1,  # Use a small pool size for testing
            poolResetSession=True,
            host="shoeyou.local",
            user="db_main",
            password="dbteamd",
            dbName="db_shoeyou",
            port="3307",
        )


    def test_db_connection(self):
        # Attempt to get a connection from the pool
        try:
            connection = self.db_manager.connection_pool.get_connection()
            self.assertIsNotNone(connection, "Failed to acquire a connection from the pool")
        except mariadb.Error as err:
            self.fail(f"Database connection failed with error: {err}")
        finally:
            if connection:
                connection.close()

    def tearDown(self):
        # Optionally, close the connection pool
        self.db_manager.connection_pool.close()
