import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

def bmih(bmi):
    if bmi <= 18.5:
        mess = '저체중입니다.'
    elif bmi < 23:
        mess = '정상입니다.'
    elif bmi  < 25:
        mess = '과체중입니다.'
    elif bmi < 30:
        mess = '고도비만입니다.'
    else:    
        mess = '초고도비만입니다.'

    return mess

add_selectbox = st.sidebar.selectbox(
    "목차",
    ("체질량계산기", "갭마인더", "마이페이지")
)
if add_selectbox == '체질량계산기':
    
    st.info('# 체질량 지수 계산기')

    height = st.number_input('신장 (cm)',value = 170 , step =5)
    st.write(height,'cm')

    weight = st.number_input('체중 (kg)',value = 60 , step =5)
    st.write(weight,'kg')

    bmi = weight/((height/100)**2)

    if st.button('계산'):
        st.balloons()
        
        bmif = round(bmi,2)
        

        st.write('당신의 체질량 지수는',bmif,'입니다.')
    
        st.success(bmih(bmi))
        image = Image.open('cow.jpg')
        st.image(image, caption='Oh my god!')
elif add_selectbox == '갭마인더':
    st.header('여기는 갭마인더입니다.')
    st.write('파일 읽어오기')
    data = pd.read_excel('gapminder.xlsx')
    st.write(data)
    
    colors=[]
    for x in data['continent']:
        if x == 'asia':
            colors.append('tomato')
        elif x == 'Europe':
            colors.append('blue')  
        elif x == 'Africa':
            colors.append('olive')
        elif x == 'America':
            colors.append('green')
        else:
            colors.append('orange')
    data['colors'] = colors                     

    year = st.slider('select a year',1952,2007,1952,step = 5)
    st.write('##',year,'년')

    data = data[data['year']==year]

    fig, ax = plt.subplots()
    ax.scatter(data['gdpPercap'],data['lifeExp'],s=data['pop']*0.000002,color=data['colors'])
    st.pyplot(fig)

else:
    st.header('여기는 마이페이지입니다.')    
    

    