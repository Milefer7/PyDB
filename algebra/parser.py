from sly import Lexer


class ParserLexer(Lexer):
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


if __name__ == '__main__':
    data = 'π name, department (Employee)'
    lexer = ParserLexer()
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))
