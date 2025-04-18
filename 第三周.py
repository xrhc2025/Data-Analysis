# CREATE DATABASE IF NOT EXISTS douban_movie_db;
# USE douban_movie_db;
#
# CREATE TABLE IF NOT EXISTS movies (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     title VARCHAR(255) NOT NULL,
#     rating DECIMAL(3, 1), -- 例如：9.5
#     cover_url VARCHAR(1024), -- 封面图片的URL
#     details_url VARCHAR(1024), -- 详情页URL
#     year INT, -- 上映年份
#     directors TEXT, -- 导演，考虑到可能有多个导演，使用TEXT类型
#     casts TEXT, -- 主演，同样使用TEXT类型处理多个演员的情况
#     genres TEXT, -- 类型，比如剧情、喜剧等
#     countries TEXT -- 制片国家/地区
# );




import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error

def fetch_douban_top250():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    movie_list = []
    for start in range(0, 100, 25):  # 每页25部电影，总共获取前100部
        url = f"https://movie.douban.com/top250?start={start}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='item')
        for item in items:
            title = item.find('span', class_='title').text
            rating = float(item.find('span', class_='rating_num').text)
            cover_url = item.find('img')['src']
            details_url = item.find('a')['href']
            info = item.find('p').text.strip().split('\n')
            year = int(info[1].strip().split('/')[-1])
            directors_casts_countries_genres = info[0].strip()
            directors, casts, genres, countries = parse_directors_casts_genres_countries(directors_casts_countries_genres)
            movie_list.append((title, rating, cover_url, details_url, year, directors, casts, genres, countries))
    return movie_list

def parse_directors_casts_genres_countries(text):
    # 这里需要根据实际内容解析出导演、演员、类型和地区
    # 示例仅为演示，具体逻辑需根据页面实际情况调整
    directors = "示例导演"
    casts = "示例演员"
    genres = "示例类型"
    countries = "示例地区"
    return directors, casts, genres, countries

class MySqlHelper:
    def __init__(self, host='localhost', database='douban_movie_db', user='root', password='your_password'):
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
        query = """INSERT INTO movies (title, rating, cover_url, details_url, year, directors, casts, genres, countries) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.executemany(query, data)
        self.connection.commit()

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

# 获取数据
movies = fetch_douban_top250()

# 存储数据到数据库
if movies:
    helper = MySqlHelper(password='your_real_password_here')
    helper.store_data(movies)
    helper.close_connection()