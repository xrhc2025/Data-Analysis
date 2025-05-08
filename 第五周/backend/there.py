# CREATE DATABASE IF NOT EXISTS douban_movie_db; # 如果名为 douban_movie_db 的数据库不存在，则创建它
# USE douban_movie_db; # 选择 douban_movie_db 数据库作为当前操作的数据库
#
# CREATE TABLE IF NOT EXISTS movies ( # 如果名为 movies 的表不存在，则创建它
#     id INT AUTO_INCREMENT PRIMARY KEY, # id 字段，整数类型，自增，主键
#     title VARCHAR(255) NOT NULL, # title 字段，字符串类型，最大长度255，不能为空
#     rating DECIMAL(3, 1), -- 例如：9.5 # rating 字段，十进制数类型，总共3位数，小数点后1位
#     cover_url VARCHAR(1024), -- 封面图片的URL # cover_url 字段，字符串类型，最大长度1024，用于存储封面图片URL
#     details_url VARCHAR(1024), -- 详情页URL # details_url 字段，字符串类型，最大长度1024，用于存储详情页URL
#     year INT, -- 上映年份 # year 字段，整数类型，用于存储上映年份
#     directors TEXT, -- 导演，考虑到可能有多个导演，使用TEXT类型 # directors 字段，文本类型，用于存储导演信息
#     casts TEXT, -- 主演，同样使用TEXT类型处理多个演员的情况 # casts 字段，文本类型，用于存储主演信息
#     genres TEXT, -- 类型，比如剧情、喜剧等 # genres 字段，文本类型，用于存储电影类型
#     countries TEXT -- 制片国家/地区 # countries 字段，文本类型，用于存储制片国家/地区
# );




import requests # 导入 requests 库，用于发送HTTP请求
from bs4 import BeautifulSoup # 从 bs4 库中导入 BeautifulSoup 类，用于解析HTML文档
# import mysql.connector # 导入 mysql.connector 库，用于连接MySQL数据库
# from mysql.connector import Error # 从 mysql.connector 库中导入 Error 类，用于处理数据库错误

# 定义一个函数，用于从豆瓣Top250网站抓取电影数据
def fetch_douban_top250():
    # 定义请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.douban.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    }
    movie_list = [] # 初始化一个空列表，用于存储抓取到的电影信息
    for start in range(0, 100, 25):  # 循环抓取数据，每页25部电影，总共获取4页，即前100部电影
        url = f"https://movie.douban.com/top250?start={start}" # 构建豆瓣电影Top250的URL
        response = requests.get(url, headers=headers) # 发送GET请求获取页面内容
        soup = BeautifulSoup(response.text, 'html.parser') # 使用BeautifulSoup解析HTML内容
        items = soup.find_all('div', class_='item') # 查找所有包含电影信息的 'div' 标签，其 class 为 'item'
        print(f"找到 {len(items)} 个电影条目") # 打印找到的电影条目数量
        for item in items: # 遍历每个电影条目
            title = item.find('span', class_='title').text # 获取电影标题
            rating = float(item.find('span', class_='rating_num').text) # 获取电影评分，并转换为浮点数
            cover_url = item.find('img')['src'] # 获取电影封面图片的URL
            details_url = item.find('a')['href'] # 获取电影详情页的URL

            # 添加调试输出
            print("处理电影:", title)

            # 尝试使用不同的选择器来获取信息
            # 1. 直接查找所有p标签
            all_p_tags = item.find_all('p')
            print(f"找到 {len(all_p_tags)} 个p标签")

            # 2. 查找包含"导演:"的p标签
            p_tag = None
            for p in all_p_tags:
                # 打印每个p标签的文本内容，帮助调试
                p_text = p.get_text()
                print(f"p标签文本: {p_text[:50]}...")  # 只打印前50个字符，避免输出过长
                
                if "导演:" in p_text or "主演:" in p_text:
                    p_tag = p
                    print("找到包含导演/主演信息的p标签!")
                    break
            
            # 如果仍然没有找到包含导演/主演信息的标签，使用第一个看起来有内容的p标签
            if p_tag is None and len(all_p_tags) > 0:
                for p in all_p_tags:
                    if len(p.get_text().strip()) > 10:  # 假设内容丰富的p标签文本长度应该大于10
                        p_tag = p
                        print("使用备选p标签")
                        break
            
            # 如果所有尝试都失败，则尝试找到.bd div下的p标签
            if p_tag is None:
                bd_div = item.find('div', class_='bd')
                if bd_div:
                    p_tag = bd_div.find('p')
                    if p_tag:
                        print("从.bd div找到p标签")

            directors_str = ""
            casts_str = ""
            year_val = 0
            countries_str = ""
            genres_str = ""

            if p_tag:
                # 使用 get_text(separator='\n', strip=True) 来处理 <br> 标签并按行分割
                # strip=True 会移除每部分文本的首尾空格
                p_lines = [line.strip() for line in p_tag.get_text(separator='\n', strip=True).split('\n') if line.strip()]
                print("提取到的行:", p_lines)
                
                if len(p_lines) >= 2:
                    line1_info = p_lines[0]  # 通常是 "导演: XXX 主演: YYY"
                    line2_info = p_lines[1]  # 通常是 "YYYY / 国家 / 类型"

                    # 解析第一行：导演和主演
                    directors_str = "" #确保在每次循环开始时清空
                    casts_str = ""     #确保在每次循环开始时清空

                    if "导演:" in line1_info:
                        # temp_str 是 "导演:" 之后的所有内容
                        temp_str = line1_info.split("导演:", 1)[1]
                        if "主演:" in temp_str: # 检查 "主演:" 是否在 "导演:" 之后的部分中
                            director_part = temp_str.split("主演:", 1)[0].strip()
                        else: # "导演:" 之后没有 "主演:"，则剩余部分都是导演信息
                            director_part = temp_str.strip()
                        directors_str = ' '.join(director_part.split()) # 清理空格，并处理类似 "名 姓" 的情况

                    if "主演:" in line1_info:
                        # cast_part_full 是 "主演:" 之后的所有内容
                        # 从原始 line1_info 分割，以避免 "主演:" 出现在导演名中的罕见情况的错误解析
                        cast_part_full = line1_info.split("主演:", 1)[1].strip()
                        # 按 "/" 分割演员，并移除 "..." 标记
                        casts_list = [c.strip() for c in cast_part_full.split('/') if c.strip() and c.strip() != "..."]
                        casts_str = " / ".join(casts_list) # 用 " / " 重新连接演员列表

                    # 解析第二行：年份、国家、类型
                    line2_parts = [part.strip() for part in line2_info.split('/') if part.strip()]
                    
                    if len(line2_parts) >= 1: # 年份
                        year_text = line2_parts[0]
                        year_digits = ''.join(filter(str.isdigit, year_text))
                        if year_digits:
                            year_val = int(year_digits)
                        # else year_val remains 0

                    if len(line2_parts) >= 2: # 国家
                        countries_str = line2_parts[1]
                    
                    if len(line2_parts) >= 3: # 类型
                        # 类型部分可能是 "剧情 爱情" 或 "剧情 / 犯罪" (如果豆瓣用/分隔类型)
                        # 我们将从第三个元素开始的所有部分用 " / " 连接起来
                        genres_str = " / ".join(line2_parts[2:])

            # 将提取到的电影信息作为一个元组添加到 movie_list 中
            movie_list.append({
                'index': len(movie_list) + 1,
                'title': title,
                'rating': rating,
                'cover_url': cover_url,
                'details_url': details_url,
                'year': year_val,
                'directors': directors_str,
                'casts': casts_str,
                'genres': genres_str,
                'countries': countries_str
            })
            # print(movie_list)
    return movie_list # 返回包含所有电影信息的列表

# 定义一个名为 MySqlHelper 的类，用于封装MySQL数据库的操作
class MySqlHelper:
    # 初始化方法，当创建 MySqlHelper 对象时调用
    def __init__(self, host='localhost', database='douban_movie_db', user='root', password='your_password'):
        # 初始化connection属性
        self.connection = None
        # 调用 connect_database 方法连接数据库
        self.connect_database(host, database, user, password)

    # 定义连接数据库的方法
    def connect_database(self, host, database, user, password):
        try:
            # 尝试连接MySQL数据库
            self.connection = mysql.connector.connect(
                host=host, # 数据库主机地址
                database=database, # 数据库名称
                user=user, # 数据库用户名
                password=password # 数据库密码
            )
            # 如果连接成功
            if self.connection.is_connected():
                print("Successfully connected to MySQL database") # 打印连接成功的消息
        except Error as e: # 如果连接过程中发生错误
            print(f"Error: {e}") # 打印错误信息

    # 定义存储数据到数据库的方法
    def store_data(self, data):
        cursor = self.connection.cursor() # 创建一个游标对象，用于执行SQL语句
        # 定义插入数据的SQL语句，使用占位符 %s
        query = """INSERT INTO movies (title, rating, cover_url, details_url, year, directors, casts, genres, countries) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.executemany(query, data) # 执行SQL语句，批量插入数据
        self.connection.commit() # 提交事务，将数据写入数据库

    # 定义关闭数据库连接的方法
    def close_connection(self):
        # 如果数据库连接处于打开状态
        if self.connection.is_connected():
            self.connection.close() # 关闭数据库连接
            print("MySQL connection is closed") # 打印连接已关闭的消息

# 主程序部分
# 调用 fetch_douban_top250 函数获取电影数据
# movies = False
movies = fetch_douban_top250()

# 如果成功获取到电影数据
if movies:
    # 创建 MySqlHelper 对象，用于操作数据库
    # 注意：请将 'your_real_password_here' 替换为你的真实MySQL密码
    helper = MySqlHelper(password='your_real_password_here')
    helper.store_data(movies) # 调用 store_data 方法将电影数据存储到数据库
    helper.close_connection() # 调用 close_connection 方法关闭数据库连接