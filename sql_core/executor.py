import os
import pandas as pd
from transaction import log
from utils.util import *
import json


class DatabaseManager:
    def __init__(self):
        self.root_dir = 'database'
        self.database_name = None
        self.database_path = None
        self.log_path = None

    @staticmethod
    @timeit
    def dbm_show_database():
        try:
            root_dir = 'database'
            if not os.path.exists(root_dir):
                print('No database exists', end='')
            else:
                databases = []
                for item in os.listdir(root_dir):
                    path = os.path.join(root_dir, item)
                    if os.path.isdir(path):
                        databases.append(item)
                if databases:
                    print(f"databases: {databases}", end='')
                else:
                    print("databases are none.", end='')
        except Exception as e:
            print(f"An error occurred: {e}", end='')

    @staticmethod
    @timeit
    def dbm_create_database(sql_tree):
        database_name = sql_tree.get("database_name")
        try:
            # 如果根目录下database文件夹不存在，创建一个
            root_dir = 'database'
            if not os.path.exists(root_dir):
                os.makedirs(root_dir)
                print(f"Created root directory: {root_dir}", end='')

            database_path = os.path.join(root_dir, database_name)
            if not os.path.exists(database_path):
                os.makedirs(database_path)
                print(f"Database '{database_name}' created at: {database_path}", end='')
                # 初始化日志
                log.init_log(database_path)
            else:
                print(f"Database '{database_name}' already exists", end='')
        except Exception as e:
            print(f"An error occurred while creating the database: {e}", end='')

    @timeit
    def dbm_use_database(self, sql_tree):
        self.database_name = sql_tree.get("database_name")
        self.database_path = os.path.join(self.root_dir, self.database_name)
        self.log_path = os.path.join(self.database_path, 'log.txt')

        # print(f"Database Name: {self.database_name}")
        # print(f"Database Path: {self.database_path}")
        # print(f"Log Path: {self.log_path}")

        print("Database changed", end='')

    @timeit
    def dbm_create_table(self, sql_tree):
        # print(json.dumps(sql_tree, indent=2))
        try:
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
            schema_table_name = f"{table_name}_schema"

            schema_file_path = os.path.join(self.database_path, schema_table_name)
            # 将约束存储为 CSV 文件
            schema_df.to_csv(f"{schema_file_path}.csv", index=False)

            # 表数据
            data_df = pd.DataFrame(columns=[col['name'] for col in schema])
            data_file_path = os.path.join(self.database_path, table_name)
            data_df.to_csv(f"{data_file_path}.csv", index=False)

            print("Table created successfully.", end='')

        except Exception as e:
            print(f"An error occurred: {e}", end='')

    @timeit
    def dbm_insert_data(self, sql_tree):
        try:
            table_name = sql_tree.get("table_name")
            schema_table_name = f"{table_name}_schema"

            # 读取数据结构定义文件
            path_table_schema = f"{os.path.join(self.database_path, schema_table_name)}.csv"
            # print(path_table_schema)
            with open(path_table_schema) as f:
                schema = pd.read_csv(path_table_schema)

            # column_order = [col["name"] for col in schema["name"]]
            # primary_key = next((col["name"] for col in schema["columns"] if col.get("primary_key")), None)
            # nullable_columns = {col["name"]: col["nullable"] for col in schema["columns"]}

            # 对数据的处理
            columns = sql_tree["columns"]
            values = sql_tree["insert_clause"]["values"]
            new_data = pd.DataFrame(values, columns=columns)
            row_count = len(new_data)

            # data_file_path 是 CSV 数据文件的路径
            data_file_path = os.path.join(self.database_path, f"{table_name}.csv")

            # 将 new_data 追加到现有的 CSV 文件中
            new_data.to_csv(data_file_path, mode='a', header=False, index=False)

            print(f"Query OK, {row_count} row affected", end='')
        except Exception as e:
            print(f"An error occurred: {e}", end='')

# if __name__ == '__main__':
#     # tree = """
#     # {
#     #     "type": "insert_data",
#     #     "table_name": "students",
#     #     "columns": [
#     #         "name",
#     #         "age",
#     #         "major"
#     #     ],
#     #     "insert_clause": {
#     #         "insert_type": "values",
#     #         "values": [
#     #             [
#     #                 "Bob",
#     #                 "22",
#     #                 "Mathematics"
#     #             ],
#     #             [
#     #                 "Charlie",
#     #                 "19",
#     #                 "Physics"
#     #             ]
#     #         ]
#     #     }
#     # }
#     # """
#     tree = '''
#     CREATE TABLE employees (id INT PRIMARY KEY NOT NULL, name VARCHAR(100) NOT NULL,salary DECIMAL(10, 2),department VARCHAR(50));
#     '''
#
#     db = DatabaseManager()
#     db.database_name = 'geek'
#     db.database_path = 'database\geek'
#     db.dbm_create_table(json.loads(tree))
#     # db.dbm_insert_data(json.loads(tree))
