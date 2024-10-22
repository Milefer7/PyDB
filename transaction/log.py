import os
import time


def init_log(path):
    try:
        os.makedirs(path, exist_ok=True)
        log_file_path = os.path.join(path, 'log.txt')
        with open(log_file_path, 'w') as log_file:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 使用 time 模块获取当前时间
            log_file.write(f"Log file created at {current_time}.\n")
    except Exception as e:
        print(f"An error occurred while creating the log file: {e}")
