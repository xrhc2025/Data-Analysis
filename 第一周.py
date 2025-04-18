import mysql.connector
from mysql.connector import Error


class MySqlHelper:
    def __init__(self, host='localhost', database='school', user='root', password=''):
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            if self.connection.is_connected():
                print("Successfully connected to MySQL database")
        except Error as e:
            print(f"Error: {e}")

    def execute_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"Error: {e}")

    def fetch_data(self, query):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error: {e}")

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")



helper = MySqlHelper(password='your_password')
helper.execute_query("INSERT INTO students (name, height) VALUES ('李四', 170.0)")
print(helper.fetch_data("SELECT * FROM students"))
helper.close_connection()