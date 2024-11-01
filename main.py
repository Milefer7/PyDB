import json

from algebra.executor import *
from algebra.parser import *

# if __name__ == '__main__':
#     sql_server()

if __name__ == '__main__':
    db = DatabaseManager()

    # user_input = 'USE test;'

    # user_input = 'CREATE DATABASE test_db;'
    #
    user_input = 'SHOW DATABASES;'
    #
    # user_input = """
    # CREATE TABLE employees (
    #     id INT PRIMARY KEY NOT NULL,
    #     name VARCHAR(100) NOT NULL,
    #     salary DECIMAL(10, 2),
    #     department VARCHAR(50)
    # );
    # """

    # user_input = """
    # SELECT name, age
    # FROM users
    # WHERE
    #     city = 'New York'
    #     AND name = 'John Doe'
    # ORDER BY age DESC;
    # """

    # user_input = '''
    # SELECT s.name, c.course_name
    # FROM students s
    # JOIN courses c ON s.course_id = c.id;
    # '''

    # user_input = '''
    # INSERT INTO students (name, age, major) VALUES
    # ('Bob', 22, 'Mathematics'),
    # ('Charlie', 19, 'Physics');
    # '''

    # user_input = """
    # INSERT INTO graduated_students (name, age, major)
    # SELECT name, age, major FROM students WHERE graduated = true;
    # """

    # user_input = """
    # SELECT * FROM students;
    # """

    user_input = """
    SELECT name, age FROM students;
    """

    # user_input = '''
    #     SELECT name, age
    #     FROM students
    #     WHERE graduated = true
    #         AND age > 20
    #         AND name = 'Ella'
    #         AND NOT age = 25;
    # '''

    # user_input = '''
    # SELECT name, age FROM students ORDER BY age DESC;
    #  '''

    # user_input = '''
    # SELECT s.name, c.course_name
    # FROM students s
    # JOIN courses c ON s.course_id = c.id;
    # '''

    # user_input = '''
    # SELECT name, age FROM students
    # WHERE major IN (SELECT major FROM majors WHERE department = 'Science');
    # '''
    lexer = SqlLexer()
    parser = SqlParser(db)
    tokens = lexer.tokenize(user_input)
    # for tok in tokens:
    #     print(f"Token Type: {tok.type}, Token Value: {tok.value}")
    parser_tree = parser.parse(tokens)
    print(json.dumps(parser_tree, indent=2))
