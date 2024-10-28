from server.server import sql_server
from algebra.executor import DatabaseManager
from algebra.executor import *
from algebra.parser import *
import json

# if __name__ == '__main__':
#     sql_server()

if __name__ == '__main__':
    db = DatabaseManager()
    # user_input = 'USE test;'
    # user_input = 'CREATE DATABASE test_db '
    # SHOW DATABASES USE test_db;'
    # user_input = 'SHOW DATABASES;'
    # user_input = "SELECT id, name, salary FROM employees WHERE department = 'Sales' ORDER BY salary DESC LIMIT 3;"
    user_input = """
    CREATE TABLE employees (
        id INT PRIMARY KEY NOT NULL,
        name VARCHAR(100) NOT NULL,
        salary DECIMAL(10, 2),
        department VARCHAR(50)
    );
    """
    # user_input = 'salary DECIMAL(10, 2),'
    lexer = SqlLexer()
    # parser = SqlParser(db)
    tokens = lexer.tokenize(user_input)
    for tok in tokens:
        print(f"Token Type: {tok.type}, Token Value: {tok.value}")
    # print(parser.parse(tokens))
    # parser_tree = parser.parse(tokens)
    # print(json.dumps(parser_tree, indent=2))
