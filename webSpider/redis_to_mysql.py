import redis
import pymysql
import json

redis_connection = redis.Redis(host='127.0.0.1', port= 6379, db= 0) # 连接redis数据库
mysql_connection = pymysql.connect(host='localhost', user='root', password='123456', database='ssm_test') # 连接mysql数据库

cursor = mysql_connection.cursor() # 创建游标
# print(redis_connection)
# print(mysql_connection)

redis_keys = redis_connection.keys() # 获取redis数据库内所有键
for item in redis_keys:
    key_str = item.decode()
    if ':items' in key_str:
        while redis_connection.exists(key_str): # 判断键是否存在
            key, value = redis_connection.blpop([key_str])
            data = json.loads(value)
            print("****************************************")
            print(data['id'])
            print(data['title'])
            print(data['content'])
            print(data['url'])
            print(data['date'])
            print("****************************************")
            if(data['title']==None or len(data['title'])==0 or len(data['date'])==0 or len(data['content'])==0):
                continue
            cursor.execute("INSERT INTO news(id, title, content, url, date) VALUES(%s, %s, %s, %s, %s)", (data['id'], data['title'], data['content'], data['url'], data['date']))
        # data = json.loads(value)

# while redis_connection.exists('test:items'):
#     key, value = redis_connection.blpop(['test:items'])
#     data = json.loads(value)
# key, value = redis_connection.blpop(['test:items'])
# data = json.loads(value)



mysql_connection.commit() # 提交数据
    



redis_connection.close()
mysql_connection.close() # 释放资源