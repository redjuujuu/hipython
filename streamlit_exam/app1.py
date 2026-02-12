import streamlit as st

st.title('안녕하세요')

#브라우저에 텍스트 출력
st.write('Hello Streamlit!!!')

st.divider()

#사용자 입력을 받는 요소
name = st.text_input('이름 : ')

st.write(name)

def bt1_click():  # 정의
    st.write('왜 눌렀어?')   
    
    # 정의가 호출보다 먼저 나와야함

### 버튼
# btn1 = st.button('누를래말래누를래말래', on_click = bt1_click) #호출

btn1 = st.button('누를래말래누를래말래')
if btn1 :
    # st.write('정말 눌렀어??')
    bt1_click()

    









#### 판다스 사용하기
import pandas as pd
df = pd.read_csv('./data/pew.csv')

#log 출력할 때 이 함수가 필수임
print(df.info())

st.write(df.head())





