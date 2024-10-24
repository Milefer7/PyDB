from server.server import sql_server
from algebra.executor import DatabaseManager
from algebra.executor import *
from algebra.parser import *

# if __name__ == '__main__':
#     sql_server()

if __name__ == '__main__':
    db = DatabaseManager()
    user_input = 'USE test;'
    # user_input = 'CREATE DATABASE test;'
    # user_input = 'SHOW DATABASES;'
    lexer = SqlLexer()
    parser = SqlParser(db)
    tokens = lexer.tokenize(user_input)
    # for tok in tokens:
    #     print(f"Token Type: {tok.type}, Token Value: {tok.value}")
    # print(tokens)
    parser.parse(tokens)
