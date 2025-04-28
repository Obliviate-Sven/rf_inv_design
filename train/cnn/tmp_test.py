import pandas as pd

# 假设原始文件名为 input.csv
# header=None 表示没有表头
df = pd.read_csv('test.csv', header=None)

# 取前 500 行
df_first_500 = df.head(500)

# 将其保存到新的文件 output.csv，同时不写入表头和索引
df_first_500.to_csv('minitest.csv', header=False, index=False)