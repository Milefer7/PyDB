# 专管 AST 转 Pandas 的向量化计算
from tabulate import tabulate
import pandas as pd

class Executor:
    @staticmethod
    def eval_value(expr_node):
        if not expr_node: return None
        return expr_node.get("value") if expr_node.get("type") in ("literal", "column") else None

    @staticmethod
    def build_query_string(expr_node):
        if not expr_node: return ""
        node_type = expr_node.get("type")
        
        if node_type == "logical_op":
            op = "and" if expr_node.get("operator").upper() == "AND" else "or"
            return f"({Executor.build_query_string(expr_node.get('left'))} {op} {Executor.build_query_string(expr_node.get('right'))})"
            
        elif node_type == "compare_op":
            # 1. 提取原始操作符并转大写，提取左侧列名
            op = expr_node.get("operator").upper()
            left = Executor.build_query_string(expr_node.get("left"))
            
            # 核心修改点：单独拦截并转译 LIKE 操作符
            if op == "LIKE":
                right_node = expr_node.get("right")
                raw_val = right_node.get("value")
                
                # 将 SQL 的模糊匹配转为 Python 正则表达式
                # % 变成 .* (匹配任意多个字符)
                # _ 变成 .  (匹配单个字符)
                # ^ 和 $ 用于锚定字符串的首尾，确保精确匹配
                regex_pattern = f"^{str(raw_val).replace('%', '.*').replace('_', '.')}$"
                
                # 返回 Pandas 特有的 Series.str.match() 语法
                return f"{left}.str.match('{regex_pattern}', na=False)"
                
            # 2. 如果不是 LIKE，走常规的数学比较逻辑 (>, <, ==, !=)
            else:
                right = Executor.build_query_string(expr_node.get("right"))
                if op == "=": op = "=="
                elif op in ("<>", "!="): op = "!="
                return f"{left} {op} {right}"
                
        # 👇 新增这一块：让翻译器支持数学运算 (math_op)
        elif node_type == "math_op":
            left = Executor.build_query_string(expr_node.get("left"))
            right = Executor.build_query_string(expr_node.get("right"))
            op = expr_node.get("operator")
            return f"({left} {op} {right})"
            
        elif node_type == "column": 
            # 🌟 核心修改点：用反引号包围列名！
            # 将 "c.id" 变成 "`c.id`"，解决 Pandas 无法识别带点号列名的问题
            return f"`{expr_node.get('value')}`"
            
        elif node_type == "literal":
            val = expr_node.get("value")
            return f"'{val}'" if isinstance(val, str) else str(val)
            
        return ""

    @staticmethod
    def execute_delete(df, where_ast):
        if not where_ast: return df.iloc[0:0]
        return df.drop(df.query(Executor.build_query_string(where_ast)).index)

    
    @staticmethod
    def execute_update(df, assignments, where_ast):
        # 1. 确定需要更新的行索引
        if where_ast:
            query_str = Executor.build_query_string(where_ast)
            target_indices = df.query(query_str).index
        else:
            target_indices = df.index

        # 2. 执行向量化更新
        for assign in assignments:
            col_name = assign.get("column")
            value_ast = assign.get("value")
            
            # 魔法：把 AST 转成字符串，例如 "(salary + 5000)"
            expr_str = Executor.build_query_string(value_ast)
            
            try:
                # 极度优雅：利用 Pandas 原生的 eval() 执行向量化计算！
                computed_series = df.loc[target_indices].eval(expr_str)
                df.loc[target_indices, col_name] = computed_series
            except Exception as e:
                # 兜底方案：退回使用 eval_value 取字面量
                df.loc[target_indices, col_name] = Executor.eval_value(value_ast)
                
        # 返回更新后的 DataFrame 和 受影响的行数
        return df, len(target_indices)


    @staticmethod
    def execute_select(df, sql_tree, db_path="."): # 💡 新增 db_path 参数用于读取右表
        # ==========================================================
        # [核心新增]：处理多表 JOIN 与别名命名空间隔离
        # ==========================================================
        join_list = sql_tree.get("join")
        if join_list:
            # 1. 给主表的所有列加上前缀 (把 'id' 变成 'c.id')
            table_info = sql_tree.get("table_source")
            main_table = table_info.get("table")
            main_alias = table_info.get("alias")
            main_prefix = main_alias if main_alias else main_table
            
            df = df.rename(columns=lambda x: f"{main_prefix}.{x}")
            
            # 2. 循环处理每一个 JOIN
            for j in join_list:
                r_table_info = j.get("table")
                r_table = r_table_info.get("table")
                r_alias = r_table_info.get("alias")
                r_prefix = r_alias if r_alias else r_table
                
                # 加载右表数据，并加上前缀 (把 'amount' 变成 'o.amount')
                import os
                right_df = pd.read_csv(os.path.join(db_path, f"{r_table}.csv"))
                right_df = right_df.rename(columns=lambda x: f"{r_prefix}.{x}")
                
                # 解析连接条件 (例如 c.id = o.customer_id)
                on_cond = j.get("on")
                left_col = on_cond.get("left").get("value")
                right_col = on_cond.get("right").get("value")
                
                join_type = "left" if j.get("type").upper() == "LEFT" else "inner"
                
                # 执行 Pandas 底层的极速矩阵合并
                df = pd.merge(df, right_df, left_on=left_col, right_on=right_col, how=join_type)

        # ==========================================================
        # 原有逻辑：条件过滤、排序、分组、截断及聚合计算
        # ==========================================================
        # 条件过滤
        where_ast = sql_tree.get("where")
        if where_ast: 
            query_str = Executor.build_query_string(where_ast)
            df = df.query(query_str)

        # 排序
        order_ast = sql_tree.get("order_by")
        if order_ast: 
            df = df.sort_values(
                by=[i.get("column") for i in order_ast], 
                ascending=[i.get("direction").upper() == "ASC" for i in order_ast]
            )

        # 分组去重
        group_by_ast = sql_tree.get("group_by")
        if group_by_ast:
            df = df.drop_duplicates(subset=group_by_ast)

        # 截断
        limit_ast = sql_tree.get("limit")
        if limit_ast: 
            df = df.head(int(limit_ast))

        # 投影与聚合
        select_list_ast = sql_tree.get("select_list")
        if select_list_ast != ["*"]:
            display_columns = []
            agg_funcs = []
            
            # [核心修改点 1]：分离普通列和聚合函数
            for item in select_list_ast:
                if item.get("type") == "column":
                    display_columns.append(item.get("value"))
                elif item.get("type") == "func":
                    agg_funcs.append(item)
            
            if agg_funcs:
                # [核心修改点 2]：触发聚合计算分支 (Aggregation Engine)
                result_dict = {}
                for agg in agg_funcs:
                    func_name = agg.get("name").upper()
                    args = agg.get("args")
                    
                    # 确定要显示的表头名称，例如 "COUNT(*)" 或 "AVG(salary)"
                    if args == "*":
                        display_name = f"{func_name}(*)"
                        target_col = None
                    else:
                        # 对于 df['列名'] 取值，直接拿原始纯文本字符串即可，绝对不能带反引号！
                        target_col = args.get("value") if isinstance(args, dict) else args
                        display_name = f"{func_name}({target_col})"
                    
                    # 极速向量化计算
                    if df.empty:
                        # 如果过滤后没数据了，COUNT 是 0，其他全是空值 (None)
                        result_dict[display_name] = 0 if func_name == "COUNT" else None
                    elif func_name == "COUNT":
                        result_dict[display_name] = len(df) if args == "*" else df[target_col].count()
                    elif func_name == "AVG":
                        result_dict[display_name] = df[target_col].mean()
                    elif func_name == "SUM":
                        result_dict[display_name] = df[target_col].sum()
                    elif func_name == "MAX":
                        result_dict[display_name] = df[target_col].max()
                    elif func_name == "MIN":
                        result_dict[display_name] = df[target_col].min()
                
                # 将聚合结果字典转化为只有一行数据的 DataFrame
                df = pd.DataFrame([result_dict])
            else:
                # 只有在这时，列名是精确匹配类似 'c.username' 的
                df = df[display_columns]

        # 5. 格式化输出终端表格
        if df.empty:
            print("Empty set")
        else:
            from tabulate import tabulate
            print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
            print(f"{len(df)} row(s) in set.")
        # df.to_csv("./test/golden_data/query_result.csv", index=False, encoding='utf-8')
        return df # 建议把处理完的 df return 回去，方便测试框架做断言