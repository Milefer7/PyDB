# # 测试sql语句的各个模块执行的时间
# import time
# import pandas as pd
# from sql_core.compiler import SqlLexer, SqlParser
# from storage.executor import Executor

# # 准备 1 万行假数据 DataFrame
# df_100k = pd.DataFrame({
#     'id': range(10000),
#     'salary': [50000] * 10000,
#     'bonus': [1000] * 10000
# })
# # # 准备 10 万行假数据 DataFrame
# # df_100k = pd.DataFrame({
# #     'id': range(100000),
# #     'salary': [50000] * 100000,
# #     'bonus': [1000] * 100000
# # })
# # # 准备 100 万行假数据 DataFrame
# # df_100k = pd.DataFrame({
# #     'id': range(1000000),
# #     'salary': [50000] * 1000000,
# #     'bonus': [1000] * 1000000
# # })

# lexer = SqlLexer()
# parser = SqlParser()
# sql = "SELECT id, salary + bonus FROM employees WHERE salary > 40000;"

# # 1. 测编译时间
# t0 = time.perf_counter()
# tokens = lexer.tokenize(sql)
# ast = parser.parse(tokens)
# t1 = time.perf_counter()

# # 2. 测执行时间
# df_result = Executor.execute_select(df_100k, ast) # 假设不需要传 db 参数
# t2 = time.perf_counter()

# print(f"编译耗时 (Lexer+Parser): {(t1 - t0) * 1000:.3f} ms")
# print(f"执行耗时 (Pandas Engine): {(t2 - t1) * 1000:.3f} ms")

# # 测试结果
# # 10000 row(s) in set.
# # 编译耗时 (Lexer+Parser): 0.159 ms
# # 执行耗时 (Pandas Engine): 141.615 ms

# # 100000 row(s) in set.
# # 编译耗时 (Lexer+Parser): 0.164 ms
# # 执行耗时 (Pandas Engine): 1751.450 ms

# # 1000000 row(s) in set.
# # 编译耗时 (Lexer+Parser): 0.155 ms
# # 执行耗时 (Pandas Engine): 19296.646 ms

# ── 编译性能：用 SQL 复杂度作为变量 ──

import timeit
import time
import pandas as pd
from sql_core.compiler import SqlLexer, SqlParser
from storage.executor import Executor

lexer = SqlLexer()
parser = SqlParser()

sqls = {
    "easy": "SELECT * FROM employees;",
    "mid":  "SELECT name, salary FROM employees WHERE age > 30 AND dept_id = 1;",
    "hard": "SELECT e.name, d.department_name FROM employees e JOIN departments d ON e.dept_id = d.id WHERE e.salary > 50000 GROUP BY d.department_name ORDER BY e.salary DESC;"
}

results = []  # 收集所有输出行

# ── Part 1: perf_counter 循环均值 ──
results.append("=== Part 1: perf_counter × 1000 均值 ===")
for level, query in sqls.items():
    t_start = time.perf_counter()
    for _ in range(1000):
        parser.parse(lexer.tokenize(query))
    t_end = time.perf_counter()
    line = f"[{level}] 复杂度 SQL 单次解析平均耗时: {(t_end - t_start):.3f} ms"
    print(line)
    results.append(line)

# ── Part 2: timeit × 10000 均值 ──
results.append("\n=== Part 2: timeit × 10000 均值 ===")
t_simple = timeit.timeit(lambda: parser.parse(lexer.tokenize(sqls.get('easy'))), number=10000)
t_mid    = timeit.timeit(lambda: parser.parse(lexer.tokenize(sqls.get('mid'))),  number=10000)
t_hard   = timeit.timeit(lambda: parser.parse(lexer.tokenize(sqls.get('hard'))), number=10000)

for label, t in [("简单SQL", t_simple), ("中等SQL", t_mid), ("复杂SQL", t_hard)]:
    line = f"{label} 平均编译: {t / 10000 * 1000:.4f} ms"
    print(line)
    results.append(line)

# ── Part 3: 执行性能，数据行数为变量 ──
results.append("\n=== Part 3: 执行性能（行数变量）===")
ast = parser.parse(lexer.tokenize("SELECT id, salary + bonus FROM employees WHERE salary > 40000;"))

for n in [10_000, 100_000, 1_000_000]:
    df = pd.DataFrame({
        'id':     range(n),
        'salary': [50000] * n,
        'bonus':  [1000]  * n,
    })
    t0 = time.perf_counter()
    Executor.execute_select(df, ast)
    t1 = time.perf_counter()
    line = f"{n:>10,} 行  执行耗时: {(t1 - t0) * 1000:.3f} ms"
    print(line)
    results.append(line)

# ── 持久化到文件 ──
output_path = "benchmark_results.txt"
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

with open(output_path, "w", encoding="utf-8") as f:
    f.write(f"Benchmark Run @ {timestamp}\n")
    f.write("=" * 50 + "\n")
    f.write("\n".join(results) + "\n")

print(f"\n结果已写入 {output_path}")

