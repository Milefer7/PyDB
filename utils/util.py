import time
import os
from colorama import Fore, Style


def user_input():
    info_input = ''
    while True:
        # 定义带颜色的提示符
        # Fore.CYAN 让文字变青色，Style.BRIGHT 让颜色更亮，Style.RESET_ALL 确保用户输入的内容恢复默认颜色
        prompt_main = f"{Fore.CYAN}{Style.BRIGHT}pysql> {Style.RESET_ALL}"
        prompt_cont = f"{Fore.CYAN}{Style.BRIGHT}>>>> {Style.RESET_ALL}"

        if info_input == '':
            # 第一次提示
            current_line = input(prompt_main)
            info_input = current_line
        else:
            # 当输入不完整时，继续提示输入
            current_line = input(prompt_cont)
            # 🌟 关键修改：拼接时增加一个空格，防止跨行单词粘连
            info_input += " " + current_line

        # 如果输入是 'exit;'，返回 None 表示退出
        if info_input.lower().strip() == 'exit;':
            return None
        
        # 检查是否以分号结尾（考虑到用户可能在分号后误打空格，用 strip）
        if ';' in info_input:
            return info_input.strip()


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f" ({end_time - start_time:.2f} sec)", end="")
        print()
        return result
    return wrapper


def find_table(table_name, path_to_find):
    # print(path_to_find)
    for root, dirs, files in os.walk(path_to_find):
        if f"{table_name}.csv" in files:
            return True
    return False
