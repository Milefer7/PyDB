import utils.util
from sql_core.compiler import *
from router.router import *
from colorama import Fore, Style
import json


def sql_client():
    # 定义本次会话的全局变量db
    db = DatabaseManager()
    lexer = SqlLexer()
    parser = SqlParser(db)

    # 监听控制台
    while True:
        try:
            user_input = utils.util.user_input()
            if user_input is None:  # 如果user_input返回None，退出整个服务器循环
                break

            tokens = lexer.tokenize(user_input)
            # 打印每个 token 的详细信息
            # for i, token in enumerate(tokens):
            #     print(f"Token {i}: {token}")
            #     # 如果 token 有类型和值属性
            #     if hasattr(token, 'type') and hasattr(token, 'value'):
            #         print(f"  类型: {token.type}, 值: {token.value}")
            #     # 如果是元组形式 (type, value)
            #     elif isinstance(token, tuple) and len(token) >= 2:
            #         print(f"  类型: {token[0]}, 值: {token[1]}")
            #     print()
            parser_tree = parser.parse(tokens)
            print(json.dumps(parser_tree, indent=2))
            # router(parser_tree, db)

        except Exception as e:
            # print(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)
            print(Fore.RED + "An error occurred:" + Style.RESET_ALL + f" {e}")
            continue
