# (.venv) PS C:\Users\hello\myRespository\PyDB> python -m test.test_parser
import unittest
import sys
import os

# 将项目根目录加入到 sys.path 中，确保能导入编译器代码
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 假设你的编译器代码在根目录下的 compiler.py 中
from sql_core.compiler import SqlLexer, SqlParser

class TestSqlCompiler(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """在所有测试开始前初始化 Lexer 和 Parser"""
        cls.lexer = SqlLexer()
        cls.parser = SqlParser()

    def run_ast_test(self, sql_query, expected_ast):
        """核心断言助手：接收 SQL 和期望的 AST，执行解析并做深度比对"""
        tokens = self.lexer.tokenize(sql_query)
        actual_ast = self.parser.parse(tokens)
        
        self.assertEqual(
            actual_ast, 
            expected_ast, 
            msg=f"\nSQL解析失败!\nSQL: {sql_query}\n期望: {expected_ast}\n实际: {actual_ast}"
        )

    # =========================================================
    # 阶段 1: DDL 测试 (建库建表)
    # =========================================================
    def test_01_ddl_statements(self):
        test_cases = [
            ("CREATE DATABASE company_db;", {"type": "create_database", "database_name": "company_db"}),
            ("USE company_db;", {"type": "use_database", "database_name": "company_db"}),
            (
                """CREATE TABLE departments (
                    id INT PRIMARY KEY,
                    department_name VARCHAR(50) NOT NULL
                );""",
                {
                  "type": "create_table", "table_name": "departments",
                  "columns": [
                    {"name": "id", "data_type": "int", "constraints": ["primary key"]},
                    {"name": "department_name", "data_type": "varchar(50)", "constraints": ["not null"]}
                  ]
                }
            ),
            (
                """CREATE TABLE employees (
                    id INT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    age INT,
                    salary DECIMAL(10, 2),
                    dept_id INT,
                    performance_score FLOAT, 
                    bonus DOUBLE
                );""",
                {
                  "type": "create_table", "table_name": "employees",
                  "columns": [
                    {"name": "id", "data_type": "int", "constraints": ["primary key"]},
                    {"name": "name", "data_type": "varchar(100)", "constraints": ["not null"]},
                    {"name": "age", "data_type": "int", "constraints": []},
                    {"name": "salary", "data_type": "decimal(10,2)", "constraints": []},
                    {"name": "dept_id", "data_type": "int", "constraints": []},
                    {"name": "performance_score", "data_type": "float", "constraints": []},
                    {"name": "bonus", "data_type": "double", "constraints": []}
                  ]
                }
            ),
            (
                """CREATE TABLE customers (
                    id INT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    city VARCHAR(50)
                );""",
                {
                  "type": "create_table", "table_name": "customers",
                  "columns": [
                    {"name": "id", "data_type": "int", "constraints": ["primary key"]},
                    {"name": "username", "data_type": "varchar(50)", "constraints": ["not null"]},
                    {"name": "city", "data_type": "varchar(50)", "constraints": []}
                  ]
                }
            ),
            (
                """CREATE TABLE orders (
                    id INT PRIMARY KEY,
                    customer_id INT NOT NULL,
                    amount FLOAT,
                    order_date VARCHAR(20)
                );""",
                {
                  "type": "create_table", "table_name": "orders",
                  "columns": [
                    {"name": "id", "data_type": "int", "constraints": ["primary key"]},
                    {"name": "customer_id", "data_type": "int", "constraints": ["not null"]},
                    {"name": "amount", "data_type": "float", "constraints": []},
                    {"name": "order_date", "data_type": "varchar(20)", "constraints": []}
                  ]
                }
            )
        ]
        for sql, expected in test_cases:
            with self.subTest(sql=sql):
                self.run_ast_test(sql, expected)

    # =========================================================
    # 阶段 2: 制造测试数据 (DML - INSERT)
    # =========================================================
    def test_02_insert_statements(self):
        test_cases = [
            (
                "INSERT INTO departments (id, department_name) VALUES (1, 'Engineering'), (2, 'Marketing'), (3, 'HR');",
                {
                  "type": "insert", "table_name": "departments",
                  "columns": ["id", "department_name"],
                  "values": [
                    [{"type": "literal", "value": 1}, {"type": "literal", "value": "Engineering"}],
                    [{"type": "literal", "value": 2}, {"type": "literal", "value": "Marketing"}],
                    [{"type": "literal", "value": 3}, {"type": "literal", "value": "HR"}]
                  ]
                }
            ),
            (
                """INSERT INTO employees (id, name, age, salary, dept_id, performance_score, bonus) VALUES 
                (1, 'Alice', 28, 45000.00, 2, 4.5, 0),
                (2, 'John Doe', 32, 55000.00, 1, 3.8, 0), 
                (3, 'Alice Johnson', 45, 72000.00, 2, 4.9, 0), 
                (4, 'Bob Smith', 22, 64000.00, 1, 4.2, 0),
                (5, 'Charlie HR', 29, 30000.00, 3, 3.0, 0);""",
                {
                  "type": "insert", "table_name": "employees",
                  "columns": ["id", "name", "age", "salary", "dept_id", "performance_score", "bonus"],
                  "values": [
                    [{"type": "literal", "value": 1}, {"type": "literal", "value": "Alice"}, {"type": "literal", "value": 28}, {"type": "literal", "value": 45000.0}, {"type": "literal", "value": 2}, {"type": "literal", "value": 4.5}, {"type": "literal", "value": 0}],
                    [{"type": "literal", "value": 2}, {"type": "literal", "value": "John Doe"}, {"type": "literal", "value": 32}, {"type": "literal", "value": 55000.0}, {"type": "literal", "value": 1}, {"type": "literal", "value": 3.8}, {"type": "literal", "value": 0}],
                    [{"type": "literal", "value": 3}, {"type": "literal", "value": "Alice Johnson"}, {"type": "literal", "value": 45}, {"type": "literal", "value": 72000.0}, {"type": "literal", "value": 2}, {"type": "literal", "value": 4.9}, {"type": "literal", "value": 0}],
                    [{"type": "literal", "value": 4}, {"type": "literal", "value": "Bob Smith"}, {"type": "literal", "value": 22}, {"type": "literal", "value": 64000.0}, {"type": "literal", "value": 1}, {"type": "literal", "value": 4.2}, {"type": "literal", "value": 0}],
                    [{"type": "literal", "value": 5}, {"type": "literal", "value": "Charlie HR"}, {"type": "literal", "value": 29}, {"type": "literal", "value": 30000.0}, {"type": "literal", "value": 3}, {"type": "literal", "value": 3.0}, {"type": "literal", "value": 0}]
                  ]
                }
            ),
            (
                "INSERT INTO customers (id, username, city) VALUES (1, 'Alice', 'New York'), (2, 'Bob', 'London'), (3, 'Charlie', 'Paris');",
                {
                  "type": "insert", "table_name": "customers",
                  "columns": ["id", "username", "city"],
                  "values": [
                    [{"type": "literal", "value": 1}, {"type": "literal", "value": "Alice"}, {"type": "literal", "value": "New York"}],
                    [{"type": "literal", "value": 2}, {"type": "literal", "value": "Bob"}, {"type": "literal", "value": "London"}],
                    [{"type": "literal", "value": 3}, {"type": "literal", "value": "Charlie"}, {"type": "literal", "value": "Paris"}]
                  ]
                }
            ),
            (
                """INSERT INTO orders (id, customer_id, amount, order_date) VALUES 
                (101, 1, 250.50, '2026-02-20'),
                (102, 1, 120.00, '2026-02-21'),
                (103, 2, 999.99, '2026-02-21'),
                (104, 3, 45.00, '2026-02-22');""",
                {
                  "type": "insert", "table_name": "orders",
                  "columns": ["id", "customer_id", "amount", "order_date"],
                  "values": [
                    [{"type": "literal", "value": 101}, {"type": "literal", "value": 1}, {"type": "literal", "value": 250.5}, {"type": "literal", "value": "2026-02-20"}],
                    [{"type": "literal", "value": 102}, {"type": "literal", "value": 1}, {"type": "literal", "value": 120.0}, {"type": "literal", "value": "2026-02-21"}],
                    [{"type": "literal", "value": 103}, {"type": "literal", "value": 2}, {"type": "literal", "value": 999.99}, {"type": "literal", "value": "2026-02-21"}],
                    [{"type": "literal", "value": 104}, {"type": "literal", "value": 3}, {"type": "literal", "value": 45.0}, {"type": "literal", "value": "2026-02-22"}]
                  ]
                }
            )
        ]
        for sql, expected in test_cases:
            with self.subTest(sql=sql):
                self.run_ast_test(sql, expected)

    # =========================================================
    # 阶段 3: 数据更新与清洗 (DML - UPDATE/DELETE)
    # =========================================================
    def test_03_update_delete(self):
        test_cases = [
            (
                "UPDATE employees SET bonus = bonus + 5000 WHERE performance_score >= 4.0;",
                {
                  "type": "update", "table_name": "employees",
                  "assignments": [
                    {
                      "column": "bonus",
                      "value": {"type": "math_op", "operator": "+", "left": {"type": "column", "value": "bonus"}, "right": {"type": "literal", "value": 5000}}
                    }
                  ],
                  "where": {
                    "type": "compare_op", "operator": ">=",
                    "left": {"type": "column", "value": "performance_score"},
                    "right": {"type": "literal", "value": 4.0}
                  }
                }
            ),
            (
                "DELETE FROM employees WHERE performance_score <= 3.0 AND salary < 40000.00;",
                {
                  "type": "delete", "table_name": "employees",
                  "where": {
                    "type": "logical_op", "operator": "AND",
                    "left": {
                      "type": "compare_op", "operator": "<=",
                      "left": {"type": "column", "value": "performance_score"},
                      "right": {"type": "literal", "value": 3.0}
                    },
                    "right": {
                      "type": "compare_op", "operator": "<",
                      "left": {"type": "column", "value": "salary"},
                      "right": {"type": "literal", "value": 40000.0}
                    }
                  }
                }
            )
        ]
        for sql, expected in test_cases:
            with self.subTest(sql=sql):
                self.run_ast_test(sql, expected)

    # =========================================================
    # 阶段 4: 核心表达式与查询流水线测试 (DQL)
    # =========================================================
    def test_04_select_queries(self):
        test_cases = [
            ("SELECT * FROM employees;", {
              "type": "select", "select_list": ["*"], "table_source": {"table": "employees", "alias": None},
              "join": [], "where": None, "group_by": None, "order_by": None, "limit": None
            }),
            ("SELECT * FROM employees WHERE name LIKE 'Alice%';", {
              "type": "select", "select_list": ["*"], "table_source": {"table": "employees", "alias": None},
              "join": [], "where": {"type": "compare_op", "operator": "LIKE", "left": {"type": "column", "value": "name"}, "right": {"type": "literal", "value": "Alice%"}},
              "group_by": None, "order_by": None, "limit": None
            }),
            ("SELECT name, salary, bonus FROM employees WHERE salary + bonus > 60000;", {
              "type": "select", 
              "select_list": [{"type": "column", "value": "name"}, {"type": "column", "value": "salary"}, {"type": "column", "value": "bonus"}],
              "table_source": {"table": "employees", "alias": None}, "join": [],
              "where": {"type": "compare_op", "operator": ">", "left": {"type": "math_op", "operator": "+", "left": {"type": "column", "value": "salary"}, "right": {"type": "column", "value": "bonus"}}, "right": {"type": "literal", "value": 60000}},
              "group_by": None, "order_by": None, "limit": None
            }),
            ("SELECT COUNT(*), AVG(salary) FROM employees;", {
              "type": "select",
              "select_list": [{"type": "func", "name": "COUNT", "args": "*"}, {"type": "func", "name": "AVG", "args": {"type": "column", "value": "salary"}}],
              "table_source": {"table": "employees", "alias": None}, "join": [], "where": None, "group_by": None, "order_by": None, "limit": None
            }),
            ("SELECT dept_id FROM employees GROUP BY dept_id;", {
              "type": "select", "select_list": [{"type": "column", "value": "dept_id"}],
              "table_source": {"table": "employees", "alias": None}, "join": [], "where": None, "group_by": ["dept_id"], "order_by": None, "limit": None
            }),
            (
                """SELECT c.id, c.username, o.amount, o.order_date
                FROM customers c
                JOIN orders o ON c.id = o.customer_id;""",
                {
                  "type": "select",
                  "select_list": [{"type": "column", "value": "c.id"}, {"type": "column", "value": "c.username"}, {"type": "column", "value": "o.amount"}, {"type": "column", "value": "o.order_date"}],
                  "table_source": {"table": "customers", "alias": "c"},
                  "join": [
                    {"type": "INNER", "table": {"table": "orders", "alias": "o"}, "on": {"type": "compare_op", "operator": "=", "left": {"type": "column", "value": "c.id"}, "right": {"type": "column", "value": "o.customer_id"}}}
                  ],
                  "where": None, "group_by": None, "order_by": None, "limit": None
                }
            )
        ]
        for sql, expected in test_cases:
            with self.subTest(sql=sql):
                self.run_ast_test(sql, expected)

    # =========================================================
    # 阶段 5: 🌟 终极压力测试 (The Ultimate Pipeline)
    # =========================================================
    def test_05_ultimate_pipeline(self):
        sql = """
        SELECT e.name, d.department_name, e.salary
        FROM employees e
        JOIN departments d ON e.dept_id = d.id
        WHERE (e.age > 25 AND e.salary >= 50000) OR e.name LIKE 'A%'
        GROUP BY d.department_name
        ORDER BY e.salary DESC
        LIMIT 5;
        """
        expected_ast = {
          "type": "select",
          "select_list": [
            {"type": "column", "value": "e.name"},
            {"type": "column", "value": "d.department_name"},
            {"type": "column", "value": "e.salary"}
          ],
          "table_source": {"table": "employees", "alias": "e"},
          "join": [
            {
              "type": "INNER",
              "table": {"table": "departments", "alias": "d"},
              "on": {
                "type": "compare_op", "operator": "=",
                "left": {"type": "column", "value": "e.dept_id"},
                "right": {"type": "column", "value": "d.id"}
              }
            }
          ],
          "where": {
            "type": "logical_op", "operator": "OR",
            "left": {
              "type": "logical_op", "operator": "AND",
              "left": {
                "type": "compare_op", "operator": ">",
                "left": {"type": "column", "value": "e.age"},
                "right": {"type": "literal", "value": 25}
              },
              "right": {
                "type": "compare_op", "operator": ">=",
                "left": {"type": "column", "value": "e.salary"},
                "right": {"type": "literal", "value": 50000}
              }
            },
            "right": {
              "type": "compare_op", "operator": "LIKE",
              "left": {"type": "column", "value": "e.name"},
              "right": {"type": "literal", "value": "A%"}
            }
          },
          "group_by": ["d.department_name"],
          "order_by": [
            {"column": "e.salary", "direction": "DESC"}
          ],
          "limit": 5
        }
        self.run_ast_test(sql, expected_ast)

    # =========================================================
    # 阶段 6: 破坏性测试 (清理)
    # =========================================================
    def test_06_drop_statements(self):
        test_cases = [
            ("DROP TABLE employees;", {"type": "drop_table", "table_name": "employees"}),
            ("DROP DATABASE company_db;", {"type": "drop_database", "database_name": "company_db"})
        ]
        for sql, expected in test_cases:
            with self.subTest(sql=sql):
                self.run_ast_test(sql, expected)

if __name__ == '__main__':
    unittest.main(verbosity=2)