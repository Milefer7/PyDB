# 专管主键冲突、非空等防呆校验
import pandas as pd

class Validator:
    @staticmethod
    def validate_insert(columns, raw_values_list, schema_df, existing_df, eval_func):
        valid_columns = schema_df['name'].tolist()

        # [校验 0.1] 检查 Unknown column
        for col in columns:
            if col not in valid_columns:
                raise ValueError(f"Error: Unknown column '{col}' in 'field list'.")

        # [校验 0.2] 检查数量错位
        for i, row in enumerate(raw_values_list):
            if len(row) != len(columns):
                raise ValueError(f"Error: Column count doesn't match value count at row {i + 1}.")

        new_df = pd.DataFrame([[eval_func(expr) for expr in row] for row in raw_values_list], columns=columns)
        full_new_df = pd.DataFrame(columns=valid_columns)
        for col in columns:
            full_new_df[col] = new_df[col]

        # [校验 1] 主键冲突
        pk_series = schema_df[schema_df['is_primary_key'] == True]['name']
        if not pk_series.empty:
            pk_col = pk_series.iloc[0]
            if pk_col not in columns:
                raise ValueError(f"Error: Field '{pk_col}' doesn't have a default value.")
            if full_new_df[pk_col].duplicated().any():
                raise ValueError(f"Error: Duplicate entry in the insert list for PRIMARY KEY '{pk_col}'.")
            
            conflict = set(full_new_df[pk_col].dropna().astype(str)).intersection(set(existing_df[pk_col].dropna().astype(str)))
            if conflict:
                raise ValueError(f"Error: Duplicate entry '{list(conflict)[0]}' for PRIMARY KEY '{pk_col}'.")

        # [校验 2] 非空检测
        nn_series = schema_df[schema_df['is_not_null'] == True]['name']
        for nn_col in nn_series:
            if nn_col not in columns or full_new_df[nn_col].isnull().any():
                raise ValueError(f"Error: Field '{nn_col}' cannot be null.")

        return True, full_new_df