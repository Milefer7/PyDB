from storage.engine import *
from utils.util import *


def router(sql_tree, db):
    # print(json.dumps(sql_tree, indent=2))
    sql_type = sql_tree.get("type")
    # print(sql_type)

    # 使用 match-case 匹配 sql_type
    match sql_type:
        case "use_database":
            db.dbm_use_database(sql_tree)
        case "create_database":
            DatabaseManager.dbm_create_database(sql_tree)
        case "show_databases":
            DatabaseManager.dbm_show_database()
        case "create_table":
            if db.database_name is None:
                print("error: No database selected")
            else:
                db.dbm_create_table(sql_tree)
        case "insert_data":
            if db.database_name is None:
                print("error: No database selected")
            elif not find_table(sql_tree.get("table_name"), db.database_path):
                print("error: Table isn't created")
            else:
                db.dbm_insert_data(sql_tree)
        case "select_data":
            if db.database_name is None:
                print("error: No database selected")
            elif not find_table(sql_tree.get("select_info").get("table_name"), db.database_path):
                print("error: Table isn't created")
            else:
                select_type = sql_tree.get("select_info").get("select_type")
                match select_type:
                    case "select_all":
                        db.dbm_select_all_data(sql_tree)
                    case "simple_select":
                        db.dbm_simple_select_data(sql_tree)
        case "delete_data":
            if db.database_name is None:
                print("error: No database selected")
            elif not find_table(sql_tree.get("delete_clause").get("table_name"), db.database_path):
                print("error: Table doesn't exist")
            else:
                db.dbm_delete_data(sql_tree)
