from sly import Lexer
from sly import Parser


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
        'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'INSERT', 'INTO', 'VALUES',
        'UPDATE', 'SET', 'DELETE', 'CREATE', 'TABLE', 'DROP', 'JOIN',
        'ON', 'AS', 'ORDER', 'BY', 'GROUP', 'HAVING', 'LIMIT',
        'IDENTIFIER', 'NUMBER', 'STRING', 'OPERATOR', 'SEPARATOR'
    }

    # SQL keywords
    SELECT = r'SELECT'
    FROM = r'FROM'
    WHERE = r'WHERE'
    AND = r'AND'
    OR = r'OR'
    INSERT = r'INSERT'
    INTO = r'INTO'
    VALUES = r'VALUES'
    UPDATE = r'UPDATE'
    SET = r'SET'
    DELETE = r'DELETE'
    CREATE = r'CREATE'
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

    # 标识符（表名、列名等）
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # 常量（数字、字符串）
    NUMBER = r'[0-9]+(\.[0-9]+)?'  # 整数或浮点数
    STRING = r'\'[^\']*\''  # 用单引号括起来的字符串常量

    # 操作符（比较、算术、逻辑）
    OPERATOR = r'[=<>!~%^&|+\-*/]'

    # 分隔符（括号、逗号等）
    SEPARATOR = r'[(),.]'

    # 忽略空白字符和换行符
    ignore = ' \t\n'

    # 定义一些未识别字符的错误处理
    def error(self, value):
        print(f"非法字符 '{value.value}'")  # 直接使用 value.value
        self.index += 1


# # sql语法分析器
# class SqlParser(Parser):
#     tokens = SQLLexer.tokens
#
#     # 解析SQL的语法规则
#     @_('INSERT INTO IDENTIFIER "(" column_list ")" VALUES "(" value_list ")"')
#     def insert(self, p):
#         return ('insert', p.IDENTIFIER, p.column_list, p.value_list)
#
#     @_('SELECT column_list FROM IDENTIFIER WHERE condition')
#     def select(self, p):
#         return ('select', p.column_list, p.IDENTIFIER, p.condition)
#
#     @_('UPDATE IDENTIFIER SET assign_list WHERE condition')
#     def update(self, p):
#         return ('update', p.IDENTIFIER, p.assign_list, p.condition)
#
#     @_('DELETE FROM IDENTIFIER WHERE condition')
#     def delete(self, p):
#         return ('delete', p.IDENTIFIER, p.condition)
#
#     @_('IDENTIFIER "=" value')
#     def condition(self, p):
#         return ('condition', p.IDENTIFIER, p.value)
#
#     @_('IDENTIFIER "=" value')
#     def assign_list(self, p):
#         return ('assign', p.IDENTIFIER, p.value)
#
#     @_('column_list "," IDENTIFIER')
#     def column_list(self, p):
#         return p.column_list + [p.IDENTIFIER]
#
#     @_('IDENTIFIER')
#     def column_list(self, p):
#         return [p.IDENTIFIER]
#
#     @_('value_list "," value')
#     def value_list(self, p):
#         return p.value_list + [p.value]
#
#     @_('value')
#     def value_list(self, p):
#         return [p.value]
#
#     @_('NUMBER')
#     def value(self, p):
#         return int(p.NUMBER)
#
#     @_('STRING')
#     def value(self, p):
#         return p.STRING


if __name__ == '__main__':
    # Create（增）：插入数据
    data_c1 = "INSERT INTO users (name, age, city) VALUES ('John', 25, 'New York');"
    # Read（查）：查询数据
    data_r1 = "SELECT name, age FROM users WHERE age > 30 AND city = 'New York';"
    # Update（改）：更新数据
    data_u1 = "UPDATE users SET age = 26 WHERE name = 'John';"
    # Delete（删）：删除数据
    data_d1 = "DELETE FROM users WHERE age < 20;"

    lexer = SqlLexer()
    for tok in lexer.tokenize(data_c1):
        print('type=%r, value=%r' % (tok.type, tok.value))
