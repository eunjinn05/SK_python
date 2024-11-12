import streamlit as st
import joblib
import numpy as np

import sys
import os

@st.cache_resource
def load_model():
    return joblib.load('models/best_xgb.pkl')

@st.cache_resource
def load_preprocessor():
    sys.path.append(os.getcwd()) # preprocessing.py의 사용자 전처리기들을 load하기위해서 현재 디렉토리를 파이썬 모듈 검색 경로에 추가. 
    return joblib.load('models/preprocessor.pkl')

# 모델 및 전처리기 로드
model = load_model()
preprocessor = load_preprocessor()

# Streamlit 앱 설정
st.title('대출 위험도 예측')
st.divider()
# 사이드바에서 사용자 입력 받기
st.sidebar.header('입력 정보')
revolvingutilizationofunsecuredlines = st.sidebar.number_input('신용대비 운용가능한 돈 비율', min_value=0.0,value=0.0)
age = st.sidebar.number_input('나이', min_value=18, max_value=120, value=30)
numberoftime30_59dayspastduenotworse = st.sidebar.number_input('2년간 30~59일 연체횟수', min_value=0, value=0)
debtratio = st.sidebar.number_input('전체수입 대비 지출비율', min_value=0.0, value=0.2)
monthlyincome = st.sidebar.number_input('월 수입', min_value=0, value=0)
numberofopencreditlinesandloans = st.sidebar.number_input('대출건수', min_value=0, value=0)
numberoftimes90dayslate = st.sidebar.number_input('90일 이상 연체한 횟수', min_value=0, value=0)
numberrealestateloansorlines = st.sidebar.number_input('부동산담보대출 건수', min_value=0, value=0)
numberoftime60_89dayspastduenotworse = st.sidebar.number_input('2년간 60~89일 연체횟수', min_value=0, value=0)
numberofdependents = st.sidebar.number_input('부양가족수', min_value=0, value=0)

# 예측 버튼
if st.sidebar.button('예측'):
    # 입력 데이터를 DataFrame으로 변환
    input_data = np.array([[
        revolvingutilizationofunsecuredlines,
        age,
        numberoftime30_59dayspastduenotworse,
        debtratio,
        monthlyincome,
        numberofopencreditlinesandloans,
        numberoftimes90dayslate,
        numberrealestateloansorlines,
        numberoftime60_89dayspastduenotworse,
        numberofdependents
    ]])

    # 데이터 전처리
    processed_data = preprocessor.transform(input_data)

    # 예측 수행
    prediction = model.predict(processed_data)
    prediction_proba = model.predict_proba(processed_data)[:, 1]

    # 결과 출력
    st.header('예측 결과')
    st.subheader(f'상환여부 예측: {"상환 불이행" if prediction[0] == 1 else "상환"}')
    st.write(f'대출을 못 갚을  확률: {prediction_proba[0]*100:.2f}%')