from openai import OpenAI
import os
from dotenv import load_dotenv   #API키 쓸 때 띄어쓰기 주의하기!! 


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

res = client.responses.create(
    model = 'gpt-4o-mini',        #파라미터와 파라미터는 콤마로 연결!!
    input = [                       #리스트 구조로 연결
        {"role":"system", "content":"너는 뮤지컬 음악 작곡가야"},   #이건 시스템 프롬프팅         #이렇게 되면 딕셔너리   #멀티모달이 뭐더라 role이라는걸 정의해서 뒤에 뭐가 들어오냐에 따라서 달라지는 것
        {"role":"user", "content":"어떤 장면에 음악을 작곡하는게 나을까?"}
    ],  #parameter 추가할 때 콤마 써야 하니까
    temperature=0  
    
)

print(res.output_text)