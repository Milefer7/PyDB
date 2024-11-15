import utils.util
from sql_core.compiler import *
from router.router import *
from colorama import Fore, Style


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
            parser_tree = parser.parse(tokens)
            # print(json.dumps(parser_tree, indent=2))
            router(parser_tree, db)

        except Exception as e:
            # print(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)
            print(Fore.RED + "An error occurred:" + Style.RESET_ALL + f" {e}")
            continue
