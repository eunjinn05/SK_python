import streamlit as st
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from uuid import uuid4

from dotenv import load_dotenv
print(load_dotenv())

st.set_page_config(page_title='Chatbot memory 예제', page_icon=':robot_face:')
st.title('Chatbot 메모리 예제')

##############################################
#   InMemoryChatMessageHistory 생성
##############################################
store = {}


def get_session_history(session_id:str) :
    if session_id not in store :
        store['session_id'] = InMemoryChatMessageHistory()
    return store['session_id']

#############################################################
# Runnable Chain -> PromptTemplate -> Model -> Outputparser
#############################################################
@st.cache_resource
def get_resource() :
    prompt_template = ChatPromptTemplate(
        [
            ('system', '답변은 100단어 이하로 작성해주세요. 정확하지 않은 경우 모른다고 대답해주세요'),
            MessagesPlaceholder('history'),
            ('human', '{query}')
        ]
    )
    model = ChatOpenAI(model='gpt-4o-mini', streming=True)
    return prompt_template | model | StrOutputParser()

runnable = get_resource()

##################################
# RunnableWithMessageHistory
##################################
@st.cache_resource
def get_chain() :
    return RunnableWithMessageHistory(
        runnable=runnable,
        get_session_history=get_session_history,
        input_messages_key="query",
        history_messages_key='history'
    )

chain = get_chain()

#############################################
# st.session_state에 대화 내용을 저장 할 state 생성
#############################################
if 'message_list' not in st.session_state :
    st.session_state['message_list'] = []
if 'session_id' not in st.session_state :
    st.session_state['session_id'] = None


##################################
# 기존 대화 내용 chat_message에 출력
##################################
for message in st.session_state['message_list'] :
    with st.chat_message(message['role']) :
        st.write(message['message'])


############################################
# sidebar에 session_id 입력 폼
############################################
session_id = st.sidebar.text_input('Session ID', placeholder='대화 ID를 입력하세요')

prompt = st.chat_input('사용자 : ')
if prompt :
    # 사용자 입력 prompt를 message_list에 추가
        st.session_state['message_list'].append({'role':'user', 'message':prompt})
        with st.chat_message('user') :
            st.write(prompt)
        # session_id가 입력되지않았을때 처리
        if session_id is None :
            session_id = str(uuid4())
        if st.session_state['session_id'] is None :
            st.session_state['session_id'] = session_id

        ## chain을 이용해서 LLM에게 요청
        with st.chat_message('ai') :
            full_message = ''  #model이 token 단위로 응답 (streaming=True)하면 그것을 누적할 변수
            message_placeholder = st.empty() # chat message 컨테이너에 empty 컨테이너 추가
            config = {'configurable':{session_id:st.session_state['session_id']}}
            for chunk in chain.stream({'query':prompt}, config=config) :
                full_message += chunk
                message_placeholder.write(full_message)

            # 응답이 완료되면 응답을 session_state의 message list에 추가
            st.session_state['message_list'].append({'role':'ai', 'message':full_message})
