import time
import os


def user_input():
    info_input = ''
    while True:
        if info_input == '':
            # 第一次提示
            info_input = input('SQL> ')
        else:
            # 当输入不完整时，继续提示输入
            info_input += input('>>>> ')
        # 如果输入是 'exit;'，返回 None 表示退出
        if info_input.lower().strip() == 'exit;':
            return None
        if ';' in info_input:
            return info_input.strip()


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        # 回到上一行并输出内容到上一行的结尾
        print(f" ({end_time - start_time:.4f} sec)")  # 在上一行结尾处输出
        return result

    return wrapper


def find_table(table_name, path_to_find):
    for root, dirs, files in os.walk(path_to_find):
        if f"{table_name}.csv" in files:
            return True
    return False
