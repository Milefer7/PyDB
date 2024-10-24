from algebra.executor import DatabaseManager
from algebra.executor import *
from algebra.parser import *


def sql_server():
    # 定义本次会话的全局变量db
    db = DatabaseManager()

    lexer = SqlLexer()
    parser = SqlParser(db)

    # 监听控制台
    while True:
        user_input = input('SQL> ')

        if user_input.lower() == 'exit':
            print('Exiting the SQL server.')
            break

        tokens = lexer.tokenize(user_input)
        parser.parse(tokens)
