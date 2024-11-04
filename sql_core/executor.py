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
        schema = []

        for column in columns:
            name = column.get("name")
            data_type = column.get("data_type")
            constraints = column.get("constraints", [])

            # 检查是否有主键和非空约束
            is_primary_key = 'primary key' in constraints
            is_not_null = 'not null' in constraints

            # 添加每列的信息到结构数据中
            schema.append({
                "name": name,
                "data_type": data_type,
                "is_primary_key": is_primary_key,
                "is_not_null": is_not_null
            })

        # 表约束条件
        schema_df = pd.DataFrame(schema)
        schema_table_name = f"{self.database_name}_schema"

        schema_file_path = os.path.join(self.database_path, schema_table_name)
        # 将数据存储为 CSV 文件
        schema_df.to_csv(f"{schema_file_path}.csv", index=False)

        # 表数据
        data_df = pd.DataFrame(columns=[col['name'] for col in schema])
        data_file_path = os.path.join(self.database_path, self.database_name)
        data_df.to_csv(f"{data_file_path}.csv", index=False)
