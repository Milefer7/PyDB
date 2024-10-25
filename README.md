# **项目结构**

```python
PyDBMS
├── algebra/           # 处理关系代数解析与执行
│   ├── parser.py      # sql解析模块
│   ├── executor.py    # sql执行模块
│   └── ast.py         # 语法树节点定义
├── storage/           # 数据存储引擎
│   ├── engine.py      # 数据存储逻辑
├── transaction/       # 事务管理与日志记录
│   ├── log.py         # 日志管理
│   ├── transaction.py # 事务管理
├── gui/               # PyQt5 GUI 相关文件
│   ├── mainwindow.py  # 主窗口逻辑
├── server.py          # 主服务，处理客户端请求
└── README.md          # 项目文档
```

#### 1. **确定项目范围**

首先，明确项目的范围和目标。你需要决定这个 DBMS 的核心功能，比如：

- 支持基本的 SQL 操作：`SELECT`，`INSERT`，`UPDATE`，`DELETE`
- 简单的事务支持
- 基础的索引机制
- 文件存储引擎

你可以从一个非常简化的功能集开始，逐步增加复杂性。

#### 2. **模块划分**

参考 MySQL 的模块划分方式，设计你的 Python DBMS 各个模块：

- **SQL 解析器**：负责解析输入的 SQL 查询，将其转换为内部表示（AST，抽象语法树）。
  - 可以使用 Python 的 `ply` 或 `lark-parser` 这样的解析器生成库来实现 SQL 解析。
- **查询优化器**：解析后的 SQL 语句通常需要进行优化，比如选择合适的执行路径（简化的查询优化）。
- **执行器**：负责执行 SQL 语句，访问数据库文件、处理数据和返回结果。
- **存储引擎**：负责管理底层数据的存储，可以设计自己的简单文件格式，或者使用现有的存储库（如 SQLite 的文件系统）。
- **日志与事务管理**：实现简单的事务机制（如 ACID），可以通过文件日志记录来确保一致性和恢复。

#### 3. **功能实现细节**

- **SQL 解析**：可以参考 MySQL 的 SQL 解析器，构建一个基于 Python 的语法解析工具。`lark-parser` 可以帮助你生成一个简单的 SQL 解析器。
- **存储引擎**：你可以简化 MySQL 的存储引擎逻辑，设计一个文件存储机制，每个表用一个文件来存储，类似于 MySQL 的 MyISAM 引擎最基本的存储方式。
- **索引**：可以参考 B-tree 或哈希索引结构，初期你可以实现一个简单的线性扫描，后期逐步优化成 B-tree 等复杂结构。
- **事务管理**：可以参考 MySQL 的事务机制，设计一个简化版的日志记录系统（Write-Ahead Logging, WAL），确保基本的 ACID 特性。

#### 4. **测试与优化**

在实现完初步功能后，使用一些 SQL 语句进行测试，并逐步优化性能。你还可以尝试实现更多的高级功能，比如多用户并发控制（可以参考 MySQL 的锁机制）。

## 完成SQL语句

* 创建数据库
  * `CREATE DATABASE IDENTIFIER;`
    * `CREATE DATABASE test;`

* 展示所有数据库
  * `SHOW DATABASES;`
* 使用某个数据库
  * `USE IDENTIFIER`
    * `USE test`





# Create（增）：插入数据

    # data_c1 = "INSERT INTO users (name, age, city) VALUES ('John', 25, 'New York');"
    # # Read（查）：查询数据
    # data_r1 = "SELECT name, age FROM users WHERE age > 30 AND city = 'New York';"
    # # Update（改）：更新数据
    # data_u1 = "UPDATE users SET age = 26 WHERE name = 'John';"
    # # Delete（删）：删除数据
    # data_d1 = "DELETE FROM users WHERE age < 20;"
    #
    # data_list = [data_create_database]
    # # data_list = [data_create_database, data_d1, data_r1, data_u1, data_d1]
    # lexer = SqlLexer()
    # for data in data_list:
    #     for tok in lexer.tokenize(data):
    #         print('type=%r, value=%r' % (tok.type, tok.value))
    #     print('----------------------------------------------')