import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
from sklearn.model_selection import cross_val_score, RandomizedSearchCV, KFold
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve
from sklearn.utils import resample
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier

df_hoyin = pd.read_csv('/content/pima-indians-diabetes.csv')
df_hoyin.columns = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']
print(df_hoyin.info())
print(df_hoyin.isna().sum())
print(df_hoyin.describe())
print(df_hoyin.select_dtypes(include=object))
print()
print(df_hoyin['class'].value_counts())

transformer_hoyin = StandardScaler()
X = df_hoyin.drop('class', axis=1)
y = df_hoyin['class']
X_train_hoyin, X_test_hoyin, y_train_hoyin, y_test_hoyin = train_test_split(X, y, test_size=0.3, random_state=42)
X_train_prepared = transformer_hoyin.fit_transform(X_train_hoyin)
X_test_prepared = transformer_hoyin.fit_transform(X_test_hoyin)

lr_w = LogisticRegression(max_iter=1400)
rf_w = RandomForestClassifier()
svm_w = SVC()
dt_w = DecisionTreeClassifier(criterion='entropy', max_depth=42)
et_w = ExtraTreesClassifier()

voting_clf = VotingClassifier(
    estimators=
    [
     ('lr', lr_w), 
     ('rf', rf_w), 
     ('svc', svm_w),
     ('dt', dt_w),
     ('et', et_w)
    ],
    voting='hard'
)
for clf in (lr_w, rf_w, svm_w, dt_w, et_w, voting_clf):
    clf.fit(X_train_prepared, y_train_hoyin)
    y_pred = clf.predict(X_test_hoyin)
    print(clf.__class__.__name__)
    print('Actual Value')
    print(y_test_hoyin.values)
    print('Predicted Value')
    print(y_pred)
    print('Accuracy')
    print(accuracy_score(y_test_hoyin, y_pred))

lr_w = LogisticRegression(max_iter=1400)
rf_w = RandomForestClassifier()
svm_w = SVC(probability=True)
dt_w = DecisionTreeClassifier(criterion='entropy', max_depth=42)
et_w = ExtraTreesClassifier()

voting_clf = VotingClassifier(
    estimators=
    [
     ('lr', lr_w), 
     ('rf', rf_w), 
     ('svc', svm_w),
     ('dt', dt_w),
     ('et', et_w)
    ],
    voting='soft'
)
for clf in (lr_w, rf_w, svm_w, dt_w, et_w, voting_clf):
    clf.fit(X_train_prepared, y_train_hoyin)
    y_pred = clf.predict(X_test_hoyin)
    print(clf.__class__.__name__)
    print('Actual Value')
    print(y_test_hoyin.values)
    print('Predicted Value')
    print(y_pred)
    print('Accuracy')
    print(accuracy_score(y_test_hoyin, y_pred))

pipeline1_hoyin = Pipeline(
    [
        ('scaler', transformer_hoyin),
        ('et_clf', et_w)
    ]
)

pipeline2_hoyin = Pipeline(
    [
        ('scaler', transformer_hoyin),
        ('dt_clf', dt_w)
    ]
)

pipeline1_hoyin.fit(X, y)
pipeline2_hoyin.fit(X, y)

cv = KFold(n_splits=10, shuffle=True, random_state=42)
scores_1 = cross_val_score(pipeline1_hoyin, X, y, cv=cv)
scores_2 = cross_val_score(pipeline2_hoyin, X, y, cv=cv)

print('Mean Score for Pipeline1')
print(scores_1.mean())
print()
print('Mean Score for Pipeline2')
print(scores_2.mean())
print()

for pipe in (pipeline1_hoyin, pipeline2_hoyin):
    y_pred = pipe.predict(X_test_hoyin)
    print(f"Accuracy for {pipe}", accuracy_score(y_test_hoyin, y_pred))
    print(f"Precision for {pipe}", precision_score(y_test_hoyin, y_pred))
    print(f"Recall for {pipe}", recall_score(y_test_hoyin, y_pred))
    print(confusion_matrix(y_test_hoyin, y_pred))
    print()

param_44 = {"et_clf__n_estimators": range(10, 3000, 20),
            "et_clf__max_depth": range(1, 1000, 2)}

search_44 = RandomizedSearchCV(
    estimator=pipeline1_hoyin, 
    param_distributions=param_44, 
    scoring='accuracy', cv=5,
    n_iter=7, refit=True, 
    verbose=3)

res = search_44.fit(X_train_hoyin, y_train_hoyin)

print("Best Params:", res.best_params_)
print("Best Score:", res.best_score_)
print()
best_model = res.best_estimator_
ypred_tuned = best_model.predict(X_test_hoyin)
print('Predicted Value by fine tune model:')
print(ypred_tuned)
print()
print(f"Accuracy", accuracy_score(y_test_hoyin, ypred_tuned))
print(f"Precison",precision_score(y_test_hoyin, ypred_tuned))
print(f"Recall", recall_score(y_test_hoyin, ypred_tuned))