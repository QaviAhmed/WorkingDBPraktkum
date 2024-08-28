import mariadb
from mariadb import ConnectionPool
from typing import Callable, Any
import json

# making the basic structure for the MariaDB connector 
# logic from connecting to the db to the creating db
# as well as the tables further all the query logic

class DBManager:

    def __init__(self, poolName, poolSize, poolResetSession, host, dbName, port, user, password):
        self.connection_pool = ConnectionPool(
            pool_name=poolName,
            pool_size=poolSize,
            pool_reset_connection=poolResetSession,  # Note: reset session is slightly different in MariaDB
            host=host,
            user=user,
            password=password,
            port=int(port),  # Ensure port is passed as an integer
            ssl=False
        )
        self.__create_db_if_not_exists(dbName)
        self.connection_pool.close()
        
        self.connection_pool = ConnectionPool(
            pool_name=poolName,
            pool_size=poolSize,
            pool_reset_connection=poolResetSession,  # Note: reset session is slightly different in MariaDB
            host=host,
            user=user,
            password=password,
            port=int(port),  # Ensure port is passed as an integer
            database=dbName,
            ssl=False
        )
        
    def __create_db_if_not_exists(self, dbName):
        connection_obj = self.connection_pool.get_connection()
        try:
            cursor = connection_obj.cursor()
            cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = ?", (dbName,))
            record = cursor.fetchone()
            print(record)
            if record:
                print(f"The database '{dbName}' already exists. Skipping creation!")
                return True
            else:
                createDBQuery = f"CREATE DATABASE {dbName}"
                cursor.execute(createDBQuery)
                print(f"Database: {dbName} created successfully")
        except mariadb.Error as err:
            print("Error: ", err)
        finally:
            if cursor:
                cursor.close()
            if connection_obj:
                connection_obj.close()

    def execute_query(self, operation: str, *args: Any):
        if "SELECT" not in operation:
            connection_obj = self.connection_pool.get_connection()
            try:
                cursor = connection_obj.cursor()
                cursor.execute(operation)
                connection_obj.commit()
            except mariadb.Error as err:
                print(err)
            finally:
                if cursor:
                    cursor.close()
                if connection_obj:
                    connection_obj.close()
        elif "INSERT" in operation:
            connection_obj = self.connection_pool.get_connection()
            try:
                cursor = connection_obj.cursor()
                cursor.execute(operation, *args)
                connection_obj.commit()
            except mariadb.Error as err:
                print(err)
            finally:
                if cursor:
                    cursor.close()
                if connection_obj:
                    connection_obj.close()
        else:
            return "Get query does not work with execute_query use get_query instead!"
    
    @staticmethod 
    def __get_query(func: Callable) -> Callable:
        def wrapper(self: Any, operation: str, *args):
            if "SELECT" in operation:
                connection_obj = self.connection_pool.get_connection()
                try:
                    cursor = connection_obj.cursor()
                    cursor.execute(operation, args)
                    result = func(cursor)
                    return result
                except mariadb.Error as err:
                    print(err)
                finally:
                    if cursor:
                        cursor.close()
                    if connection_obj:
                        connection_obj.close()
            else:
                return "This query does not work with get_query; use execute_query instead!"
        return wrapper

    @__get_query
    def fetch_all(cursor, *args):
        columns = [col[0] for col in cursor.description]
        return cursor.fetchall()

    @__get_query
    def fetch_one(cursor, *args):
        columns = [col[0] for col in cursor.description]
        return cursor.fetchone()

    @__get_query
    def fetch_many(cursor, n, *args):
        columns = [col[0] for col in cursor.description]
        return cursor.fetchmany(n)
    
    def run_sql_script(self, sql_file_path):
        with open(sql_file_path, 'r') as file:
            sql_script = file.read()

            # Split the script into individual SQL statements
            sql_commands = sql_script.split(';')

            for command in sql_commands:
                command = command.strip()
                if command:  # Avoid empty commands
                    self.execute_query(command)
                    print(f"Executed command: {command}")
        print("All commands executed successfully.")

# creating the connections
db_manager = DBManager(
    poolName="shoeshop_pool",
    poolSize=5,
    poolResetSession=True,
    host="shoeyou.local",
    user="db_main",
    password="dbteamd",
    dbName="db_shoeyou",
    port="3307"
)
db_manager.run_sql_script("/Users/qavi/Desktop/SS24/DB_Praktikum/WorkingDBPraktkum/table_script.sql")
db_manager.run_sql_script("/Users/qavi/Desktop/SS24/DB_Praktikum/WorkingDBPraktkum/triggers_script.sql")
db_manager.run_sql_script("/Users/qavi/Desktop/SS24/DB_Praktikum/WorkingDBPraktkum/indices_script.sql")
db_manager.run_sql_script("/Users/qavi/Desktop/SS24/DB_Praktikum/WorkingDBPraktkum/creation_script.sql")
# Example of creating tables and inserting data
# db_manager.execute_query("""CREATE TABLE IF NOT EXISTS newsletter 
#                            (id INT AUTO_INCREMENT,
#                            email VARCHAR(255) NOT NULL UNIQUE, PRIMARY KEY (id))""")
#
# db_manager.execute_query("""CREATE TABLE IF NOT EXISTS projects 
#                           (id INT AUTO_INCREMENT,project_name 
#                            VARCHAR(255) UNIQUE,description TEXT, promo_video TEXT, PRIMARY KEY (id))""")
#
# with open('/Users/qavi/Desktop/projects/DummyData/Json/newsletterData.json', 'r') as newsletterData:
#     data = json.load(newsletterData)
#     for email_data in data['emails']:
#          db_manager.execute_query("""
#          INSERT INTO newsletter (email)
#                    VALUES (?)
#          """, email_data['email'])