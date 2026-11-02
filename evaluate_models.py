import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

FEATURE_COLUMNS = ['MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)', 'MDVP:Shimmer', 'NHR']
df = pd.read_csv('data.csv')
X = df[FEATURE_COLUMNS]
y = df['status']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
scaler = StandardScaler().fit(X_train)
X_train_s = scaler.transform(X_train)
X_test_s = scaler.transform(X_test)

for name, model in [
    ('KNN-7', KNeighborsClassifier(n_neighbors=7)),
    ('Logistic', LogisticRegression(max_iter=2000)),
    ('RandomForest', RandomForestClassifier(n_estimators=200, random_state=42)),
]:
    model.fit(X_train_s, y_train)
    pred = model.predict(X_test_s)
    print('---', name, '---')
    print('Accuracy:', model.score(X_test_s, y_test))
    print('Confusion matrix:')
    print(confusion_matrix(y_test, pred))
    print('Classification report:')
    print(classification_report(y_test, pred, digits=4))
    print()