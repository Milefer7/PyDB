import unittest
import os
import sys
import pandas as pd
import json

# 将项目根目录加入到 sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 引入你的真实核心组件！
from router.router import myRouter
from sql_core.compiler import SqlLexer, SqlParser
from storage.executor import Executor
from storage.engine import DatabaseManager
from storage.metadata import MetadataManager

class TestSelectRegression(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.golden_dir = os.path.join(os.path.dirname(__file__), "golden_data")
        cls.db = DatabaseManager()  
        cls.lexer = SqlLexer()
        cls.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        cls.database_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), "database")
        
        # 🌟 3. 必须把 db 传给 Parser！否则解析器会罢工或解析错误！
        cls.parser = SqlParser(cls.db)

    def execute_and_assert(self, sql_query, expected_csv_name=None):
        # 增加这两行，让输出带上标题和 SQL
        if expected_csv_name:
            print(f"\n========== [测试项: {expected_csv_name}] ==========")
            print(f"执行 SQL: {sql_query}")
            
        tokens = self.lexer.tokenize(sql_query)
        parser_tree = self.parser.parse(tokens)
        
        if not parser_tree: return

        ast_type = parser_tree.get("type")
        current_db_path = self.db.database_path

        # 1. 专门处理 SELECT 查询
        if ast_type == "select":
            table_name = parser_tree.get("table_name")
            if not table_name:
                table_source = parser_tree.get("table_source", {})
                if isinstance(table_source, dict):
                    table_name = table_source.get("table")
            
            if not table_name:
                raise ValueError(f"无法从 AST 中解析出表名！当前 SQL: {sql_query}")

            table_file_path = os.path.join(current_db_path, f"{table_name}.csv")
            if not os.path.exists(table_file_path):
                raise FileNotFoundError(f"找不到表文件: {table_file_path}")

            df = pd.read_csv(table_file_path)
            
            # 使用 execute_select 进行查询
            result_df = Executor.execute_select(df, parser_tree, db_path=current_db_path)
            
            # 对比结果
            if expected_csv_name:
                self._compare_with_golden(result_df, expected_csv_name)
            
            return result_df

        # 2. 专门处理 UPDATE / DELETE
        elif ast_type in ["update", "delete"]:
            # 先让 Router 去真实执行，修改并保存 CSV 文件
            myRouter(parser_tree, self.db)
            
            # 执行完之后，如果需要比对答案，则读取被修改后的 CSV 文件
            if expected_csv_name:
                table_name = parser_tree.get("table_name")
                table_file_path = os.path.join(current_db_path, f"{table_name}.csv")
                
                # 读取修改后落盘的文件
                result_df = pd.read_csv(table_file_path)
                self._compare_with_golden(result_df, expected_csv_name)
                
            return None

        # 3. 处理 CREATE, INSERT, USE 等其他语句
        else:
            myRouter(parser_tree, self.db)
            return None

    # 为了代码整洁，把对比逻辑单独抽出来成一个小方法
    def _compare_with_golden(self, result_df, expected_csv_name):
        golden_path = os.path.join(self.golden_dir, expected_csv_name)
        self.assertTrue(os.path.exists(golden_path), f"找不到标准答案文件: {expected_csv_name}")
        
        expected_df = pd.read_csv(golden_path)
        
        # 矩阵级对齐比对
        pd.testing.assert_frame_equal(
            result_df.reset_index(drop=True), 
            expected_df.reset_index(drop=True), 
            check_dtype=False, 
            check_index_type=False
        )


    def test_select_golden_data(self):
        print("\n--- 开始自动化比对测试 ---")
        # 清理上一轮可能残留的脏环境
        try:
            self.execute_and_assert("DROP DATABASE company_db;")
        except:
            pass # 没库就忽略
        init_sqls = [
            "CREATE DATABASE company_db;",
            "USE company_db;",
            "CREATE TABLE departments ( id INT PRIMARY KEY, department_name VARCHAR(50) NOT NULL );",
            "CREATE TABLE employees ( id INT PRIMARY KEY, name VARCHAR(100) NOT NULL, age INT, salary DECIMAL(10, 2), dept_id INT, performance_score FLOAT, bonus DOUBLE );",
            "CREATE TABLE customers ( id INT PRIMARY KEY, username VARCHAR(50) NOT NULL, city VARCHAR(50) );",
            "CREATE TABLE orders ( id INT PRIMARY KEY, customer_id INT NOT NULL, amount FLOAT, order_date VARCHAR(20) );",
            "INSERT INTO departments (id, department_name) VALUES (1, 'Engineering'), (2, 'Marketing'), (3, 'HR');",
            "INSERT INTO employees (id, name, age, salary, dept_id, performance_score, bonus) VALUES (1, 'Alice', 28, 45000.00, 2, 4.5, 0), (2, 'John Doe', 32, 55000.00, 1, 3.8, 0), (3, 'Alice Johnson', 45, 72000.00, 2, 4.9, 0), (4, 'Bob Smith', 22, 64000.00, 1, 4.2, 0), (5, 'Charlie HR', 29, 30000.00, 3, 3.0, 0);",
            "INSERT INTO customers (id, username, city) VALUES (1, 'Alice', 'New York'), (2, 'Bob', 'London'), (3, 'Charlie', 'Paris');",
            "INSERT INTO orders (id, customer_id, amount, order_date) VALUES (101, 1, 250.50, '2026-02-20'), (102, 1, 120.00, '2026-02-21'), (103, 2, 999.99, '2026-02-21'), (104, 3, 45.00, '2026-02-22');",
        ]
        for sql in init_sqls:
            self.execute_and_assert(sql)

        # 2. 核对各项查询结果 (对应你提供的 CSV)
        queries = [
            ("UPDATE employees SET bonus = bonus + 5000 WHERE performance_score >= 4.0;", "employees_update.csv"),
            ("DELETE FROM employees WHERE performance_score <= 3.0 AND salary < 40000.00;", "employees_delete.csv"),
            ("SELECT * FROM employees;", "employees_delete.csv"),
            ("SELECT * FROM employees WHERE name LIKE 'Alice%';", "employees_Alice.csv"),
            ("SELECT name, salary, bonus FROM employees WHERE salary + bonus > 60000;", "employees_salary+bonus.csv"), 
            ("SELECT * FROM employees WHERE (age > 30 AND dept_id = 1) OR salary > 70000;", "employees_salary_70000.csv"),
            ("SELECT COUNT(*), AVG(salary) FROM employees;", "employees_COUNT_AVG.csv"),
            ("SELECT dept_id FROM employees GROUP BY dept_id;", "employees_GROUP_BY_dept_id.csv"),
            ("SELECT c.id, c.username, o.amount, o.order_date FROM customers c JOIN orders o ON c.id = o.customer_id;", "employees_join.csv")
        ]
        
        for sql, csv_name in queries:
            with self.subTest(csv_file=csv_name):
                self.execute_and_assert(sql, expected_csv_name=csv_name)

        # 彻底的清理
        drop_queries = [
            "DROP TABLE departments;",
            "DROP TABLE employees;",
            "DROP TABLE customers;",
            "DROP TABLE orders;",
            "DROP DATABASE company_db;"
        ]

        for drop_sql in drop_queries:
            self.execute_and_assert(drop_sql)

        print("--- 所有 Select 测试完成！---")

if __name__ == '__main__':
    unittest.main(verbosity=3)