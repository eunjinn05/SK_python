from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.callbacks import StreamingStdOutCallbackHandler # LLM의 응답을 chunk 단위로 받아 출력하는 callback

from dotenv import load_dotenv

load_dotenv()

prompt_template = ChatPromptTemplate(
    [
        ('system', '당신은 AI Assistant입니다. 질문에 정확한 답변을 해주세요. 모르면 모른다고 하세요'),
        ('human', '{query}')
    ]
)

model = ChatOpenAI(model='gpt-4o-mini', streaming=True, callbacks=[StreamingStdOutCallbackHandler()]) # stream : chunk 단위로 달라함, callbacks=StreamingStdOutCallbackHandler 알아서 붙여줌
query = input('질문할 내용')
prompt = prompt_template.invoke({'query':query})
result = model.invoke(prompt).content
# print(result)

#stream:True -> model.stream(prompt) : generator
# for chunk in model.stream(prompt) :
#     print(chunk.content, end='')