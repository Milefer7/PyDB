from algebra.executor import *
from algebra.parser import *

if __name__ == '__main__':
    data_create_database = "CREATE DATABASE test;"

    lexer = SqlLexer()
    parser = SqlParser()  # 创建一个解析器实例

    # 词法分析
    tokens = lexer.tokenize(data_create_database)  # 生成 token

    # 语法分析
    parser.parse(tokens)  # 传递 token 流给解析器

    # # Create（增）：插入数据
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
