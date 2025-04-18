import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error


def get_baidu_top_search():
    url = 'https://top.baidu.com/board?tab=realtime'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.select('.c-single-text-ellipsis')[:10]  # Adjust the selector based on actual HTML structure
        top_searches = [item.get_text(strip=True) for item in items]
        return top_searches
    else:
        print("Failed to retrieve data")
        return []


class MySqlHelper:
    def __init__(self, host='localhost', database='your_database', user='root', password='your_password'):
        self.connect_database(host, database, user, password)

    def connect_database(self, host, database, user, password):
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

    def store_data(self, data):
        cursor = self.connection.cursor()
        query = """INSERT INTO baidu_top_search (search_term) VALUES (%s)"""
        for term in data:
            cursor.execute(query, (term,))
        self.connection.commit()

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")


# 爬取数据
top_searches = get_baidu_top_search()

# 存储数据到数据库
if top_searches:
    helper = MySqlHelper(password='your_password_here')
    helper.store_data(top_searches)
    helper.close_connection()