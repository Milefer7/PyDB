import os
import time

def init_log(path):
    """初始化数据库时创建日志文件"""
    try:
        os.makedirs(path, exist_ok=True)
        log_file_path = os.path.join(path, 'log.txt')
        # 用 'a' 模式追加，防止覆盖已有日志
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            log_file.write(f"[{current_time}] [SYSTEM] Database initialized.\n")
    except Exception as e:
        print(f"An error occurred while creating the log file: {e}")

def write_log(path, sql_query, status="SUCCESS", error_msg=""):
    """
    函数参数解释
    :param path: 当前选中的数据库路径
    :param sql_query: 用户输入的原始 SQL
    :param status: SUCCESS 或 ERROR
    :param error_msg: 如果报错了，记录下具体的错误信息
    """
    # 如果还没选中任何数据库 (USE database)，就不记录
    if not path or not os.path.exists(path):
        return
        
    try:
        log_file_path = os.path.join(path, 'log.txt')
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            
            # 清理一下 SQL 里的换行符，保证日志一行一条，整齐美观
            clean_sql = ' '.join(sql_query.split())
            
            if status == "SUCCESS":
                log_file.write(f"[{current_time}] [INFO] {clean_sql}\n")
            else:
                log_file.write(f"[{current_time}] [ERROR] {clean_sql} | Reason: {error_msg}\n")
    except Exception:
        # 日志写入失败不影响主程序运行，静默吞掉异常
        pass