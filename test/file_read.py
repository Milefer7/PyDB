import os
import time
from utils.util import *


@timeit
def test_file_read_speed(file_path):
    # 获取文件大小
    file_size = os.path.getsize(file_path)

    # 读取文件内容
    with open(file_path, 'rb') as file:
        file.read()

    print(f"文件大小: {file_size / (1024 ** 2):.2f} MB")
    # print(f"读取时间: {read_time:.4f} 秒")
    # print(f"读取速度: {read_speed / (1024 ** 2):.2f} MB/s")  # 转换为 MB/s


# 示例：测试一个文件的读入速度
if __name__ == '__main__':
    # print(os.getcwd())
    file_paths = []
    file_paths.append("../mock/employees_1000.csv")
    file_paths.append("../mock/employees_10000.csv")
    file_paths.append("../mock/employees_0.1_million.csv")
    file_paths.append("../mock/employees_1_million.csv")
    file_paths.append("../mock/employees_10_million.csv")
    for file_path in file_paths:
        test_file_read_speed(file_path)


