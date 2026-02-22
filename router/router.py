from storage.engine import *
from utils.util import *


def myRouter(sql_tree, db):
    # 打印精美的 AST，方便你在调试时查看生成的树结构
    # print("解析生成的 AST 树: ")
    # print(json.dumps(sql_tree, indent=2))
    
    if not sql_tree:
        return

    sql_type = sql_tree.get("type")

    # 使用 match-case 匹配标准化的 sql_type
    match sql_type:
        # ==========================================
        # 1. DDL: 数据库级别的操作 (无需选中数据库)
        # ==========================================
        case "show_databases":
            DatabaseManager.dbm_show_database()
            
        case "create_database":
            DatabaseManager.dbm_create_database(sql_tree)
            
        case "drop_database":
            # 论文点：新增的删库功能路由
            DatabaseManager.dbm_drop_database(sql_tree)
            
        case "use_database":
            db.dbm_use_database(sql_tree)

        # ==========================================
        # 2. DDL: 表级别的操作 (必须先选中数据库)
        # ==========================================
        case "create_table":
            if db.database_name is None:
                print("Error: No database selected. Please use 'USE <database_name>' first.")
            else:
                db.dbm_create_table(sql_tree)
                
        case "drop_table":
            if db.database_name is None:
                print("Error: No database selected.")
            elif not find_table(sql_tree.get("table_name"), db.database_path):
                print(f"Error: Table '{sql_tree.get('table_name')}' does not exist.")
            else:
                db.dbm_drop_table(sql_tree)

        # ==========================================
        # 3. DML: 增删改操作
        # ==========================================
        case "insert" | "update" | "delete":
            # 💡 修改：将同类型校验合并，因为新版AST中它们的表名都在第一层的 "table_name"
            if db.database_name is None:
                print("Error: No database selected.")
                return
                
            table_name = sql_tree.get("table_name")
            if not find_table(table_name, db.database_path):
                print(f"Error: Table '{table_name}' does not exist.")
                return
                
            # 根据具体类型分发到具体的执行器引擎
            if sql_type == "insert":
                db.dbm_insert_data(sql_tree)
            elif sql_type == "update":
                db.dbm_update_data(sql_tree)
            elif sql_type == "delete":
                db.dbm_delete_data(sql_tree)

        # ==========================================
        # 4. DQL: 查询操作 (大一统流水线入口)
        # ==========================================
        case "select":
            if db.database_name is None:
                print("Error: No database selected.")
                return
                
            # 新版 AST 的表名在 table_source 字典里的 table 键中
            table_name = sql_tree.get("table_source").get("table")
            if not find_table(table_name, db.database_path):
                print(f"Error: Table '{table_name}' does not exist.")
                return
                
            # 💡 亮点：不再区分 select_all 还是 simple_select
            # 将整棵树 (AST) 原封不动地交给 Pandas 执行引擎，由它按流水线解析
            db.dbm_select_data(sql_tree)

        # ==========================================
        # 5. 未知兜底
        # ==========================================
        case _:
            print(f"Error: Unsupported SQL operation type '{sql_type}'.")