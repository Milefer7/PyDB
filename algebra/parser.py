from sly import Lexer
from sly import Parser
from .executor import *


# sql词法分析器
class SqlLexer(Lexer):
    # Regular expression rules for tokens
    tokens = {
        'USE', 'DATABASES', 'SHOW', 'CREATE', 'DATABASE',
        'IDENTIFIER', 'NUMBER', 'STRING', 'OPERATOR', 'SEPARATOR',

    }

    # SQL keywords
    USE = r'USE'
    DATABASES = r'DATABASES'
    SHOW = r'SHOW'
    CREATE = r'CREATE'
    DATABASE = r'DATABASE'

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
        print(f"非法字符 '{value.value}'，当前索引位置：{self.index}")
        self.index += 1


# sql语法分析器
class SqlParser(Parser):
    tokens = SqlLexer.tokens

    def __init__(self, db):
        self.db = db

    # 解析SQL的语法规则

    # 创建数据库
    # @_('CREATE DATABASE IDENTIFIER')
    # def create_database(self, p):
    #     return DatabaseManager.create_database(p.IDENTIFIER)

    @_('USE IDENTIFIER')
    def use_database(self, p):
        return self.db.select_database(p.IDENTIFIER)

    # @_('SHOW DATABASES')
    # def show_databases(self, p):
    #     return DatabaseManager.show_database()

