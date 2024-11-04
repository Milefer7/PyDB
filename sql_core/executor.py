import os
import pandas as pd
from transaction import log


class DatabaseManager:
    def __init__(self):
        self.root_dir = 'database'
        self.database_name = None
        self.database_path = None
        self.log_path = None

    @staticmethod
    def dbm_show_database():
        try:
            root_dir = 'database'
            if not os.path.exists(root_dir):
                print('No database exists')
            else:
                databases = []
                for item in os.listdir(root_dir):
                    path = os.path.join(root_dir, item)
                    if os.path.isdir(path):
                        databases.append(item)
                if databases:
                    print(f"databases: {databases}")
                else:
                    print("databases are none.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def dbm_create_database(sql_tree):
        database_name = sql_tree.get("database_name")
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
            else:
                print(f"Database '{database_name}' already exists")
        except Exception as e:
            print(f"An error occurred while creating the database: {e}")

    def dbm_select_database(self, database_name):
        self.database_name = database_name
        self.database_path = os.path.join(self.root_dir, database_name)
        self.log_path = os.path.join(self.database_path, 'log.txt')

        print(f"Database Name: {self.database_name}")
        print(f"Database Path: {self.database_path}")
        print(f"Log Path: {self.log_path}")

    def dbm_use_database(self, sql_tree):
        self.database_name = sql_tree.get("database_name")
        self.database_path = os.path.join(self.root_dir, self.database_name)
        self.log_path = os.path.join(self.database_path, 'log.txt')

        # print(f"Database Name: {self.database_name}")
        # print(f"Database Path: {self.database_path}")
        # print(f"Log Path: {self.log_path}")

        print("Database changed")

    def dbm_create_table(self, sql_tree):
        table_name = sql_tree.get("table_name")
        columns = sql_tree.get("columns")
        data = []
        for column in columns:
            name = column.get("name")
            # data_type = column.get("data_type")
            # constraints = column.get("constraints")
            data.append(name)
        print(data)

        df = pd.DataFrame(data)
        print(self.database_path + table_name)
        file_path = os.path.join(self.database_path, table_name)
        # 将数据存储为 CSV 文件
        df.to_csv(f"{file_path}.csv", index=False)



