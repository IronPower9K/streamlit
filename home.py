import streamlit as st
from PIL import Image

def bmih(bmi):
    if bmi <= 18.5:
        mess = '저체중'
    elif bmi < 23:
        mess = '정상'
    elif bmi  < 25:
        mess = '과체중'
    elif bmi < 30:
        mess = '고도비만'
    else:    
        mess = '초고도비만'

    return mess



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
    bmig = '당신은',bmih(bmi),'입니다.'
    st.success(bmig)
    image = Image.open('cow.jpg')
    st.image(image, caption='Oh my god!')



    
