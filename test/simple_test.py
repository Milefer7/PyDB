import json
import unittest
from storage.engine import DatabaseManager
from sql_core.compiler import SqlLexer
from sql_core.compiler import SqlParser


class TestSqlExecution(unittest.TestCase):
    def setUp(self):
        """
        这里可以初始化数据库连接，清空表格等。
        """
        self.db = DatabaseManager()  # 实例化数据库管理器
        self.lexer = SqlLexer()  # 实例化词法分析器
        self.parser = SqlParser(self.db)  # 实例化语法分析器

    def run_sql(self, user_input):
        """
        运行 SQL 语句并返回结果
        """
        tokens = self.lexer.tokenize(user_input)
        # 打印每个 token 的信息
        # for token in tokens:
        #     print(f"Type: {token.type}, Value: {token.value}")
        parser_tree = self.parser.parse(tokens)
        return parser_tree

    # **********************************************************************************************
    # **********************************************************************************************
    # 验证表删除是否成功
    def test_drop_table(self):
        user_input = 'DELETE FROM employees;'
        result = self.run_sql(user_input)
        self.assertIsNotNone(result)
        print("删除表")
        # 输出json格式化的结果
        print(json.dumps(result, indent=2))

    # 验证选择 db 是否成功
    def test_use_database(self):
        user_input = 'USE test_db;'
        result = self.run_sql(user_input)
        self.assertIsNotNone(result)
        print("选择数据库")
        print(json.dumps(result, indent=2))

    # 验证 db 创建是否成功
    def test_create_database(self):
        user_input = 'CREATE DATABASE test_db;'
        result = self.run_sql(user_input)
        self.assertIsNotNone(result)
        print("创建数据库")
        print(json.dumps(result, indent=2))

    # 验证 db 展示是否成功
    def test_show_databases(self):
        user_input = 'SHOW DATABASES;'
        result = self.run_sql(user_input)
        self.assertIsNotNone(result)
        print("展示数据库")
        print(json.dumps(result, indent=2))

    # **********************************************************************************************
    # **********************************************************************************************
    # 验证 table 创建是否成功
    def test_create_table(self):
        user_input = """
        CREATE TABLE employees (
            id INT PRIMARY KEY NOT NULL,
            name VARCHAR(100) NOT NULL,
            salary DECIMAL(10, 2),
            department VARCHAR(50)
        );
        """
        result = self.run_sql(user_input)
        self.assertIsNotNone(result)
        print(json.dumps(result, indent=2))

    # **********************************************************************************************
    # **********************************************************************************************

    # 验证数据是否成功插入
    def test_insert_data3(self):
        user_input = '''
        INSERT INTO employees (id, name, salary, department) VALUES
        (1, 'John Doe', 55000.00, 'Engineering'),
        (2, 'Alice Johnson', 72000.00, 'Marketing'),
        (3, 'Bob Smith', 64000.00, 'Engineering');
        '''
        result = self.run_sql(user_input)
        self.assertIsNotNone(result)
        print("插入数据")
        print(json.dumps(result, indent=2))

    def test_insert_data1000(self):
        user_input = '''
           INSERT INTO employees (id, name, salary, department) VALUES
            (1, 'Juan Hutchinson', 73494.76, 'HR'),
            (2, 'Michael Cooper', 75228.07, 'Marketing'),
            (3, 'Carrie May', 64503.72, 'Marketing'),
            (4, 'Nicholas Jones', 90960.78, 'Marketing'),
            (5, 'Anna Richardson', 65515.56, 'Marketing'),
            (6, 'Ashley Lopez', 89399.73, 'HR'),
            (7, 'Gina Lewis', 73588.83, 'Finance'),
            (8, 'Lisa Chavez', 76849.2, 'Finance'),
            (9, 'Juan Charles', 81424.61, 'Engineering'),
            (10, 'Bradley Hopkins', 52115.2, 'Engineering'),
            (11, 'Kathleen Brown', 66012.12, 'Marketing'),
            (12, 'Jeffrey Kelley', 99894.65, 'Marketing'),
            (13, 'Joseph Clark', 99521.74, 'Marketing'),
            (14, 'Joseph Casey', 94200.48, 'Engineering'),
            (15, 'Sherry Lopez', 80146.19, 'Marketing'),
            (16, 'Michelle Davis', 86675.74, 'Finance'),
            (17, 'Michael Horne', 87162.58, 'Finance'),
            (18, 'Paul Perez', 97086.6, 'Marketing'),
            (19, 'Bobby Hayes', 65787.95, 'Finance'),
            (20, 'David Carey', 99151.03, 'Finance'),
        '''
        result = self.run_sql(user_input)
        self.assertIsNotNone(result)
        print("Inserted 20 rows")


    # SELECT ALL
    def test_select_all(self):
        user_input = '''
            SELECT * FROM employees;
            '''
        result = self.run_sql(user_input)
        self.assertIsNotNone(result)
        print(json.dumps(result, indent=2))

    # simple SELECT
    def test_select(self):
        user_input = '''
            SELECT name, salary FROM employees;
            '''
        result = self.run_sql(user_input)
        self.assertIsNotNone(result)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    unittest.main()
