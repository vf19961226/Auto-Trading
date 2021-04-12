# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 01:23:13 2021

@author: vf199
"""

import argparse
import MyLogic

parser=argparse.ArgumentParser()
parser.add_argument("--training",default="./data/training.csv",help="Input your training data.")
parser.add_argument("--testing",default="./data/testing.csv",help="Input your testing data.")
parser.add_argument("--output",default="./output.csv",help="Output your result.")
args=parser.parse_args()


data = MyLogic.load_csv(args.training)
        
all_price = MyLogic.get_price(data)
spread = MyLogic.get_spread(all_price)
sum_spread = MyLogic.get_sum_spread(spread)
output = MyLogic.mylogic(spread, sum_spread)
output = MyLogic.final_day(output) #最後一天強制出清後結算的收益
output = MyLogic.testing_first_day(output)#假設testing第一天為0
MyLogic.creat_csv(output, "./data/label.csv")

#------------------Training-------------------
import pandas as pd
from keras.models import Sequential
import keras
import numpy as np
from pandas import DataFrame
from tensorflow.keras.models import load_model
from keras.layers import Dense, LSTM
from keras.callbacks import EarlyStopping


label = pd.read_csv("./data/label.csv",names=["Label"])

def readTrain():
  #train = pd.read_csv("./data/training.csv",names=["Open", "High", "Low", "Close"]) 
  train = pd.read_csv(args.training,names=["Open", "High", "Low", "Close"]) 
  return train

#正規化
def normalize(train):
  train_norm = train.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))
  train_norm = pd.concat([train_norm,label],axis=1)
  
  return train_norm

#建立訓練data
def buildTrain(train,pastDay,futureDay):
    X_train, Y_train = [], []
    for i in range(train.shape[0]-futureDay-pastDay):
      X_train.append(np.array(train.iloc[i:i+pastDay])) #分割訓練集      
      Y_train.append(np.array(train.iloc[i+pastDay:i+pastDay+futureDay]["Label"])) #分割輸出label

    Y_train = keras.utils.to_categorical(Y_train, 3)
    return np.array(X_train), np.array(Y_train)
def splitData(X,Y,rate):
  X_train = X[int(X.shape[0]*rate):]
  
  Y_train = Y[int(Y.shape[0]*rate):]
  X_val = X[:int(X.shape[0]*rate)]

  Y_val = Y[:int(Y.shape[0]*rate)]
  return X_train, Y_train, X_val, Y_val    

# read SPY.csv
train = readTrain()
# Normalization
train_norm = normalize(train)

# build Data, use last 20 days to predict next 1 days
X_train, Y_train, = buildTrain(train_norm, 20, 1)

# split training data and validation data
X_train, Y_train,X_val, Y_val,  = splitData(X_train, Y_train, 0.1)

#build Model
def buildManyToManyModel(shape):

  model = Sequential()
  model.add(LSTM(5, input_length=shape[1], input_dim=shape[2], return_sequences=False))
  model.add(Dense(3))
  model.compile(loss="mse", optimizer="adam")
  model.summary()
  return model

#Star training
model = buildManyToManyModel(X_train.shape)
callback = EarlyStopping(monitor="loss", patience=10, verbose=1, mode="auto")

history=model.fit(X_train, Y_train, epochs=1000, batch_size=128, validation_data=(X_val, Y_val), callbacks=[callback])

model.save('./LSTM_New.h5')

#------------------Predict-------------------

predict_data = pd.read_csv(args.training, names=["Open", "High", "Low", "Close"])

testing=pd.read_csv(args.testing, names=["Open", "High", "Low", "Close"])



model_predict = load_model('./LSTM_New.h5')
label_dict={0:"nothing",1:"buy",2:"sell"}  #轉換標籤為類別名稱用 
print(len(predict_data))
print(len(testing))


#正規化
def normalize_predict(train):
  predict_norm = train.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))
  predict_norm = pd.concat([predict_norm,label],axis=1)
  return predict_norm
  

def buildpredict(data):        
    dataforpredict.append(np.array(data.iloc[data.shape[0]-20:data.shape[0]]))
    return np.array(dataforpredict)
def label_for_predict(data2):
    label_predicet.append(np.array(data2.iloc[data2.shape[0]-20:data2.shape[0]]))
    return np.array(label_predicet)


for i in range(len(testing)-1):
  dataforpredict = []
  label_predicet = []

  #加上預測 
  train=predict_data.append(testing[:(i+1)]) 
  train=train.reset_index(drop=True)#數字重新編排

  #Normalization
  predict_norm = normalize_predict(train) #數據nomalize＋label

  dataforpredict = buildpredict(predict_norm) #切割最後20比
 
  prediction=model_predict.predict_classes(dataforpredict)

  insert=DataFrame(prediction,columns=['Label'])
  label = label.append(insert)
  label=label.reset_index(drop=True)

print(type(label))


result=[]
result.append(np.array(label.iloc[label.shape[0]-(len(testing)-1):label.shape[0]]))
result = np.array(result, np.int32)

result[result==2] = -1
result = result.reshape(-1,1)
print(result.shape)
print(result)

output_csv = []
for i in result:
    output_csv.append(i[0])
    
MyLogic.creat_csv(output_csv, args.output) #將結果輸出CSV檔