import pandas as pd

df = pd.read_csv('data.csv')
print('Dataset shape:', df.shape)
print('\nClass distribution:')
print(df['status'].value_counts().sort_index())
print(f'\nParkinson cases: {(df["status"] == 1).sum()}')
print(f'Healthy cases: {(df["status"] == 0).sum()}')
print(f'Ratio (Parkinsons/Healthy): {(df["status"] == 1).sum() / (df["status"] == 0).sum():.2f}')
