import random
from faker import Faker

# 初始化 Faker 实例
fake = Faker()

# 定义部门列表
departments = ['Engineering', 'HR', 'Finance', 'Marketing']


# 生成1000条数据的SQL
def generate_sql(num_records=1000):
    sql = "INSERT INTO employees (id, name, salary, department) VALUES\n"
    for i in range(1, num_records + 1):
        name = fake.name()
        salary = round(random.uniform(50000, 100000), 2)  # 随机生成50,000到100,000之间的薪水
        department = random.choice(departments)
        sql += f"({i}, '{name}', {salary}, '{department}')"

        if i < num_records:
            sql += ",\n"
        else:
            sql += ";"

    return sql


if __name__ == '__main__':
    # 生成SQL语句
    sql = generate_sql(1000)

    # 输出结果
    with open('insert1000.sql', 'w') as file:
        file.write(sql)
