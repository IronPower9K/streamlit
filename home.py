import streamlit as st

st.write('# Hi! welcome to My App!')

st.write('Nice to meet you!')

if st.button('Say hello'):
    st.write('why hello there')
else:
    st.write('Goodbye') 

option = st.selectbox('좋아하는 동물은?',('강아지','말','토끼','코끼리'))

st.write('내가 좋아하는 동물은', option,'입니다.')
st.write(f'좋아하는 동물은 {option}입니다.')

txt = st.text_area('자신을 소개해보세요.')

st.write('입력한 내용은: ',txt)

age = st.slider('나이를 선택하세요.',0,130,25)
st.write('저의 나이는',age,'입니다.')
