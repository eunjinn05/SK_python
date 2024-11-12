
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

# revolvingutilizationofunsecuredlines 에 적용할 Transformer 클래스
## 1초과하는 값들을 1로 변경한다

class CapValuesTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X_capped = np.where(X > 1, 1, X)
        return X_capped
    
# Age 전처리에 적용할 transformer 클래스
## 21 이하인 값들은 중위수로 변환

class AgeTransformer(BaseEstimator, TransformerMixin):
    
    def fit(self, X, y=None):
        """
        X의 중위값을 계산해서 저장
        """
        self.median_value = np.median(X)
        return self
    
    def transform(self, X, y=None):
        X_transformed = np.where(X <= 21, self.median_value, X)
        return X_transformed
    
# debtratio, monthlyincome 전처리에 적용할 transformer 클래스
## - 정상범위 최대값, 최소값으로 대체한다.
## - debtratio: 2000, monthlyincome: 1.5 배의 IQR로 계산한 최대값, 최소값으로 대체한다.

class OutlierTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, whis=1.5):
        self.whis = whis
    
    def fit(self, X, y=None):
        q1 = np.nanquantile(X, q=0.25)
        q3 = np.nanquantile(X, q=0.75)
        IQR = q3 - q1
        self.lower_bound = q1 - IQR * self.whis
        self.upper_bound = q3 + IQR * self.whis
        return self
    
    def transform(self, X, y=None):
        X_transformed = np.where(X < self.lower_bound, self.lower_bound, X)
        X_transformed = np.where(X_transformed > self.upper_bound, self.upper_bound, X_transformed)
        return X_transformed
