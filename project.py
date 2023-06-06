import pandas as pd

from prophet import Prophet
import yfinance as yf


import plotly.graph_objects as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta

import streamlit as st
from PIL import Image

option = st.selectbox('어떤 종목을 보시겠습니까?',("대한항공",'삼성전자'))

if option == '대한항공':
    finance = '003490.KS'
if option == '삼성전자':
    finance = '005930.KS'

dt_now = datetime.now()

d = st.date_input(
    "언제 매수하셨나요?",
    dt_now)

number = st.number_input('몇주를 사셨습니까?')

if st.button('계산'):
    
    dt_past = dt_now - relativedelta(years = 5)

    df = yf.download(finance,
                        start=dt_past,
                        end=dt_now.date(),
                        progress=False)

    df = df[["Close"]]

    df = df.reset_index()

    df.columns = ["ds", "y"]

    df['ds'] = pd.to_datetime(df['ds'])
    d = pd.to_datetime(d)
    dt_now = pd.to_datetime(dt_now)

    df.index = df['ds']
    df.set_index('ds', inplace=True)

    df = df.reset_index()

    df.columns = ['ds', 'y']
    
    buy = df[df['ds']== d]
   
    
    
    if buy.empty:
        st.warning('선택하신 날짜는 휴장일입니다. 다른 날짜를 선택해 주세요!')
        st.stop()

    df_prophet = Prophet(changepoint_prior_scale=0.15, daily_seasonality=True)
    df_prophet.fit(df)

    fcast_time = 180
    df_forecast = df_prophet.make_future_dataframe(periods = fcast_time,freq = 'D')

    df_forecast = df_prophet.predict(df_forecast)

   
    
    if not buy.empty:
        buy_index = df[df['ds'] == d].index[0]
        
        if not df_forecast[(df_forecast['ds'] > dt_now) & (df_forecast['yhat'] > buy['y'].values[0])].empty:
            sell = df_forecast[(df_forecast['ds'] > dt_now) & (df_forecast['yhat'] > buy['y'].values[0])]
            sell = sell.set_index('ds')
            sellprice = sell['yhat'].max()
            #print(sellprice)

            selltime =sell['yhat'].idxmax()
            sellprice = sellprice - buy['y'].values[0]
            #print(selltime,sellprice)
        
            st.balloons()
            st.write(selltime, '에 파시는 것을 추천드립니다! 수익은',sellprice*number,'원입니다')
            
        else:
            st.write('존버가 답입니다...')  
            image = Image.open('cow.jpg')
            st.image(image, caption='Oh my god!')
                
    fig = plt.Figure()
    fig.add_trace(plt.Scatter(x=df['ds'], y=df['y'], name='실제값'))
    fig.add_trace(plt.Scatter(x=df_forecast['ds'], y=df_forecast['yhat'], name='예측값'))
    fig.add_annotation(x=d, y=float(buy['y']), text='구입시점', showarrow=True, arrowhead=1, ax=30, ay=-30)

    fig.update_layout(title=f"{option}",
                      xaxis_title='Date',
                      yaxis_title='Stock Price',
                      template='plotly_white')

    st.plotly_chart(fig)


