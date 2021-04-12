# Auto-Trading
## 簡介
使用由美國那斯達克（Nasdaq）所提供的IBM（International Business Machines Corporation）過去5年的歷史股價作為基礎資料，並基於 **長短期記憶（Long Short-Term Memory，LSTM）** 建立一預測模型，用以預測未來一天的交易狀態，並附有一測試檔案提供測試。在本專案中以追求收益最大化為目標。

## 使用數據
### IBM過去股價
* 資料來源：[**NASDAQ：IBM**](https://www.nasdaq.com/market-activity/stocks/ibm)
* 訓練資料：[**training.csv**](https://github.com/vf19961226/Auto-Trading/blob/main/data/training.csv)
* 測試資料：[**testing.csv**](https://github.com/vf19961226/Auto-Trading/blob/main/data/testing.csv)
* 時間範圍：約為過去5年（2021）
* 說明：資料中分別為每日的開盤價、盤中最高價、盤中最低價、收盤價，並將資料分為訓練資料[**training.csv**](https://github.com/vf19961226/Auto-Trading/blob/main/data/training.csv)以及測試資料[**testing.csv**](https://github.com/vf19961226/Auto-Trading/blob/main/data/testing.csv)，兩者時間範圍分別為5年以上和20天，並且時間連續。    

![testing_CandlestickChart](https://github.com/vf19961226/Auto-Trading/blob/main/figure/testing_CandlestickChart.png "Testing Candlestick Chart")
## 數據預處理
首先決定[**training.csv**](https://github.com/vf19961226/Auto-Trading/blob/main/data/training.csv)的每日交易狀態，並將其結果與[**training.csv**](https://github.com/vf19961226/Auto-Trading/blob/main/data/training.csv)整合作為後續訓練模型所使用之主要資料。
### 決定交易狀態
根據[**training.csv**](https://github.com/vf19961226/Auto-Trading/blob/main/data/training.csv)中每日的開盤價進行決策，使用[**MyLogic.py**](https://github.com/vf19961226/Auto-Trading/blob/main/MyLogic.py)中的邏輯進行決策，目標為追求總收益最大化。

#### 交易規則
1. 每一天只能進行一筆交易，也可以選擇當天不交易
2. 每筆交易以1單位為上限
3. 允許買空賣空
4. 手中持股上限為1單位，下限為-1單位
5. 收益均使用開盤價計算，唯最後一天使用收盤價
6. 最後一天將強制使用收盤價出清手中持股，持有1單位則賣出，持有-1單位則買入，使手中持股歸零

#### 交易狀態
交易狀態主要有**買入**、**不進行交易**、**買入**這三種，並各自有相對應之代碼，如下表所示。本專案最終輸出以此代碼為主。    

|交易狀態|狀態說明
|:---:|:---:
|1|買入1單位
|0|不進行交易
|-1|賣出1單位

#### 交易邏輯
本專案之交易邏輯已被包裝在[**MyLogic.py**](https://github.com/vf19961226/Auto-Trading/blob/main/MyLogic.py)中的**mylogic**。需先使用[**MyLogic.py**](https://github.com/vf19961226/Auto-Trading/blob/main/MyLogic.py)中的**get_spread**以及**get_sum_spread**計算出每日之間漲跌的幅度和漲跌區間總收益以及高點與低點，以利後續進行判別交易狀態。可在[**trader.py**](https://github.com/vf19961226/Auto-Trading/blob/main/trader.py)使用以下指令呼叫**get_spread**、**get_sum_spread**、**mylogic**等功能，如下所示。交易邏輯主要分為**前後皆為連續漲跌區間**、**前段為單一漲跌區間，後段唯連續漲跌區間**、**前後皆為單一漲跌區間**三種狀態進行探討，其中可在細分為比較前後收益多寡、手中持股狀態等問題進行探討。    
```py
import MyLogic

all_price = MyLogic.get_price(data)
spread = MyLogic.get_spread(all_price)
output = MyLogic.mylogic(spread, sum_spread)
```    
* **前後皆為連續漲跌區間**    
此狀態為目前漲跌狀態將會維持超過一天，且達到高點或低點後的漲跌狀態也會維持超過一天。如下圖中A所示。    
* **前段為單一漲跌區間，後段為連續漲跌區間**    
此狀態為目前漲跌狀態將會維持一天，達到高點或低點後的漲跌狀態會維持超過一天。如下圖中B所示。    
* **前後皆為單一漲跌區間**    
此狀態為目前漲跌狀態將會維持一天，且達到高點或低點後的漲跌狀態也會維持一天。如下圖中C所示。    

![status_example](https://github.com/vf19961226/Auto-Trading/blob/main/figure/status_example.png "Status Example")
## 建立預測模型


## 如何使用本專案
### 環境要求    
| Name| Version
|:---:|---:
|Python|3.6.12
|Numpy|1.19.2
|Pandas|1.1.3
|Keras|2.3.1
|tensorflow|2.1.0

可在終端機建立Python版本為3.6.12的環境後使用[**requirements.txt**](https://github.com/vf19961226/Auto-Trading/blob/main/requirements.txt)進行套件包安裝。

    pip install -r requirements.txt
    

### 命令參數    
|Name|Input|Default
|:---:|---|---
|--training|訓練資料|./data/training.csv
|--testing|測試資料|./data/testing.csv
|--label|買賣label|./data/label.csv
|--output|輸出預測結果|./output.csv

環境安裝完成後，可於直接於終端機中執行以下指令，並將參數改成你的參數，或是直接使用我們的預設值而不輸入參數。  

    python trader.py --training "your training data" --testing "your testing data" --output "your output data"

## 買賣預測  

### 匯入資料集並加上表頭
```py
def readTrain():
  train = pd.read_csv("training.csv",names=["Open", "High", "Low", "Close"]) 
  return train
```    

### 定義正規化公式(四項數據訓練完後+加上邏輯算出的Label)
* **先前邏輯所算出的label資料長度=training.csv的資料長度**
* **將label手動新增1 row(其值為0)代表training後的第一天預設不做任何動作**

```py
def normalize(train):
  train_norm = train.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))
  train_norm = pd.concat([train_norm,label],axis=1) #加上label
  return train_norm
```

### 建立訓練用data
* **雖然Label資料長度比training多1，但是依據train.shape下去切割，故不會提取到手動增加的那一列**
* **Y_train以to_categorical處理成one_hot encoding，先前label邏輯輸出為0,1,2就是為了此步**

```py
def buildTrain(train,pastDay,futureDay):
    X_train, Y_train = [], []
    for i in range(train.shape[0]-futureDay-pastDay):
      X_train.append(np.array(train.iloc[i:i+pastDay])) #分割訓練集      
      Y_train.append(np.array(train.iloc[i+pastDay:i+pastDay+futureDay]["Label"])) #分割輸出label

    Y_train = keras.utils.to_categorical(Y_train, 3)
    return np.array(X_train), np.array(Y_train)
```
### 建立模型
1. 輸入層input數量為5項["Open", "High", "Low", "Close","Label"]
2. 平坦層output為3，代表有三種狀態提供輸出
```py
def buildManyToManyModel(shape):
  model = Sequential()
  model.add(LSTM(5, input_length=shape[1], input_dim=shape[2], return_sequences=False))
  model.add(Dense(3))
  model.compile(loss="mse", optimizer="adam")
  model.summary()
  return model
```
![lstm_structure](https://github.com/vf19961226/Auto-Trading/blob/main/figure/lstm_structure.jpg "Instructure_")
### 進行預測
```py
for i in range(len(testing)-1):
  dataforpredict = []
  label_predicet = []
  #加上預測 
  train=predict_data.append(testing[:(i+1)]) #每次只讀取下一筆資料
  train=train.reset_index(drop=True)#數字重新編排(新增的列數表頭會從0開始，故重新編排)
  #Normalization
  predict_norm = normalize_predict(train) #數據nomalize＋label
  dataforpredict = buildpredict(predict_norm) #切割最後20筆(def有先定義)
  prediction=model_predict.predict_classes(dataforpredict)
  insert=DataFrame(prediction,columns=['Label']) #轉變輸出的資料型別
  label = label.append(insert) #將新輸出的Label加入原始label集下方，以便下一天預測
  label=label.reset_index(drop=True)
print(type(label))
```
### 取出預測數據
1.將Label從testing第二天開始提取到最後一天

    result.append(np.array(label.iloc[label.shape[0]-(len(testing)-1):label.shape[0]]))
2.將輸出資料0,1,2轉換為-1,0,1    
3.將資料從三維(1,DAYS,Label)壓回二維(DAYS,Label)
   
    result = result.reshape(-1,1)

### 預測結果
最終預測結果輸出為[**output.csv**](https://github.com/vf19961226/Auto-Trading/blob/main/output.csv)，其內容如下表所示。

| Status
|---
|0
|1
|-1
|1
|0
|0
|0
|0



