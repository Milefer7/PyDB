from sly import Lexer
from sly import Parser
from .executor import *


# 关系代数词法分析器
class AlgebraLexer(Lexer):
    # Regular expression rules for tokens
    tokens = {
        OPERATION, IDENTIFIERS, SEPARATORS, CONSTANTS
    }

    OPERATION = r'[σπ×∪−]'  # 运算符：五中基本运算
    IDENTIFIERS = r'[a-zA-Z][a-zA-Z0-9]*'  # 标识符
    SEPARATORS = r'[,()]'  # 分隔符
    CONSTANTS = r'[0-9]+(\.[0-9]+)?|\'[^\']*\''  # 数字或者’xxx‘

    # String containing ignored characters between tokens
    ignore = ' \t'


# sql词法分析器
class SqlLexer(Lexer):
    # Regular expression rules for tokens
    tokens = {
        'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'NOT', 'INSERT', 'INTO', 'VALUES',
        'UPDATE', 'SET', 'DELETE', 'CREATE', 'TABLE', 'DROP', 'JOIN',
        'ON', 'AS', 'ORDER', 'BY', 'GROUP', 'HAVING', 'LIMIT',
        'IDENTIFIER', 'NUMBER', 'STRING', 'OPERATOR', 'SEPARATOR', 'DESC', 'CREATE',
        'DATABASE'
    }

    # SQL keywords
    CREATE = r'CREATE'
    DATABASE = r'DATABASE'
    SELECT = r'SELECT'
    FROM = r'FROM'
    WHERE = r'WHERE'
    AND = r'AND'
    OR = r'OR'
    NOT = r'NOT'
    INSERT = r'INSERT'
    INTO = r'INTO'
    VALUES = r'VALUES'
    UPDATE = r'UPDATE'
    SET = r'SET'
    DELETE = r'DELETE'
    TABLE = r'TABLE'
    DROP = r'DROP'
    JOIN = r'JOIN'
    ON = r'ON'
    AS = r'AS'
    ORDER = r'ORDER'
    BY = r'BY'
    GROUP = r'GROUP'
    HAVING = r'HAVING'
    LIMIT = r'LIMIT'
    DESC = r'DESC'  # 降序

    # 标识符（数据库名，表名，列名等）
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # 常量（数字、字符串）
    NUMBER = r'[0-9]+(\.[0-9]+)?'  # 整数或浮点数
    STRING = r'\'[^\']*\''  # 用单引号括起来的字符串常量

    # 操作符
    OPERATOR = r'(<=|>=|<>|!=|=|<|>|\+|-|\*|/|%)'

    # 分隔符（括号、逗号、点号）
    SEPARATOR = r'[(),.]'

    # 忽略空白字符和换行符和行末分号
    ignore = ' ;\t\n'

    # 定义一些未识别字符的错误处理
    def error(self, value):
        print(f"非法字符 '{value.value}'")  # 直接使用 value.value
        self.index += 1


# sql语法分析器
class SqlParser(Parser):
    tokens = SqlLexer.tokens

    # 解析SQL的语法规则

    # 创建数据库
    @_('CREATE DATABASE IDENTIFIER')
    def create_database(self, p):
        executor_create_database(p.IDENTIFIER)
