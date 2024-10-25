import utils.util
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
        user_input = utils.util.user_input()
        print(user_input)
        if user_input is None:
            # 如果user_input返回None，退出整个服务器循环
            break

        tokens = lexer.tokenize(user_input)
        parser.parse(tokens)
