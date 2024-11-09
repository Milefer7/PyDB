import os
import mysql.connector
import time
import yaml


def test_db_insert_speed(query, db_config):
    try:
        # 连接到数据库
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # 记录开始时间
        start_time = time.time()

        try:
            cursor.execute(query)  # 执行 SQL 插入语句
            connection.commit()  # 提交事务
            print("插入成功")
        except mysql.connector.Error as err:
            print(f"插入时出错: {err}")
            connection.rollback()  # 出错时回滚事务

        # 记录结束时间
        end_time = time.time()

        # 计算插入的时间
        insert_time = end_time - start_time
        print(f"插入操作耗时: {insert_time:.4f} 秒")

        # 获取插入的行数
        row_count = cursor.rowcount  # 获取影响的行数
        print(f"插入的行数: {row_count}")

    except mysql.connector.Error as err:
        print(f"数据库连接或执行时出错: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# 示例：测试数据库插入速度
if __name__ == '__main__':
    # 从配置文件加载数据库配置
    with open("../config/config.yaml", 'r') as file:
        config = yaml.safe_load(file)

    db_config = {
        'host': config['mysql']['host'],
        'user': config['mysql']['user'],
        'password': config['mysql']['password'],
        'database': config['mysql']['database']
    }

    # 打开并读取 SQL 文件
    try:
        with open("../mock/insert_1000000.sql", 'r') as file:
            # with open("../mock/insert_9000.sql", 'r') as file:
            query = file.read()
    except FileNotFoundError:
        print("SQL 文件未找到，请检查路径！")
        exit(1)

    # 测试数据库插入速度
    test_db_insert_speed(query, db_config)
