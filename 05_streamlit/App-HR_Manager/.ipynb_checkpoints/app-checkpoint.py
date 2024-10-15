import streamlit as st
import database as db
import configparser as parser

st.set_page_config("검색", layout="wide")

@st.cache_resource
def get_dao():
    """
    HRDao 생성 함수.
    """    
    props = parser.ConfigParser()  # parser 생성
    props.read("./config.ini")     # ini 파일 읽기
    config = props['MYSQL']        # section이름으로 읽기
    dao = db.HRDao(host=config['host'], port=3306, user=config['user'], password=config['password'], db=config['db'])
    return dao

dao = get_dao()

@st.cache_data
def get_depts():
    """
    전체 부서ID, 부서명 조회 함수
    return
        tuple[부서ID, 부서명]
    """
    return (('all', 'all'),) + dao.select_dept()

@st.cache_data
def get_jobs():
    """
    전체 업무ID, 업무명 조회 함수
    return
        tuple[업무ID, 업무명]
    """
    return (('all', 'all'),) + dao.select_job()

############################################################
# side menu
# 검색 조건 입력폼들 정의
############################################################
by = st.sidebar.radio(
    "검색기준을 선택하세요",
    ["업무로 검색", "부서로 검색"],
    index=None # 아무것도 선택되지 않도록 설정
)

job_option = dept_option = None
if by == "업무로 검색":
    job_option = st.sidebar.selectbox(
        label="검색할 직원의 업무 선택.", 
        options=get_jobs(), 
        format_func=lambda x: x[1],
    )
    dept_option = None

elif by == "부서로 검색":
    dept_option = st.sidebar.selectbox(
        label="검색할 직원의 부서 선택",
        options=get_depts(),
        format_func=lambda x: x[1]
    )
    job_option = None

####################################################
# 선택 조건에 따른 Data를 Dao를 이용해 DB로 부터 조회
####################################################
if job_option and "all" not in job_option: # 업무로 검색한 결과 출력, all을 제외(마지막 elif에서 처리)
    df = dao.select_emp_by_job(job_option[0])
    keyword = f"**{job_option[1]}** 업무로 검색한 결과 - {len(df)} 명"
elif dept_option and "all" not in dept_option: # 부서로 검색한 경우 결과 출력, all을 제외
    df = dao.select_emp_by_dept(dept_option[0])
    keyword = f"**{dept_option[1]}** 부서로 검색한 결과 - {len(df)} 명"
elif (job_option is not None and job_option[0] == "all") or (dept_option is not None and dept_option[0] == "all"): # 전체 직원 조회
    df = dao.select_all_emp()
    keyword = f"### 전체 직원 조회 - {len(df)} 명"

########################################################
# 결과 화면
########################################################
st.title("직원 조회")
try:
    st.markdown(keyword)
    st.dataframe(df, use_container_width=True)
except:
    st.subheader("검색조건을 선택하세요.")
