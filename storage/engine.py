import pandas as pd


data = {
    'ID': [1, 2, 3],
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35]
}

table_name = 'Person'
df = pd.DataFrame(data)

if __name__ == '__main__':
    print(df)

