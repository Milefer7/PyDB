import random
import csv
from faker import Faker

# 初始化 Faker 实例
fake = Faker()

# 定义部门列表
departments = ['Engineering', 'HR', 'Finance', 'Marketing']


# 生成1000条数据并写入CSV
def generate_csv(num_records=1000, filename='employees_0.1_million.csv'):
    # 打开 CSV 文件进行写入
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # 写入列头
        writer.writerow(['id', 'name', 'salary', 'department'])

        # 生成数据并写入每一行
        for i in range(1, num_records + 1):
            name = fake.first_name()
            salary = round(random.uniform(50000, 100000), 2)  # 随机生成50,000到100,000之间的薪水
            department = random.choice(departments)
            writer.writerow([i, name, salary, department])


# 生成 CSV 文件
if __name__ == '__main__':
    generate_csv(1000, 'employees_1000.csv')  # 生成???条记录
    print("CSV 文件 'employees_0.1_million.csv' 生成成功!")
