# HR Manager

Streamlit을 이용해 hr Database의 직원정보 조회.

## 설치
- 가상환경 생성
```
conda create -n hr python=3.12
또는
python -m venv .venv
```

- 패키지 설치
```
pip install -r requirements.txt
```

- DB, 테이블 생성
  - sql\ddl.sql 실행
  
## 실행
- config.ini 파일 생성 후 다음 항목 추가
```
host=DB IP
user=DB username
password=DB password
db=Database Name
```

- streamlit 실행
```
streamlit run app.py
```