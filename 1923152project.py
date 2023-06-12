import pandas as pd

from prophet import Prophet
import yfinance as yf


import plotly.graph_objects as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta

import streamlit as st
from PIL import Image

dt_now = datetime.now()   # 현재의 시간을 dt_now 변수에 저장
dt_past1 = dt_now - relativedelta(weeks = 1) # dt_now에서 1주 전 시간을 dt_past1에 저장

add_selectbox = st.sidebar.selectbox(
    "목차",
    ("나의 자산", "주식 가격예측")
) # 목차 구성 후 나의 자산 섹션으로 갈지 주식 가격예측으로 갈지 selectbox형태로 보여줌

if add_selectbox == "나의 자산": # 만약 나의 자산을 선택 했을 경우

    st.title('나의 자산:heavy_dollar_sign:') # 제목을 나의 자산으로 지정
    option1 = st.selectbox('어떤 종목을 사셨나요?',("대한항공",'삼성전자','SK 이노베이션')) # option1에 본인이 구매한 종목을 선택

    if option1 == '대한항공': # 만약 종목을 선택했을 경우
        finance1 = '003490.KS' # finance1에 해당 종목의 코드번호를 저장
    if option1 == '삼성전자':# 만약 종목을 선택했을 경우
        finance1 = '005930.KS'# finance1에 해당 종목의 코드번호를 저장
    if option1 == 'SK 이노베이션':# 만약 종목을 선택했을 경우
        finance1 = '096770.KS'    # finance1에 해당 종목의 코드번호를 저장

    num1 = st.number_input('몇주를 사셨습니까?') # 본인이 산 주식의 수량을 입력 받고 num1에 저장

    if st.button('확인'): # 위에 사항을 기입 후 확인 버튼을 누를때 시작

        data1 = yf.download(finance1,
                            start=dt_past1,
                            end=dt_now.date(),
                            progress=False) # data1에 finance1의 종목 번호 불러오고 시작지점은 dt_past1, 종료지점은 현재 날짜 이다.

        data1 = data1[["Close"]] # data1의 close열의 값만 data1에 다시 저장

        data1 = data1.reset_index() # 기존에 있던 열의 인덱스 삭제

        data1.columns = ["ds", "y"] # data1의 열의 인덱스를 처음부터 ds , y로 지정

        data1['ds'] = pd.to_datetime(data1['ds']) # data1에 있는 ds열에 해당하는  날짜값을 pandas에 호환이 되는 날짜로 변경
        dt_now = pd.to_datetime(dt_now)     #dt_now값을 pandas에 호환이 되는 날짜 값으로 변환 후 저장

        data1.index = data1['ds']    # data1의 기본 인덱스 값을 data1의 ds의 값으로 지정
        data1.set_index('ds', inplace=True) #data1의 인덱스를 ds로 지정후 ds값으로 대체


        st.write("현재 자산은",data1['y'].values[len(data1)-1]*num1 ,'입니다.')  
        # 현재 자산을 나타내 주는 코드 data1['y'].values[len(data1)-1]은 data1['y']의 가장 마지막 값을 의미한다 즉 가장 최근에 폐장한 값을 의미한다.
        st.write('전일 대비',(data1['y'].values[len(data1)-1]*num1)-(data1['y'].values[len(data1)-2]*num1),"원 만큼 변동되었습니다.")
        # data1['y'].values[len(data1)-1]*num1) 마지막 폐장일의 가격에서 data1['y'].values[len(data1)-2]*num1 전날의 가격을 빼면서 해당하는 날짜의 가격 등락을 확인한다.
        if option1 == '대한항공': # 만약 대한항공을 선택 했을 경우
            st.write("[뉴스보기](https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EB%8C%80%ED%95%9C%ED%95%AD%EA%B3%B5)")
            # 네이버 대한항공 검색 페이지를 하이퍼링크로 출력 
        if option1 == '삼성전자': # 만약 삼성전자을 선택 했을 경우
            st.write("[뉴스보기](https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90)")
            # 네이버 삼성전자 검색 페이지를 하이퍼링크로 출력
        if option1 == 'SK 이노베이션': # 만약 sk 이노베이션을 선택 했을 경우
            st.write("[뉴스보기](https://search.naver.com/search.naver?where=nexearch&sm=top_sly.hst&fbm=0&acr=1&ie=utf8&query=sk%EC%9D%B4%EB%85%B8%EB%B2%A0%EC%9D%B4%EC%85%98)")
            # 네이버 sk 이노베이션 검색 페이지를 하이퍼링크로 출력

        
    



if add_selectbox == "주식 가격예측": # 주식 가격예측을 선택했을 경우

    st.title('나의 :blue[주]:red[식]은?:chart_with_upwards_trend:') # 제목 지정

    option = st.selectbox('어떤 종목을 보시겠습니까?',("대한항공",'삼성전자','SK 이노베이션'))# option1에 본인이 구매한 종목을 선택

    if option == '대한항공':# 만약 종목을 선택했을 경우
        finance = '003490.KS'# finance1에 해당 종목의 코드번호를 저장
    if option == '삼성전자':# 만약 종목을 선택했을 경우
        finance = '005930.KS'# finance1에 해당 종목의 코드번호를 저장
    if option == 'SK 이노베이션':# 만약 종목을 선택했을 경우
        finance = '096770.KS' # finance1에 해당 종목의 코드번호를 저장
    

    d = st.date_input(
        "언제 매수하셨나요?",
        dt_now) # 달력기본값을 오늘로 출력 후 d 변수에 저장 

    number = st.number_input('몇주를 사셨습니까?') # 본인이 산 주식의 수량을 입력 받고 num1에 저장


    if st.button('계산'): # 계산 버튼 생성 후 눌렀을 때 실행
        
        dt_past = dt_now - relativedelta(years = 5) # 오늘로 부터 5년전 날짜를 dt_past에 저장

        data = yf.download(finance,
                            start=dt_past,
                            end=dt_now.date(),
                            progress=False) # 5년전 날짜로 부터 오늘까지 해당하는 주식의 데이터를 불러오고 data에 저장

        data = data[["Close"]] # data의 값 중 close값만 data에 다시 저장

        data = data.reset_index() # data의 인덱스 초기화

        data.columns = ["ds", "y"] # data의 열을 ds , y로 저장

        data['ds'] = pd.to_datetime(data['ds']) #data의 ds값을 pandas에 호환되는 날짜의 값으로 변환
        d = pd.to_datetime(d) # d를 pandas에 호환되는 날짜의 값으로 변환
        dt_now = pd.to_datetime(dt_now) # dt_now를 pandas에 호환이 되는 값으로 변환

        data.index = data['ds']  # data의 인덱스에 ds값을 삽입
        data.set_index('ds', inplace=True) # 그 ds값을 data의 인덱스로 선언 (날짜로 그 날짜에 해당하는 y값을 쉽게 추출하기 위함)

        

        data = data.reset_index() # data의 인덱스 초기화

        data.columns = ['ds', 'y']# data의 열을 ds , y로 저장

        buy = data[data['ds']== d]# 본인이 산 날짜에 해당하는 날짜와 주식 가격을 buy에 저장
        
        
        
        


    
        
        
        if buy.empty: # 만약 휴장일을 선택했다면 해당 문구 실행
            st.warning('선택하신 날짜는 휴장일입니다. 다른 날짜를 선택해 주세요!') # 경고 문구
            st.stop() # 즉시 계산 정지

        data_prophet = Prophet(changepoint_prior_scale=0.35, daily_seasonality=True) # data_prophet변수에 데이터의 유연성 0.15, 일일 영향이 있는 prophet모델을 호출 시키고 해당 세팅값 저장
        data_prophet.fit(data) # data_prophet에 data를 데이터로 저장시킨다.

        fcast_time = 180 # 예측 시간을 180일로 설정
        data_forecast = data_prophet.make_future_dataframe(periods = fcast_time) # 현재의 데이터 값을 가지고 값의 추이를 학습하고 현 시점으로 부터 180동안 예측할 수 있는 프레임을 설정

        data_forecast = data_prophet.predict(data_forecast) # 현재까지 주어진 조건을 이용하여 미래의 값을 예측 후 data_forcast에 저장

    
        
        
            
        if not data_forecast[(data_forecast['ds'] > dt_now) & (data_forecast['yhat'] > buy['y'].values[0])].empty: # 현재시점 이후에 구입한 금액보다 더 높은 가격이 예측이 된 경우 실행
            sell = data_forecast[(data_forecast['ds'] > dt_now) & (data_forecast['yhat'] > buy['y'].values[0])]# 현재시점 이후에 구입한 금액보다 더 높은 가격이 예측이 된 경우 해당 값들을 sell에 저장
            sell = sell.set_index('ds') # ds를 sell의 인덱스로 설정
            sellprice = sell['yhat'].max() # sell에서 예측한 값중 이익이 나는 값이 들어 있는 yhat에서 가장 큰 값, 즉, 가장 많이 이익을 볼 수 있는 값을 sellprice에 저장
            selltime =sell['yhat'].idxmax() # selltime에서 sellprice에 해당하는 인덱스 값 즉, 날짜를 불러와서 selltime에 저장
            sellprice = sellprice - buy['y'].values[0] # 가장 이익이 많이 나는 값에서 구매가격을 빼서 이익을 계산 후 저장
            
        
            st.balloons() # 해당 조건문 실행시 풍선이 나온다.
            st.write('사실 때의 금액은',buy['y'].values[0],'원입니다.') # 구입가격을 화면에 표출
            st.write(selltime, '에 파시는 것을 추천드립니다! 수익은',sellprice*number,'원입니다.') # 위에서 계산한 판매적기, 해당 날짜에 판매시 예측 이익을 표출한다.
            
        else: # 예측 값중 이익이 기대가 되지 않을 때
            st.snow() # 해당 모션 출력
            st.write('존버가 답입니다...')  # 해당 문구를 표출
            image = Image.open('cow.jpg') # 해당 사진을 표출
            st.image(image, caption='Oh my god!') # 해당 사진의 제목 설정
                    
        fig = plt.Figure() # fig를 plt 프레임으로 설정
        fig.add_trace(plt.Scatter(x=data['ds'], y=data['y'], name='실제값')) # x값은 data['ds'] y값은 data['y'] 즉, 실제값을 fig 프레임에 추가
        fig.add_trace(plt.Scatter(x=data_forecast['ds'], y=data_forecast['yhat'], name='예측값')) # x값은 data['ds'] y값은 data['y'] 즉, 예측값을 fig 프레임에 추가
        fig.add_annotation(x=d, y=float(buy['y']), text='구입시점', showarrow=True, arrowhead=1, ax=30, ay=-30) # 구입 시점을 annotation으로 표현 

        fig.update_layout(title=f"{option}",
                        xaxis_title='년도',
                        yaxis_title='주식 가격',
                        template='plotly_white') # plt 그래프의 제목, x,y축 제목 설정 및 템플릿 스타일 지정

        st.plotly_chart(fig) # 위에서 설정한 plot차트를 streamlit으로 출력
        st.error('본 정보를 이용한 투자에 대한 책임은 해당 투자자에게 귀속됩니다.') # 안내 메시지 출력


