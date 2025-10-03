import pandas as pd


multiplication_table = pd.DataFrame(
    [i * 2 for i in range(1, 11)],
    index=range(1, 11),
    columns=[2]
)
print('Таблица умножения на 2', '\n', multiplication_table.T)

# multiplication_table = pd.DataFrame(
#     [[i * j for j in range(1, 11)] for i in range(1, 11)],
#     index=range(1, 11),
#     columns=range(1, 11)
# )

# print(multiplication_table)