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
        'IDENTIFIER', 'NUMBER', 'STRING', 'OPERATOR', 'SEPARATOR',
        'CREATE', 'DATABASES', 'DATABASE', 'SHOW', 'USE',
    }

    # 标识符（数据库名，表名，列名等）
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # 常量（数字、字符串）
    NUMBER = r'[0-9]+(\.[0-9]+)?'  # 整数或浮点数
    STRING = r'\'[^\']*\''  # 用单引号括起来的字符串常量

    # 操作符
    OPERATOR = r'(<=|>=|<>|!=|=|<|>|\+|-|\*|/|%)'

    # 分隔符（括号、逗号、点号）
    SEPARATOR = r'[(),.]'

    # SQL 关键字
    CREATE = r'CREATE'
    DATABASES = r'DATABASES'
    DATABASE = r'DATABASE'
    SHOW = r'SHOW'
    USE = r'USE'

    # 忽略空白字符和换行符和行末分号
    ignore = ' ;\t\n'

    # 定义一些未识别字符的错误处理
    def error(self, value):
        print(f"非法字符 '{value.value}'")  # 直接使用 value.value
        self.index += 1


# sql语法分析器
class SqlParser(Parser):
    tokens = SqlLexer.tokens

    def __init__(self, db: DatabaseManager):
        self.db: DatabaseManager = db

    # 解析SQL的语法规则
    @_('SHOW DATABASES')
    def show_databases(self, p):
        return DatabaseManager.show_database()

    # 创建数据库
    @_('CREATE DATABASE IDENTIFIER')
    def create_database(self, p):
        # return DatabaseManager.create_database(p.IDENTIFIER)
        create_database(p.IDENTIFIER)

    # @_('CREATE TABLE IDENTIFIER')
    # def create_table(self, p):

    @_('USE IDENTIFIER')
    def use_database(self, p):
        return self.db.use_database(p.IDENTIFIER)
