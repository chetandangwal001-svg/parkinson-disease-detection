import pandas as pd
import pickle
from pathlib import Path

root = Path('.')
print('cwd', root.resolve())

csv_path = root / 'data.csv'
print('csv exists', csv_path.exists())
df = pd.read_csv(csv_path)
print('columns', list(df.columns))
print('shape', df.shape)
print('first rows', df.head(2).to_dict(orient='records'))

model_path = root / 'model_knn.pkl'
scaler_path = root / 'scaling.pkl'
print('model exists', model_path.exists(), 'scaler exists', scaler_path.exists())
if model_path.exists():
    model = pickle.load(open(model_path, 'rb'))
    print('model', type(model), getattr(model, 'n_features_in_', None), getattr(model, 'classes_', None))
if scaler_path.exists():
    scaler = pickle.load(open(scaler_path, 'rb'))
    print('scaler', type(scaler))
