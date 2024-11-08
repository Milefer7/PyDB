import matplotlib.pyplot as plt

# 假设记录了插入时间的列表
mysql_times = [0.1, 1.2, 12, 120]  # MySQL的插入时间
python_db_times = [0.2, 2.5, 25, 250]  # 自己实现的数据库插入时间

# 数据量
data_sizes = [1000, 10000, 100000, 1000000]

# 绘制曲线图
plt.plot(data_sizes, mysql_times, label="MySQL", marker='o')
plt.plot(data_sizes, python_db_times, label="Python DB", marker='x')

# 设置图表的标题和标签
plt.title("插入数据性能对比（MySQL vs Python DB）")
plt.xlabel("数据量")
plt.ylabel("插入时间（秒）")

# 设置对数坐标轴（可选，根据数据的量级）
plt.xscale("log")
plt.yscale("log")

# 显示图例
plt.legend()

# 显示图表
plt.show()
