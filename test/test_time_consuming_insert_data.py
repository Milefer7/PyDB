import mysql.connector
import time


def insert_data_mysql(data):
    # 连接到MySQL数据库
    connection = mysql.connector.connect(
        host="localhost",  # MySQL服务器地址
        user="root",  # 用户名
        password="password",  # 密码
        database="test_db"  # 目标数据库
    )

    cursor = connection.cursor()

    start_time = time.time()  # 记录开始时间

    # 执行批量插入操作
    insert_query = "INSERT INTO employees (name, salary, department) VALUES (%s, %s, %s)"
    cursor.executemany(insert_query, data)

    connection.commit()  # 提交事务

    end_time = time.time()  # 记录结束时间

    cursor.close()
    connection.close()

    return end_time - start_time  # 返回插入时间


# 测试数据
data = [("name1", 1000, "IT"), ("name2", 1200, "HR"), ("name3", 1500, "Finance")]

# 测试插入
time_taken = insert_data_mysql(data)
print(f"MySQL插入数据时间: {time_taken}秒")
