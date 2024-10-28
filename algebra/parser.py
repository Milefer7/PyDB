from sly import Lexer
from sly import Parser
from .executor import *


# SQL 词法分析器
class SqlLexer(Lexer):
    # 正则表达式规则

    tokens = {
        'DATABASES', 'DATABASE', 'SHOW', 'USE',

        'CREATE', "TABLE", "COLUMNS",

        'SELECT', 'SELECT_CLAUSE',
        'FROM', 'FROM_CLAUSE',
        'WHERE', 'WHERE_CLAUSE', 'AND', 'OR',
        'ORDER', 'ORDER_BY_CLAUSE', 'ASC', 'DESC', 'BY',
        'LIMIT', 'LIMIT_CLAUSE',

        'CONSTRAINTS', 'DATA_TYPE', 'IDENTIFIER', 'OPERATOR', 'NUMBER', 'STRING',
        'LEFT_PARENTHESIS', 'RIGHT_PARENTHESIS'
    }

    # SQL 关键字
    CONSTRAINTS = r'(?:PRIMARY\s+KEY(?:\s+NOT\s+NULL)?|NOT\s+NULL(?:\s+PRIMARY\s+KEY)?)'  # 限制条件-只要主键和不空

    # 定义数据类型，包括 VARCHAR 但不包括长度限制
    DATA_TYPE = r'\b(?:INT|FLOAT|DOUBLE|DATE|TIMESTAMP|VARCHAR|DECIMAL)\b'

    USE = r'USE'
    DATABASES = r'DATABASES'
    SHOW = r'SHOW'
    CREATE = r'CREATE'
    DATABASE = r'DATABASE'
    SELECT = r'SELECT'
    FROM = r'FROM'
    WHERE = r'WHERE'
    AND = r'AND'
    OR = r'OR'
    ORDER = r'ORDER'
    BY = r'BY'
    LIMIT = r'LIMIT'
    ASC = r'ASC'
    DESC = r'DESC'
    TABLE = r'TABLE'

    # 标识符（数据库名、表名、列名等）
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # 常量（数字、字符串）
    NUMBER = r'[0-9]+(\.[0-9]+)?'  # 整数或浮点数
    STRING = r'\'[^\']*\''  # 用单引号括起来的字符串常量

    # 操作符（比较符号和数学运算符）
    OPERATOR = r'(<=|>=|<>|!=|=|<|>|\+|-|\*|/|%)'

    # 分隔符（括号、逗号、点号）
    LEFT_PARENTHESIS = r'\('  # 左括号
    RIGHT_PARENTHESIS = r'\)'  # 右括号

    # 忽略空白字符和换行符、行末分号
    ignore = ' ,;\t\n'

    # 错误处理：未识别的字符
    def error(self, value):
        print(f"非法字符 '{value.value[0]}'，当前索引位置：{self.index}")
        self.index += 1


# SQL 语法分析器
class SqlParser(Parser):
    tokens = SqlLexer.tokens

    def __init__(self, db):
        self.db = db

    # 使用数据库
    @_('USE IDENTIFIER')
    def use_database(self, p):
        return {"type": "use_database", "database_name": p.IDENTIFIER}

    # 创建数据库
    @_('CREATE DATABASE IDENTIFIER')
    def create_database(self, p):
        return {"type": "create_database", "database_name": p.IDENTIFIER}

    # 显示数据库
    @_('SHOW DATABASES')
    def show_databases(self, p):
        return {"type": "show_databases"}

    # 创建表
    @_('CREATE TABLE IDENTIFIER COLUMNS')
    def create_table(self, p):
        return {"type": "create_table", "table_name": p.IDENTIFIER, "columns": [p.COLUMNS]}

    # PRIMARY KEY NOT NULL二合一
    @_('CONSTRAINTS CONSTRAINTS')
    def constraints(self, p):
        # 合并两个 CONSTRAINTS 的值
        combined_value = f"{p.CONSTRAINTS[0]} {p.CONSTRAINTS[1]}"
        return 'CONSTRAINTS', combined_value

    # 规约 eg. id INT PRIMARY KEY NOT NULL
    @_('IDENTIFIER DATA_TYPE CONSTRAINTS')
    def to_column_v1(self, p):
        return 'COLUMN', {
            "name": p.IDENTIFIER,
            "type": p.DATA_TYPE,
            "constraints": [p.CONSTRAINTS]
        }

    @_('IDENTIFIER DATA_TYPE')
    def to_column_v2(self, p):
        tok = next(self.tokens, None)
        if tok != 'LEFT_PARENTHESIS' or tok != 'CONSTRAINTS':
            return 'COLUMN', p[0] + ' ' + +p[1]

    # eg. VARCHAR(100)
    @_('DATA_TYPE LEFT_PARENTHESIS NUMBER RIGHT_PARENTHESIS')
    def data_type(self, p):
        combined_value = f"{p.CONSTRAINTS[0]}({p.NUMBER})"
        return 'DATA_TYPE', combined_value

    @_('DATA_TYPE LEFT_PARENTHESIS NUMBER NUMBER RIGHT_PARENTHESIS')
    def data_type(self, p):
        combined_value = f"{p.CONSTRAINTS[0]}({p[2]},{p[3]})"
        return 'DATA_TYPE', combined_value

    # 规约 eg. DECIMAL+(10, 2), -> DECIMAL(10, 2),
    @_('IDENTIFIER LEFT_PARENTHESIS COLUMN IDENTIFIER DATA_TYPE')
    def data_type(self, p):
        return p.DATA_TYPE(p[2], p[4])

    @_('LEFT_PARENTHESIS COLUMNS RIGHT_PARENTHESIS')
    def columns_group(self, p):
        return 'COLUMNS', p.COLUMNS

    @_('COLUMN')
    def columns_single(self, p):
        return 'COLUMNS', [p.COLUMN]  # 返回一个单一的 COLUMN 列表

    @_('COLUMN COLUMNS')
    def columns_multiple(self, p):
        return [p.COLUMN] + p.COLUMNS  # 返回多个 COLUMN 的列表
