
import pandas as pd

def load_dataset():
    # load dataset
    data = pd.read_csv('data/cs_data.csv')
    # 컬럼명 소문자로 변경
    data.columns = data.columns.str.lower()
    # taget 컬럼을 y로, 나머지를 X로
    data = data.drop(data.columns[0], axis=1)
    X = data.drop(columns='seriousdlqin2yrs')
    y = data['seriousdlqin2yrs']
    
    return X, y
