import os
from transaction import log


def executor_create_database(database_name):
    try:
        # 如果根目录下database文件夹不存在，创建一个
        root_dir = 'database'
        if not os.path.exists(root_dir):
            os.makedirs(root_dir)
            print(f"Created root directory: {root_dir}")

        database_path = os.path.join(root_dir, database_name)
        if not os.path.exists(database_path):
            os.makedirs(database_path)
            print(f"Database '{database_name}' created at: {database_path}")

        # 初始化日志
        log.init_log(database_path)
    except Exception as e:
        print(f"An error occurred while creating the database: {e}")




