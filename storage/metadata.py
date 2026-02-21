# 专管 CSV 文件的创建、读写、删除
import os
import shutil
import pandas as pd
from transaction import log

class MetadataManager:
    def __init__(self, root_dir='database'):
        self.root_dir = root_dir
        self.database_name = None
        self.database_path = None

    def show_databases(self):
        if not os.path.exists(self.root_dir):
            print('No database exists.', end='')
            return
        databases = [item for item in os.listdir(self.root_dir) if os.path.isdir(os.path.join(self.root_dir, item))]
        print(f"Databases: {', '.join(databases)}" if databases else "No databases found.", end='')

    def create_database(self, db_name):
        if not os.path.exists(self.root_dir): os.makedirs(self.root_dir)
        db_path = os.path.join(self.root_dir, db_name)
        if not os.path.exists(db_path):
            os.makedirs(db_path)
            log.init_log(db_path)
            print(f"Query OK, 1 row affected. Database '{db_name}' created.", end='')
        else:
            print(f"Error: Database '{db_name}' already exists.", end='')

    def drop_database(self, db_name):
        db_path = os.path.join(self.root_dir, db_name)
        if os.path.exists(db_path):
            shutil.rmtree(db_path)
            print(f"Query OK. Database '{db_name}' dropped.", end='')
        else:
            print(f"Error: Database '{db_name}' does not exist.", end='')

    def use_database(self, db_name):
        # 1. 拼凑出目标数据库的物理路径
        target_db_path = os.path.join(self.root_dir, db_name)
        
        # 2. 检查该路径（数据库文件夹）是否存在
        if not os.path.exists(target_db_path):
            print(f"Error: Unknown database '{db_name}'.", end='')
            return False  # 切换失败，直接返回
            
        # 3. 校验通过，更新系统当前的上下文状态
        self.database_name = db_name
        self.database_path = target_db_path
        print(f"Database changed to '{db_name}'.", end='')
        return True

    def get_table_path(self, table_name):
        return os.path.join(self.database_path, f"{table_name}.csv")

    def get_schema_path(self, table_name):
        return os.path.join(self.database_path, f"{table_name}_schema.csv")

    def load_table(self, table_name):
        return pd.read_csv(self.get_table_path(table_name))

    def load_schema(self, table_name):
        return pd.read_csv(self.get_schema_path(table_name))

    def create_table(self, sql_tree):
        table_name = sql_tree.get("table_name")
        data_path, schema_path = self.get_table_path(table_name), self.get_schema_path(table_name)

        if os.path.exists(data_path) or os.path.exists(schema_path):
            print(f"Error: Table '{table_name}' already exists.", end='')
            return

        schema = [{"name": c.get("name"), "data_type": c.get("data_type"), 
                   "is_primary_key": 'primary key' in c.get("constraints", []),
                   "is_not_null": 'not null' in c.get("constraints", [])} for c in sql_tree.get("columns")]

        pd.DataFrame(schema).to_csv(schema_path, index=False)
        pd.DataFrame(columns=[col['name'] for col in schema]).to_csv(data_path, index=False)
        print(f"Query OK, 0 rows affected. Table '{table_name}' created.", end='')

    def drop_table(self, sql_tree):
        table_name = sql_tree.get("table_name")
        data_path, schema_path = self.get_table_path(table_name), self.get_schema_path(table_name)
        if os.path.exists(data_path): os.remove(data_path)
        if os.path.exists(schema_path): os.remove(schema_path)
        print(f"Query OK. Table '{table_name}' dropped.", end='')