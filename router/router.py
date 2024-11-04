import json
from sql_core.executor import *


def router(sql_tree, db):
    print(json.dumps(sql_tree, indent=2))
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
            pass
        case "select_data":
            pass
