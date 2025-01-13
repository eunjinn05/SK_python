from langchain_community.tools import TavilySearchResults
from langchain_core.documents import Document
from langchain_core.tools import tool
from pprint import pprint
from langchain_community.document_loaders import WikipediaLoader
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field
from textwrap import dedent
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# TavilySearch로 검색한 결과 Document에 담아서 반환하는 Tool 생성

@tool
def search_web(query:str, max_results:int = 2) -> list[Document]:
    '''가지고 있지 않은 정보나 최신 정보를 찾기 위해 인터넷 검색을 하는 툴
        검색할 내용은 query로 입력 받습니다
        검색 갯수는 max_results로 받습니다 입력되지않는 경우에는 2개를 검색합니다
        검색 결과는 Document 객체에 담아 list로 묶어서 반환합니다.
    '''
    tavily_search = TavilySearchResults(max_results=max_results)
    docs = tavily_search.invoke(query)
    # print(docs)
    # list[dict] => list[Document(content:검색결과, metadata={url:검색 url})]
    document_list = []
    for doc in docs :
        _doc = Document(page_content=doc['content'], 
        metadata={'url':doc['url'], 'question':query}
        )
        document_list.append(_doc)
    if document_list :
        return document_list
    else :
        return '관련된 정보를 검색 할 수 없습니다.'

        

# 위키피디아에서 검색한 결과 문서로 loading
# Runnable로 만들 함수
def wikipedia_search(input_data:dict) -> list[Document] :
    '''
        사용자 query(검색 키워드)를 위키 백과사전에서 검색한 결과 k개 반환
        parameter :
            input_data : dict dict[str:query, int:검색갯수-max_results]
        return :
            list[Document] - 개별 검색결과
    '''
    query = input_data['query']
    k = input_data.get('max_results', 2)
    # Document Loader 생성
    wiki_loader = WikipediaLoader(query=query, load_max_docs=k, lang='ko')
    # 문서로드
    wiki_docs = wiki_loader.load()
    return wiki_docs

# tool 관련 스키마 정의 한 뒤 runnable.as_tool 메소드 이용해 생성
# parameter는 pydantic으로 정의
# description 등은 as_tool() 에 직접 정의
class WikiSearchSchema(BaseModel) :
    query:str = Field(..., description='wikipedia에서 검색할 keyword')  # ... required
    # ... 으로 시작하지않으면 optional. default: 값이 없을 경우 사용할 기본 값
    max_results:int = Field(default=2, description='검색할 문서 갯수')

search_wiki = wiki_runnable.as_tool(
    args_schema=WikiSearchSchema,
    name='search_wiki',
    description=dedent('이 도구는 위키피이다에서 정보를 검색해야할때 사용합니다 사용자의 질문과 관련된 위키피디아 문서를 지정된 개수만큼 검색해서 반환합니다')
)



COLLECTION_NAME = 'restaurant_menu_2'
PERSIST_DIRECTORY = 'vector_store/restaurant_menu_db'

embedding_model = OpenAIEmbeddings(model='text-embedding-3-small')
v_store = Chroma(
    embedding_function=embedding_model,
    collection_name=COLLECTION_NAME,
    persist_directory=PERSIST_DIRECTORY
)

retriever = v_store.as_retriever()

@tool
def search_menu(query:str) -> list[Document] :
    ''' vector store에 저장된 restaurant의 메뉴 검색한다 이 도구는 restaurant의 메뉴 관련 질문에 대해 실행한다 '''
    result = retriever.invoke(query)
    if len(result) :
        return result
    else :
        return [Document(page_content='검색 결과가 없습니다')]

search_menu.invoke('저녁 요리를 추천해주세요')