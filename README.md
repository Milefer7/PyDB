# 🎉 简版 `PYDB`

> 小玩具，实现 `sql` 编译器中几个 `sql` 语句解析 + storage层简单处理。

## :one:  **项目结构**

```
PyDBMS
├── README.md          
├── client             # 客户端代码目录
│   └── client.py      
├── config             # 配置文件目录
├── database           
├── main.py            # 主程序文件，程序入口，初始化和启动服务
├── mock               # 模拟数据
├── router             # 路由相关代码，负责请求和响应的路由逻辑
│   └── router.py     
├── sql_core           # SQL解析和执行相关的核心模块
│   └── compiler.py    # SQL编译器，解析SQL语句并生成执行计划
├── storage            # 数据存储引擎，处理数据存储和访问
│   └── engine.py      
├── test               # 测试代码目录，包含项目的单元测试
│   └── test_parser.py 
├── transaction        # 事务管理和日志记录
│   └── log.py         
└── utils              # 工具类代码，包含通用的辅助函数
    └── util.py        
```

## :two: 层级设计

![image-20241112170540661](https://my-note-drawing-bed-1322822796.cos.ap-shanghai.myqcloud.com/picture/202411121705152.png)

## :three: 模块拆分

<img src="https://my-note-drawing-bed-1322822796.cos.ap-shanghai.myqcloud.com/picture/202411121706060.png" alt="image-20241112170615921" style="zoom:50%;" />

## :four: 细节阐述

### 4.2  `SQL` 支持类型

![image-20241112171055491](https://my-note-drawing-bed-1322822796.cos.ap-shanghai.myqcloud.com/picture/202411121710550.png)

### 4.2 `SQL` 文法规则

> 调用 [sly](https://sly.readthedocs.io/en/latest/sly.html) 库，`LALR(1)` 文法

```
<statement>       ::= <create_database> 
                    | <create_table>
                    | <show_database>
                    | <use_database>
                    | <insert_data>
                    | <select_data>
                    | <delete_data>
                    
<delete_data>     ::= 'DELETE' 'FROM' 'IDENTIFIER'

<use_database>    ::= 'USE' 'IDENTIFIER'

<show_database>   ::= 'SHOW' 'DATABASES'

<create_database> ::= 'CREATE' 'DATABASE' 'IDENTIFIER'

<create_table>    ::= 'CREATE' 'TABLE' 'IDENTIFIER' '(' <columns> ')'

<columns>  ::= <column> <column_list>
             | ',' <column> <column_list>

<column_list>  ::= ',' <column> <column_list>   
                 | ',' <column>
                 | ''

<column>   ::= 'IDENTIFIER' <data_type> <constraints>

<data_type>       ::= 'INT' 
                    | 'VARCHAR' '(' NUMBER ')' 
                    | 'DECIMAL' '(' NUMBER ',' NUMBER ')'

<constraints>     ::= <constraint> <constraints>
                    | <constraint> 

<constraint>      ::= 'PRIMARY KEY' 
                    | 'NOT NULL'

<insert_data>     ::= 'INSERT' 'INTO' 'IDENTIFIER' '(' <data_columns> ')' <insert_clause>

<data_columns>    ::= <data> ',' <data_columns>  
                    | <data>

<insert_clause>   ::= 'VALUES' <values_clause>             
                    | 'SELECT' <select_data>

<values_clause>    ::= '(' <datas> ')'
                    | '(' <datas> ')', <values_clause>

<datas>           ::= <datas> ',' <data>
                    | <data>

<data>            ::= 'IDENTIFIER'
                    | "'" 'IDENTIFIER' 'IDENTIFIER' "'"
                    | "'" 'IDENTIFIER' "'"
                    | 'NUMBER'

<select_data>     ::= <select_all>
                    | <simple_select>
                    | <conditional_select>
                    | <ordered_select>

<select_all>      ::= 'SELECT' '*' <from_clause>

<simple_select>   ::= 'SELECT' <data_columns> <from_clause>

<conditional_select> ::= 'SELECT' <data_columns> <from_clause> <where_clause>

<ordered_select>  ::= 'SELECT' <data_columns> <from_clause> <order_by_clause>

<from_clause>     ::= 'FROM' <data>

<order_by_clause> ::= 'ORDER BY' <order_clause>

<order_clause>    ::= <data> ASC
                    | <data> DESC

<delete_data>     ::= <delete_all>
                    | <conditional_delete>
```

