import os
from transaction import log


def create_database(database_name):
    try:
        # 如果根目录下database文件夹不存在，创建一个
        root_dic = 'database'
        if not os.path.exists(root_dic):
            os.makedirs(root_dic)
            print(f"Created root directory: {root_dir}")

        database_path = os.path.join(root_dir, database_name)
        if not os.path.exists(database_path):
            os.makedirs(database_path)
            print(f"Database '{database_name}' created at: {database_path}")
        log.init_log(database_path)
    except Exception as e:
        print(f"An error occurred while creating the database: {e}")
