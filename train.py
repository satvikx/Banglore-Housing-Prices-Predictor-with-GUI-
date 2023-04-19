#-------------TRAINING THE DATA------------

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score

import pandas as pd
import os
os.chdir(r"C:\Users\v\Desktop\C Lang Tutorials\HPP with GUI\ ")
data = pd.read_csv("Cleaned_Data.csv",index_col=0)

print(data.head())

X = data.drop(columns=['price'])
y = data['price']

X_train, X_test, y_train, y_test =  train_test_split(X, y, test_size = 0.2, random_state = 0)
print(X_train.shape)
print(X_test.shape)

#------------LINEAR REGRESSION, LASSO, RIDGE-------------

ct = make_column_transformer((OneHotEncoder(sparse_output=False), ['location']), remainder = 'passthrough')
scaler = StandardScaler()

# lr = LinearRegression()
# pipe = make_pipeline(ct, scaler, lr)
# pipe.fit(X_train,y_train)
# y_pred_lr = pipe.predict(X_test)
# #print(r2_score(y_test, y_pred_lr))

# lasso = Lasso()
# pipe = make_pipeline(ct, scaler, lasso)
# pipe.fit(X_train, y_train)
# ypd = pipe.predict(X_test)
# #print(r2_score(y_test, ypd))

ridge = Ridge()
pipe = make_pipeline(ct, scaler, ridge)
pipe.fit(X_train, y_train)
ypr = pipe.predict(X_test)
#print(r2_score(y_test, ypr))

import pickle
pickle.dump(pipe, open("RidgeModel.pkl",'wb'))

# pope = pd.read_pickle("RidgeModel.pkl")

# # View the columns in the dataframe
# print(pope)