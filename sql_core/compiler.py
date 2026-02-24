from sly import Lexer
from sly import Parser

# =============================================================================
# 1. SQL 词法分析器 (Lexer)
# =============================================================================
class SqlLexer(Lexer):
    tokens = {
        # DDL & DML 关键字
        'CREATE', 'DROP', 'DATABASE', 'DATABASES', 'TABLE', 'SHOW', 'USE',
        'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE', 'FROM', 
        
        # DQL 查询关键字
        'SELECT', 'JOIN', 'LEFT', 'ON', 'WHERE', 'GROUP', 'BY', 'ORDER', 'ASC', 'DESC', 'LIMIT', 'AS',

        # 类型与约束
        'INT', 'FLOAT', 'DOUBLE', 'VARCHAR', 'DECIMAL', 'TIMESTAMP', 'PRIMARY', 'KEY', 'NOT', 'NULL',

        # 逻辑与聚合关键字
        'AND', 'OR', 'IN', 'LIKE', 'COUNT', 'AVG', 'SUM', 'MAX', 'MIN',

        # 基础元素
        'IDENTIFIER', 'NUMBER', 'STRING',
        
        # 复合比较操作符
        'LTE', 'GTE', 'NEQ',
    }

    literals = {'(', ')', ',', '.', '*', '+', '-', '/', '=', '>', '<'}
    ignore = ' \t\n;'

    LTE = r'<='
    GTE = r'>='
    NEQ = r'<>|!='

    @_(r"'[^']*'")
    def STRING(self, t):
        t.value = t.value[1:-1]
        return t

    @_(r'\d+(\.\d+)?')
    def NUMBER(self, t):
        t.value = float(t.value) if '.' in t.value else int(t.value)
        return t

    keyword_map = {
        'CREATE': 'CREATE', 'DROP': 'DROP', 'DATABASE': 'DATABASE', 'DATABASES': 'DATABASES',
        'TABLE': 'TABLE', 'SHOW': 'SHOW', 'USE': 'USE', 'INSERT': 'INSERT', 'INTO': 'INTO',
        'VALUES': 'VALUES', 'UPDATE': 'UPDATE', 'SET': 'SET', 'DELETE': 'DELETE',
        'SELECT': 'SELECT', 'FROM': 'FROM', 'JOIN': 'JOIN', 'LEFT': 'LEFT', 'ON': 'ON',
        'WHERE': 'WHERE', 'GROUP': 'GROUP', 'BY': 'BY', 'ORDER': 'ORDER', 'ASC': 'ASC',
        'DESC': 'DESC', 'LIMIT': 'LIMIT', 'AS': 'AS', 'AND': 'AND', 'OR': 'OR', 'IN': 'IN',
        'LIKE': 'LIKE', 'COUNT': 'COUNT', 'AVG': 'AVG', 'SUM': 'SUM', 'MAX': 'MAX', 'MIN': 'MIN',
        'INT': 'INT', 'FLOAT': 'FLOAT', 'DOUBLE': 'DOUBLE', 'VARCHAR': 'VARCHAR',
        'DECIMAL': 'DECIMAL', 'TIMESTAMP': 'TIMESTAMP',
        'PRIMARY': 'PRIMARY', 'KEY': 'KEY', 'NOT': 'NOT', 'NULL': 'NULL'
    }

    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def IDENTIFIER(self, t):
        t.type = self.keyword_map.get(t.value.upper(), 'IDENTIFIER')
        return t

    def error(self, t):
        print(f"Lexical error: Unrecognized character '{t.value[0]}' (Position: {self.index})")
        self.index += 1


# =============================================================================
# 2. SQL 语法分析器 (Parser)
# =============================================================================
class SqlParser(Parser):
    tokens = SqlLexer.tokens
    debugfile = 'parser.out'

    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', '=', '>', '<', 'LTE', 'GTE', 'NEQ', 'LIKE'),
        ('left', '+', '-'),
        ('left', '*', '/'),
    )

    def __init__(self, db=None):
        self.db = db

    def error(self, p):
        if p:
            raise SyntaxError(f"Syntax error: Unexpected token '{p.value}' (Type: {p.type}, Line: {p.lineno})")
        else:
            raise SyntaxError("Syntax error: Unexpected end of statement (EOF)")

    @_('create_database', 'drop_database', 'show_databases', 'use_database',
       'create_table', 'drop_table', 
       'insert_data', 'update_data', 'delete_data', 'select_data')
    def statement(self, p): return p[0]

    # --- DDL ---
    @_('CREATE DATABASE IDENTIFIER')
    def create_database(self, p): return {"type": "create_database", "database_name": p.IDENTIFIER}

    @_('DROP DATABASE IDENTIFIER')
    def drop_database(self, p): return {"type": "drop_database", "database_name": p.IDENTIFIER}

    @_('SHOW DATABASES')
    def show_databases(self, p): return {"type": "show_databases"}

    @_('USE IDENTIFIER')
    def use_database(self, p): return {"type": "use_database", "database_name": p.IDENTIFIER}

    @_('CREATE TABLE IDENTIFIER "(" column_defs ")"')
    def create_table(self, p): return {"type": "create_table", "table_name": p.IDENTIFIER, "columns": p.column_defs}

    @_('DROP TABLE IDENTIFIER')
    def drop_table(self, p): return {"type": "drop_table", "table_name": p.IDENTIFIER}

    @_('column_defs "," column_def')
    def column_defs(self, p): return p.column_defs + [p.column_def]

    @_('column_def')
    def column_defs(self, p): return [p.column_def]

    @_('IDENTIFIER data_type opt_constraints')
    def column_def(self, p): return {"name": p.IDENTIFIER, "data_type": p.data_type, "constraints": p.opt_constraints}

    @_('INT', 'FLOAT', 'DOUBLE', 'TIMESTAMP')
    def data_type(self, p): return p[0].lower()

    @_('VARCHAR "(" NUMBER ")"')
    def data_type(self, p): return f"varchar({p.NUMBER})"

    @_('DECIMAL "(" NUMBER "," NUMBER ")"')
    def data_type(self, p): return f"decimal({p[2]},{p[4]})"

    @_('constraint opt_constraints')
    def opt_constraints(self, p): return [p.constraint] + p.opt_constraints

    @_('constraint')
    def opt_constraints(self, p): return [p.constraint]

    @_('')
    def opt_constraints(self, p): return []

    @_('PRIMARY KEY', 'NOT NULL')
    def constraint(self, p): return f"{p[0]} {p[1]}".lower()

    # --- DML ---
    @_('INSERT INTO IDENTIFIER "(" ident_list ")" VALUES values_list')
    def insert_data(self, p): return {"type": "insert", "table_name": p.IDENTIFIER, "columns": p.ident_list, "values": p.values_list}

    @_('UPDATE IDENTIFIER SET assignment_list opt_where')
    def update_data(self, p): return {"type": "update", "table_name": p.IDENTIFIER, "assignments": p.assignment_list, "where": p.opt_where}

    @_('DELETE FROM IDENTIFIER opt_where')
    def delete_data(self, p): return {"type": "delete", "table_name": p.IDENTIFIER, "where": p.opt_where}

    @_('ident_list "," IDENTIFIER')
    def ident_list(self, p): return p.ident_list + [p.IDENTIFIER]

    @_('IDENTIFIER')
    def ident_list(self, p): return [p.IDENTIFIER]

    # 🌟 新增：支持带点号引用的列表 (如 e.id, d.name)
    @_('ref_list "," identifier_ref')
    def ref_list(self, p):
        return p.ref_list + [p.identifier_ref]

    @_('identifier_ref')
    def ref_list(self, p):
        return [p.identifier_ref]

    @_('values_list "," "(" expr_list ")"')
    def values_list(self, p): return p.values_list + [p.expr_list]

    @_('"(" expr_list ")"')
    def values_list(self, p): return [p.expr_list]

    @_('assignment_list "," IDENTIFIER "=" expr')
    def assignment_list(self, p): return p.assignment_list + [{"column": p.IDENTIFIER, "value": p.expr}]

    @_('IDENTIFIER "=" expr')
    def assignment_list(self, p): return [{"column": p.IDENTIFIER, "value": p.expr}]

    # --- DQL & JOIN ---
    @_('SELECT select_list FROM table_source opt_join opt_where opt_group_by opt_order_by opt_limit')
    def select_data(self, p):
        return {
            "type": "select",
            "select_list": p.select_list,
            "table_source": p.table_source,
            "join": p.opt_join,
            "where": p.opt_where,
            "group_by": p.opt_group_by,
            "order_by": p.opt_order_by,
            "limit": p.opt_limit
        }

    @_('"*"')
    def select_list(self, p): return ["*"]

    @_('expr_list')
    def select_list(self, p): return p.expr_list

    @_('IDENTIFIER IDENTIFIER', 'IDENTIFIER AS IDENTIFIER')
    def table_ref(self, p): return {"table": p[0], "alias": p[len(p)-1]}

    @_('IDENTIFIER')
    def table_ref(self, p): return {"table": p.IDENTIFIER, "alias": None}

    @_('table_ref')
    def table_source(self, p): return p.table_ref

    @_('opt_join JOIN table_ref ON expr')
    def opt_join(self, p): return p.opt_join + [{"type": "INNER", "table": p.table_ref, "on": p.expr}]

    @_('opt_join LEFT JOIN table_ref ON expr')
    def opt_join(self, p): return p.opt_join + [{"type": "LEFT", "table": p.table_ref, "on": p.expr}]

    @_('')
    def opt_join(self, p): return []

    @_('WHERE expr')
    def opt_where(self, p): return p.expr

    @_('')
    def opt_where(self, p): return None

# 🌟 修改：由 ident_list 改为 ref_list
    @_('GROUP BY ref_list')
    def opt_group_by(self, p): return p.ref_list

    @_('')
    def opt_group_by(self, p): return None

    @_('ORDER BY order_list')
    def opt_order_by(self, p): return p.order_list

    @_('')
    def opt_order_by(self, p): return None

    @_('LIMIT NUMBER')
    def opt_limit(self, p): return p.NUMBER

    @_('')
    def opt_limit(self, p): return None

    @_('order_list "," identifier_ref ASC', 'order_list "," identifier_ref DESC')
    def order_list(self, p): return p.order_list + [{"column": p.identifier_ref, "direction": p[2]}]

    @_('order_list "," identifier_ref')
    def order_list(self, p): return p.order_list + [{"column": p.identifier_ref, "direction": "ASC"}]

    @_('identifier_ref ASC', 'identifier_ref DESC')
    def order_list(self, p): return [{"column": p.identifier_ref, "direction": p[1]}]

    @_('identifier_ref')
    def order_list(self, p): return [{"column": p.identifier_ref, "direction": "ASC"}]

    # --- Expressions ---
    @_('expr_list "," expr')
    def expr_list(self, p): return p.expr_list + [p.expr]

    @_('expr')
    def expr_list(self, p): return [p.expr]

    @_('expr AND expr', 'expr OR expr')
    def expr(self, p): return {"type": "logical_op", "operator": p[1], "left": p.expr0, "right": p.expr1}

    @_('expr "=" expr', 'expr ">" expr', 'expr "<" expr', 
       'expr LTE expr', 'expr GTE expr', 'expr NEQ expr', 'expr LIKE expr')
    def expr(self, p): return {"type": "compare_op", "operator": p[1], "left": p.expr0, "right": p.expr1}

    @_('expr "+" expr', 'expr "-" expr', 'expr "*" expr', 'expr "/" expr')
    def expr(self, p): return {"type": "math_op", "operator": p[1], "left": p.expr0, "right": p.expr1}

    @_('"(" expr ")"')
    def expr(self, p): return p.expr

    @_('COUNT "(" "*" ")"')
    def expr(self, p): return {"type": "func", "name": "COUNT", "args": "*"}

    @_('AVG "(" expr ")"', 'COUNT "(" expr ")"', 'SUM "(" expr ")"', 'MAX "(" expr ")"', 'MIN "(" expr ")"')
    def expr(self, p): return {"type": "func", "name": p[0], "args": p.expr}

    @_('identifier_ref')
    def expr(self, p): return {"type": "column", "value": p.identifier_ref}

    @_('NUMBER', 'STRING')
    def expr(self, p): return {"type": "literal", "value": p[0]}

    @_('IDENTIFIER "." IDENTIFIER')
    def identifier_ref(self, p): return f"{p.IDENTIFIER0}.{p.IDENTIFIER1}"

    @_('IDENTIFIER')
    def identifier_ref(self, p): return p.IDENTIFIER