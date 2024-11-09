import matplotlib.pyplot as plt

# 假设记录了插入时间的列表
mysql_times = [0.0068, 0.0046, 0.0060, 0.0091, 0.0252, 0.0377, 0.1793, 0.7021, 1.4322]  # MySQL的插入时间
python_db_times = [0.0046, 0.0055, 0.0078, 0.0185, 0.0371, 0.1679, 0.6373, 17.1394, 58.9076]  # 自己实现的数据库插入时间

# 数据量
data_sizes = [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000]

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

# 绘制曲线图
plt.plot(data_sizes, mysql_times, label="MySQL", marker='o')
plt.plot(data_sizes, python_db_times, label="PyDB", marker='x')

# 设置图表的标题和标签
plt.title("插入数据性能对比（MySQL vs PyDB）")
plt.xlabel("数据量")
plt.ylabel("插入时间（秒）")

# 设置对数坐标轴（可选，根据数据的量级）
plt.xscale("log")
plt.yscale("log")

# 显示图例
plt.legend()

plt.savefig("performance_comparison.png", format="png", dpi=300)

# 显示图表
plt.show()
