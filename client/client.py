import utils.util
from sql_core.compiler import *
from router.router import *
from colorama import Fore, Style
import json
from utils.ai_dba import diagnose_sql_error
from transaction.log import write_log

def sql_client():
    # 定义本次会话的全局变量db
    db = DatabaseManager()
    lexer = SqlLexer()
    parser = SqlParser(db)
    
    # AI DBA 全局开关
    ai_dba_enabled = False
    # 用来保护“案发现场”的记忆变量
    last_failed_sql = None
    last_error_msg = None
    prompt_egg = True
    
    print(Fore.GREEN + Style.BRIGHT +"[Welcome to PyDB]" + Style.RESET_ALL)
    # print("提示: 输入 '+ai;' 可开启 AI 智能诊断助手，输入 '-ai;' 可关闭。")

    # 监听控制台
    while True:
        try:
            user_input = utils.util.user_input()
            if user_input is None:  # 如果user_input返回None，退出整个服务器循环
                break
                
            # 清理输入，方便做命令拦截
            clean_input = user_input.strip().lower()
            
            # 拦截系统级命令：开启或关闭 AI
            if clean_input in ('+ai;'):
                ai_dba_enabled = True
                print(Fore.GREEN + "[系统通知]: AI DBA 智能诊断已开启！" + Style.RESET_ALL)
                # 如果刚刚发生了错误，直接调起 AI 诊断！
                if last_failed_sql and last_error_msg:
                    diagnose_sql_error(last_failed_sql, last_error_msg)
                    # 诊断完就清空，防止下次重复诊断
                    last_failed_sql = None
                    last_error_msg = None
                    
                continue
            elif clean_input in ('-ai;'):
                ai_dba_enabled = False
                print(Fore.YELLOW + "[系统通知]: AI DBA 智能诊断已关闭。" + Style.RESET_ALL)
                continue

            # 正常 SQL 解析与路由
            tokens = lexer.tokenize(user_input)
            parser_tree = parser.parse(tokens)
            # print(json.dumps(parser_tree, indent=2))
            myRouter(parser_tree, db)

            # 代码能走到这里没有抛出异常，说明 SQL 执行成功！记录 INFO 日志
            if db.database_path:
                write_log(db.database_path, user_input, status="SUCCESS")
            
            # 如果一条 SQL 成功执行到底，说明没有报错，清空之前的错误记忆
            last_failed_sql = None
            last_error_msg = None

        except Exception as e:
            # 先打印出原本的系统报错
            raw_error = str(e)
            print(Fore.RED + f"[系统报错] {raw_error}" + Style.RESET_ALL)
            
            # 记住案发现场，留给后面的 '+ai;' 使用
            last_failed_sql = user_input
            last_error_msg = raw_error

            # 记录 ERROR 日志
            if db.database_path:
                write_log(db.database_path, user_input, status="ERROR", error_msg=raw_error)
            
            # 根据开关状态决定是否召唤 AI
            if ai_dba_enabled:
                diagnose_sql_error(user_input, raw_error)
                # AI 已经接管了，清空现场
                last_failed_sql = None
                last_error_msg = None
            else:
                # 贴心的小彩蛋：如果没开 AI，微微提示用户可以开
                if prompt_egg:
                    print(Fore.LIGHTBLACK_EX + "(提示: 输入 '+ai;' 可开启 AI DBA 诊断此错误，输入 '-ai;'可关闭此模式)" + Style.RESET_ALL)
                    prompt_egg = False
