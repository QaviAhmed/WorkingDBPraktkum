import mariadb
import sys

def connecting_mariadb():
    try:
        connection = mariadb.connect(user="root",password="root", host="localhost", database="test")
        cur = connection.cursor()

    except mariadb.Error as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)


    if cur:
        employees = []
        cur.execute("""SELECT first_name,
                    last_name FROM employees""")
        
        for (first_name, last_name) in cur:
            employees.append(f"{first_name} {last_name}")
        print("\n".join(employees))    
        connection.close()
        