import os

from transaction import log


class DatabaseManager:
    def __init__(self):
        self.root_dir = 'database'
        self.database_name = None
        self.database_path = None
        self.log_path = None

    @staticmethod
    def show_database():
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
    def create_database(database_name):
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

    def use_database(self, database_name):
        self.database_name = database_name
        self.database_path = os.path.join(self.db.root_dir, database_name)
        self.log_path = os.path.join(self.db.database_path, 'log.txt')

        print(f"Database Name: {self.db.database_name}")
        print(f"Database Path: {self.db.database_path}")
        print(f"Log Path: {self.db.log_path}")


def create_database(database_name):
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
