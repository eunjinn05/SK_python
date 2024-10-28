from matplotlib.pylab import f
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

import pickle



@st.cache_data
def load_data():
    return load_iris()

import json

@st.cache_resource
def load_model():
    with open('config.json', 'r') as f:
        config = json.load(f)
    model_path = config['model_path']
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    return model
    

iris = load_data()
model = load_model()
st.title("Iris 품종 예측 APP")

# side bar에 입력 폼 정의
st.sidebar.title('Iris 품종 예측 입력')
with st.sidebar.form(key='iris_form'):

    sepal_length = st.number_input('Sepal length', min_value=0.0, max_value=20.0)
    sepal_width = st.number_input('Sepal width', min_value=0.0, max_value=20.0)
    petal_length = st.number_input('Petal length', min_value=0.0, max_value=20.0)
    petal_width = st.number_input('Petal width', min_value=0.0, max_value=20.0)
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    data = np.array([[sepal_length, sepal_width, petal_length,petal_width]])
    prediction = model.predict(data)
    prediction_proba = model.predict_proba(data)

    print(prediction[0])

    result = f'예측된 품종은 {iris.target_names[prediction[0]].capitalize()}({np.round(prediction_proba[0, prediction].item()*100, 2)}%) 입니다.'
    st.header('예측 결과')

    st.subheader(result)





