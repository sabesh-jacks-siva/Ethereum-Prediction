



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from yahoofinancials import YahooFinancials
import warnings
warnings.filterwarnings('ignore')

df_data=yf.download('ETH-USD',progress=False,auto_adjust=True)
df_data

plt.figure(figsize=(10,6))
plt.grid(True)
plt.xlabel("Date")
plt.ylabel("Close")
plt.plot(df_data['Close'])
plt.title("ETH Price Graph")
plt.show()

df_data.shape

df_data.info()

df=df_data.drop("Volume",axis=1)
df.head(2)

df_data.index.rename('Date', inplace=True)

df=df.sort_values(by=['Date'],ignore_index=True)
df.head()

plt.figure(figsize=(10,6))
plt.grid(True)
plt.xlabel("Date")
plt.ylabel("Close")
plt.plot(df['Close'])
plt.title("ETH Price Graph")
plt.show()

corr=df.corr()
corr

plt.figure(figsize=(20, 7),facecolor="lightgrey",frameon=True,edgecolor='blue')
sns.heatmap(corr, annot=True, cmap='magma');
plt.show()

#STATIONARITY TEST -ADF(ADfuller)
from statsmodels.tsa.stattools import adfuller
ADF_test=adfuller(df["Close"],autolag="AIC")
print(ADF_test)

output=pd.DataFrame(ADF_test[0:4],index=["Test Statistics","p-Value","Lag","number of observation"])
print(output)

df["s1"]=df["Close"]-df['Close'].shift(1)
df.head(15)

plt.figure(figsize=(10,6))
plt.grid(True)
plt.xlabel("Date")
plt.ylabel("s1")
plt.plot(df['s1'])
plt.title("CC Inc s1")
plt.show()

df=df.dropna()
df.head()

df.shape

df.info()

#STATIONARITY TEST -ADF(ADfuller)
from statsmodels.tsa.stattools import adfuller
ADF_test2=adfuller(df["s1"],autolag="AIC")
print(ADF_test2)

output=pd.DataFrame(ADF_test2[0:4],index=["Test Statistics","p-Value","Lag","number of observation"])
print(output)

from statsmodels.tsa.seasonal import seasonal_decompose
# decompose used for checking trend seasonality and error
plt.style.use('ggplot')

result = seasonal_decompose(df['Close'], model='multiplicative', period=100)
fig = plt.figure()
fig = result.plot()
fig.set_size_inches(16, 9)

"""**Train and Test Split**"""

total_count=df.shape
total_count

import math
train_count=math.floor(0.8*total_count[0])
test_count=total_count[0]-train_count
train_count,test_count

Train=df["Close"].loc[:train_count]
Test=df["Close"].loc[(train_count+1):]

Train

Test

plt.plot(Train)
plt.plot(Test)
plt.show()

"""##**SARIMA MODEL**"""

from pmdarima import auto_arima
import warnings
warnings.filterwarnings("ignore")

stepwise_fit = auto_arima(df["s1"], trace=True,suppress_warnings=True)
stepwise_fit.summary()

Test

import statsmodels.api as sm

from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf

plot_pacf(df["s1"]);

plot_acf(df[['s1']]);

model_Sarima = sm.tsa.statespace.SARIMAX(Train,order=(1,0,0),seasonal_order=(1,0,0,12))
result=model_Sarima.fit()

result.summary()

y_pred=result.forecast(steps=test_count)
y_pred=pd.DataFrame(y_pred)
y_pred.shape

y_pred

y_pred["predicted_mean"]

#y_pred.shape

plt.figure(figsize=(15,10))
plt.plot(Train.index,Train,label= 'Training')
plt.plot(Test.index,Test,label= 'Testing')
plt.plot(Test.index,y_pred["predicted_mean"],label= 'future_forecast')
plt.legend()
plt.show()

from sklearn.metrics import mean_squared_error
x_arima=mean_squared_error(Test,y_pred)
x_arima

rmse_arima=x_arima**0.5
rmse_arima

from sklearn.metrics import mean_absolute_percentage_error
mape_arima =mean_absolute_percentage_error(Test,y_pred)*100
print(mape_arima)

"""##**Holt**-**Winters**"""

from statsmodels.tsa.holtwinters import ExponentialSmoothing

model_hw = ExponentialSmoothing(Train,trend="add",seasonal="add", seasonal_periods=100)
fitted_model=model_hw.fit()
y_pred_hw=fitted_model.predict(start=1437,end=1796)

plt.figure(figsize=(15,10))
plt.plot(Train.index,Train,label= 'Training')
plt.plot(Test.index,Test,label= 'Testing')
plt.plot(Test.index,y_pred_hw,label= 'future_forecast')
plt.legend()
plt.show()

from sklearn.metrics import mean_squared_error
x_hw=mean_squared_error(Test,y_pred_hw)
x_hw

if len(Test) > len(y_pred_hw):
    y_pred_hw = np.pad(y_pred_hw, (0, len(Test) - len(y_pred_hw)), 'constant')
else:
    Test = np.pad(Test, (0, len(y_pred_hw) - len(Test)), 'constant')

rmse_hw=x_hw**0.5
rmse_hw

from sklearn.metrics import mean_absolute_percentage_error
mape_hw =mean_absolute_percentage_error(Test,y_pred_hw)*100
print(mape_hw)

"""##**RNN**"""

from keras.models import Sequential

from sklearn.preprocessing import MinMaxScaler

min_max_scaler=MinMaxScaler(feature_range=(0,1))

dataset=min_max_scaler.fit_transform(df_data['Close'].values.reshape(-1,1))

"""**Train and Test split**"""

train_size=int(len(df_data)*0.8)

test_size=len(df_data)-train_size

Train=dataset[0:train_size,:]

Test=dataset[train_size:len(dataset),:]

len(Train)

len(Test)

def create_dataset(dataset,time_step=15):
    x_ind,y_dep =[],[]
    for i in range(len(dataset)-time_step-1):
        a=dataset[i:(i+time_step),0]
        x_ind.append(a)
        y_dep.append(dataset[i+time_step,0])
    return np.array(x_ind),np.array(y_dep)

x_train,y_train=create_dataset(Train,time_step=15)

x_train.shape

x_test,y_test=create_dataset(Test,time_step=15)

y_test.shape

x_test.shape

"""##**LSTM**"""

x_train.shape,x_test.shape

x_train=np.reshape(x_train,(x_train.shape[0],1,x_train.shape[1]))

x_train.shape

x_test=np.reshape(x_test,(x_test.shape[0],1,x_test.shape[1]))

!pip install keras

from keras.layers import Dense, Dropout, Activation
from keras.layers import LSTM

time_step=15
model=Sequential()

model.add(LSTM(20,input_shape=(1,time_step)))
model.add(Dense(1))

model.compile(loss="mean_squared_error",optimizer='adam')

model.fit(x_train,y_train,epochs=100)

y_pred=model.predict(x_test)

x_test.shape

y_pred

y_pred_RNN=min_max_scaler.inverse_transform(y_pred)

y_pred_RNN

y_test=np.expand_dims(y_test,axis=1)

y_test=min_max_scaler.inverse_transform(y_test)

y_test

def plot_pred(test,predicted):
    plt.plot(test,color='red',label='Actual ETH price')
    plt.plot(predicted,color='blue',label="RNN predicted ETH price")
    plt.xlabel('Time')
    plt.ylabel("Price")
    plt.legend()
    plt.show()

plot_pred(y_test,y_pred_RNN)

from sklearn.metrics import mean_squared_error
x_rnn=mean_squared_error(y_test,y_pred_RNN)
x_rnn

rmse_rnn=x_rnn**0.5
rmse_rnn

from sklearn.metrics import mean_absolute_percentage_error
mape_rnn =mean_absolute_percentage_error(y_test,y_pred_RNN)*100
print(mape_rnn)

df1=df_data.drop(["Volume","Open","High","Low"],axis=1)
df1.head(2)

a=300
b=df1[(1796-a):]
b.shape

new_data = df1.iloc[-301:-1]
last60prices=np.array(new_data)

last60prices=last60prices.reshape(-1, 1)

last60prices.shape

X_60=min_max_scaler.transform(last60prices)

NumSamples=20
TimeSteps=15
NumFeatures=1
X_60=X_60.reshape(NumSamples,NumFeatures,TimeSteps)

X_60.shape

x_test.shape

predicted_Price = model.predict(X_60)
predicted_Price = min_max_scaler.inverse_transform(predicted_Price)
predicted_Price

plt.plot(predicted_Price,color='blue',label="RNN predicted ETH price")
plt.xlabel('Time')
plt.ylabel("Price")
plt.legend()
plt.show()

def plot_multi_step(history, prediction1):

    plt.figure(figsize=(15, 6))

    range_history = len(history)
    range_future = list(range(range_history, range_history +
                        len(prediction1)))
    plt.plot(np.arange(range_history), np.array(history),
             label='History')
    plt.plot(range_future, np.array(prediction1),
             label='Forecasted for RNN')

    plt.legend(loc='upper right')
    plt.xlabel('Time step (hour)')
    plt.ylabel('ETH Price')

plot_multi_step(new_data, predicted_Price)

Rmse_data={"model":["ARIMA","HOLT_WINTERS","LSTM"],"Rmse_value":[rmse_arima,rmse_hw,rmse_rnn]}

Rmse_data=pd.DataFrame(Rmse_data)
Rmse_data

plt.figure(figsize=(6,6))
R=sns.barplot(x="Rmse_value",y="model",data=Rmse_data)
for index, row in Rmse_data.iterrows():
    R.text(row.Rmse_value,row.name, round(row.Rmse_value,2), color='Red', ha="center")

MAPE_data={"model":["ARIMA","HOLT_WINTERS","LSTM"],"MAPE_value":[mape_arima,mape_hw,mape_rnn]}

MAPE_data=pd.DataFrame(MAPE_data)
MAPE_data

plt.figure(figsize=(6,6))
M=sns.barplot(x="MAPE_value",y="model",data=MAPE_data)
for index, row in MAPE_data.iterrows():
    M.text(row.MAPE_value,row.name, round(row.MAPE_value,2), color='red', ha="center")

"""

#Web Interface on LSTM using Gradio"""

df2=pd.DataFrame(df_data["Close"]).reset_index()
df2["Date"]=pd.to_datetime(df2["Date"]).dt.date
df3=df2.set_index("Date")
df3

def forecast_ETH_price(no_of_samples):
  a= int(no_of_samples)*15+1
  new_data = df3[-a:-1]
  # print(new_data)
  forecast_dataset=np.array(new_data)
  forecast_dataset=forecast_dataset.reshape(-1, 1)
  X=min_max_scaler.transform(forecast_dataset)
  TimeSteps=int(15)
  NumFeatures=int(1)
  No_of_samples=int(no_of_samples)
  X=X.reshape(No_of_samples,NumFeatures,TimeSteps)
  predicted_temp = model.predict(X)
  predicted_temp = min_max_scaler.inverse_transform(predicted_temp)
  predict_df=pd.DataFrame(list(map(lambda x: x[0], predicted_temp)),columns=["predictions"])
  predict_df.reset_index(inplace=True)
  predict_df = predict_df.rename(columns = {'index':'DAYS'})
  plt.figure(figsize=(15, 6))
  range_history = len(new_data)
  range_future = list(range(range_history, range_history +len(predicted_temp)))
  plt.plot(np.arange(range_history), np.array(new_data),label='History')
  plt.plot(range_future, np.array(predicted_temp),label='Forecasted for RNN')
  plt.legend(loc='upper right')
  plt.xlabel('Time step (hour)')
  plt.ylabel('Stock Price')
  return predict_df,plt.gcf()

forecast_price(20)

def forecast_price(days):
    # Fetch the historical data for the desired ticker symbol
    ticker_symbol = "AAPL"
    ticker_data = yf.Ticker(ticker_symbol)

    # Get the historical prices
    historical_prices = ticker_data.history(period="max")

    # Get the most recent closing price
    most_recent_price = historical_prices["Close"][-1]

    # Calculate the forecasted price by multiplying the most recent closing price by the number of days
    forecasted_price = most_recent_price * (1 + (days / 365))

    # Print the forecasted price
    print(f"The forecasted price of {ticker_symbol} in {days} days is: ${forecasted_price:.2f}")

! pip install gradio

import gradio as gr

interface = gr.Interface(fn = forecast_ETH_price,
                         inputs = gr.Slider(minimum=0, maximum=50, step=1, label="Number of Sample to Predict"),
                         outputs = ["dataframe","plot"],description="Max Temp Prediction of a day")

interface.launch()

"""**Finally by comparing all models LSTM gives better results**"""
