# 变成总经理(Facade)，统筹上面三个小弟
# 注意这里的导入路径适配了你的项目结构
from storage.metadata import MetadataManager
from storage.validator import Validator
from storage.executor import Executor
from utils.util import timeit

class DatabaseManager:
    def __init__(self):
        # 实例化元数据管家
        self.metadata = MetadataManager()

    @property
    def database_name(self): return self.metadata.database_name
    @property
    def database_path(self): return self.metadata.database_path

    @staticmethod
    @timeit
    def dbm_show_database(): 
        MetadataManager().show_databases()

    @staticmethod
    @timeit
    def dbm_create_database(sql_tree): 
        MetadataManager().create_database(sql_tree.get("database_name"))

    @staticmethod
    @timeit
    def dbm_drop_database(sql_tree): 
        MetadataManager().drop_database(sql_tree.get("database_name"))

    @timeit
    def dbm_use_database(self, sql_tree): 
        self.metadata.use_database(sql_tree.get("database_name"))

    @timeit
    def dbm_create_table(self, sql_tree): 
        self.metadata.create_table(sql_tree)

    @timeit
    def dbm_drop_table(self, sql_tree): 
        self.metadata.drop_table(sql_tree)

    # 核心 DML：三层协作
    @timeit
    def dbm_insert_data(self, sql_tree):
        table_name = sql_tree.get("table_name")

        # 1. 向 Metadata 要数据
        schema_df = self.metadata.load_schema(table_name)
        existing_df = self.metadata.load_table(table_name)
        
        # 2. 交给 Validator 拦截
        is_valid, full_new_df = Validator.validate_insert(
            sql_tree.get("columns"), sql_tree.get("values"), 
            schema_df, existing_df, Executor.eval_value
        ) # 如果有错，这里直接就爆炸了（带着 ValueError 飞到 client.py）如果能走过这一行，说明一定 is_valid，不需要再做 if not is_valid 判断了！
            
        # 3. 交给 Metadata 落盘
        full_new_df.to_csv(self.metadata.get_table_path(table_name), mode='a', header=False, index=False)
        print(f"Query OK, {len(full_new_df)} row(s) affected.", end='')

    @timeit
    def dbm_delete_data(self, sql_tree):
        table_name = sql_tree.get("table_name")
        df = self.metadata.load_table(table_name)
        # 交给 Executor 执行删除
        new_df = Executor.execute_delete(df, sql_tree.get("where"))
        new_df.to_csv(self.metadata.get_table_path(table_name), index=False)
        print(f"Query OK, {len(df) - len(new_df)} row(s) deleted.", end='')

    @timeit
    def dbm_update_data(self, sql_tree):
        table_name = sql_tree.get("table_name")
        
        # 1. 向 Metadata 要数据 (只读文件，不计算)
        df = self.metadata.load_table(table_name)
        
        # 2. 交给 Executor 执行核心计算 (只算账，不碰文件)
        new_df, affected = Executor.execute_update(df, sql_tree.get("assignments"), sql_tree.get("where"))
        
        # 3. 再次交给 Metadata 落盘保存
        new_df.to_csv(self.metadata.get_table_path(table_name), index=False)
        
        print(f"Query OK, {affected} row(s) updated.", end='')

    @timeit
    def dbm_select_data(self, sql_tree):
        df = self.metadata.load_table(sql_tree.get("table_source").get("table"))
        current_db_path = self.database_path
        # 交给 Executor 执行查询流水线并打印
        Executor.execute_select(df, sql_tree, current_db_path)