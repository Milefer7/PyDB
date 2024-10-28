from sly import Lexer
from sly import Parser
from .executor import *


# SQL 词法分析器
class SqlLexer(Lexer):
    # 正则表达式规则

    tokens = {
        # 主关键词
        CREATE, SELECT, SHOW, USE,
        # 关键词
        IDENTIFIER, DATABASES,  DATABASE, ORDER, WHERE, LIMIT, PRIMARY_KEY, NOT_NULL, NUMBER, OPERATOR,
        # 逻辑表达符
        DESC, FROM, TABLE, ASC, AND, OR,
        # 类型
        TIMESTAMP, DOUBLE, INT, VARCHAR, DECIMAL, FLOAT,

    }
    literals = {'(', ')', '{', '}', ','}

    # SQL 关键字
    PRIMARY_KEY = r'PRIMARY KEY'
    NOT_NULL = r'NOT NULL'
    # 标识符（数据库名、表名、列名等）
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    IDENTIFIER['DATABASES'] = DATABASES
    IDENTIFIER['VARCHAR'] = VARCHAR
    IDENTIFIER['DECIMAL'] = DECIMAL
    IDENTIFIER['CREATE'] = CREATE
    IDENTIFIER['SELECT'] = SELECT
    IDENTIFIER['DATABASE'] = DATABASE
    IDENTIFIER['ORDER'] = ORDER
    IDENTIFIER['WHERE'] = WHERE
    IDENTIFIER['LIMIT'] = LIMIT
    IDENTIFIER['FLOAT'] = FLOAT
    IDENTIFIER['DOUBLE'] = DOUBLE
    IDENTIFIER['DESC'] = DESC
    IDENTIFIER['FROM'] = FROM
    IDENTIFIER['TABLE'] = TABLE
    IDENTIFIER['SHOW'] = SHOW
    IDENTIFIER['USE'] = USE
    IDENTIFIER['INT'] = INT
    IDENTIFIER['ASC'] = ASC
    IDENTIFIER['AND'] = AND
    IDENTIFIER['OR'] = OR

    # 常量（数字、字符串）
    NUMBER = r'[0-9]+(\.[0-9]+)?'  # 整数或浮点数

    # 操作符（比较符号和数学运算符）
    OPERATOR = r'(<=|>=|<>|!=|=|<|>|\+|-|\*|/|%)'

    # 忽略空白字符和换行符、行末分号
    ignore = ' ;\t\n'

    # 错误处理：未识别的字符
    def error(self, value):
        print(f"非法字符 '{value.value[0]}'，当前索引位置：{self.index}")
        self.index += 1


# SQL 语法分析器
# class SqlParser(Parser):
#     tokens = SqlLexer.tokens
#
#     def __init__(self, db):
#         self.db = db
#
#     # 使用数据库
#     @_('USE IDENTIFIER')
#     def use_database(self, p):
#         return {"type": "use_database", "database_name": p.IDENTIFIER}
#
#     # 创建数据库
#     @_('CREATE DATABASE IDENTIFIER')
#     def create_database(self, p):
#         return {"type": "create_database", "database_name": p.IDENTIFIER}
#
#     # 显示数据库
#     @_('SHOW DATABASES')
#     def show_databases(self, p):
#         return {"type": "show_databases"}
#
#     # 创建表
#     @_('CREATE TABLE IDENTIFIER COLUMNS')
#     def create_table(self, p):
#         return {"type": "create_table", "table_name": p.IDENTIFIER, "columns": [p.COLUMNS]}
#
#     # PRIMARY KEY NOT NULL二合一
#     @_('CONSTRAINTS CONSTRAINTS')
#     def constraints(self, p):
#         # 合并两个 CONSTRAINTS 的值
#         combined_value = f"{p.CONSTRAINTS[0]} {p.CONSTRAINTS[1]}"
#         return 'CONSTRAINTS', combined_value
#
#     # 规约 eg. id INT PRIMARY KEY NOT NULL
#     @_('IDENTIFIER DATA_TYPE CONSTRAINTS')
#     def to_column_v1(self, p):
#         return 'COLUMN', {
#             "name": p.IDENTIFIER,
#             "type": p.DATA_TYPE,
#             "constraints": [p.CONSTRAINTS]
#         }
#
#     @_('IDENTIFIER DATA_TYPE')
#     def to_column_v2(self, p):
#         tok = next(self.tokens, None)
#         if tok != 'LEFT_PARENTHESIS' or tok != 'CONSTRAINTS':
#             return 'COLUMN', p[0] + ' ' + +p[1]
#
#     # eg. VARCHAR(100)
#     @_('DATA_TYPE LEFT_PARENTHESIS NUMBER RIGHT_PARENTHESIS')
#     def data_type(self, p):
#         combined_value = f"{p.CONSTRAINTS[0]}({p.NUMBER})"
#         return 'DATA_TYPE', combined_value
#
#     @_('DATA_TYPE LEFT_PARENTHESIS NUMBER NUMBER RIGHT_PARENTHESIS')
#     def data_type(self, p):
#         combined_value = f"{p.CONSTRAINTS[0]}({p[2]},{p[3]})"
#         return 'DATA_TYPE', combined_value
#
#     # 规约 eg. DECIMAL+(10, 2), -> DECIMAL(10, 2),
#     @_('IDENTIFIER LEFT_PARENTHESIS COLUMN IDENTIFIER DATA_TYPE')
#     def data_type(self, p):
#         return p.DATA_TYPE(p[2], p[4])
#
#     @_('LEFT_PARENTHESIS COLUMNS RIGHT_PARENTHESIS')
#     def columns_group(self, p):
#         return 'COLUMNS', p.COLUMNS
#
#     @_('COLUMN')
#     def columns_single(self, p):
#         return 'COLUMNS', [p.COLUMN]  # 返回一个单一的 COLUMN 列表
#
#     @_('COLUMN COLUMNS')
#     def columns_multiple(self, p):
#         return [p.COLUMN] + p.COLUMNS  # 返回多个 COLUMN 的列表
