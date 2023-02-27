#FindAnswer.py 클래스를 테스트
#이 테스트는 챗봇 엔진의 전체 동작 과정을 한번에 보여줌 즉 챗봇 엔진의 동작 코드임
#이 코드를 서버 환경에서 작동될 수 있도록 수정하면 챗봇 엔진 서버 프로그램이 된다.

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config.DatabaseConfig import *
from utils.Database import Database
from utils.Preprocess import Preprocess

# 전처리 객체 생성
p = Preprocess(word2index_dic='C:/Users/ETRI/Desktop/처음배우는 딥러닝 챗봇/chatbot/chatbot_dict.bin',
               userdic='C:/Users/ETRI/Desktop/처음배우는 딥러닝 챗봇/chatbot/utils/user_dic.tsv')

# 질문/답변 학습 디비 연결 객체 생성
db = Database(
    host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME
)
db.connect()    # 디비 연결

# 원문 - 1
# query = "오전에 탕수육 10개 주문합니다"
# query = "화자의 질문 의도를 파악합니다."
# query = "안녕하세요"
query = "안녕하세요"

# 의도 파악 - 2
from models.intent.IntentModel import IntentModel
intent = IntentModel(model_name='C:/Users/ETRI/Desktop/처음배우는 딥러닝 챗봇/chatbot/models/intent/intent_model.h5', preprocess=p)
predict = intent.predict_class(query)
intent_name = intent.labels[predict]

# 개체명 인식 - 3
from models.ner.NerModel import NerModel
ner = NerModel(model_name='C:/Users/ETRI/Desktop/처음배우는 딥러닝 챗봇/chatbot/models/ner/ner_model.h5', proprocess=p)
predicts = ner.predict(query)
ner_tags = ner.predict_tags(query)

print("질문 : ", query)
print("=" * 100)
print("의도 파악 : ", intent_name)
print("개체명 인식 : ", predicts)
print("답변 검색에 필요한 NER 태그 : ", ner_tags)
print("=" * 100)

# 답변 검색 - 4
from utils.FindAnswer import FindAnswer

try:
    f = FindAnswer(db)
    answer_text, answer_image = f.search(intent_name, ner_tags)
    answer = f.tag_to_word(predicts, answer_text)
except:
    answer = "죄송해요 무슨 말인지 모르겠어요"

print("답변 : ", answer)

db.close() # 디비 연결 끊음


#-1
#챗봇 엔진이 사용할 입력 문장을 정의

#-2
#챗봇 엔진에서 의도 분류를 하는 코드
#이전에 학습한 의도 분류 모델 파일을 불러와 문장의 의도를 예측

#-3
#챗봇 엔진에서 개체명 인식을 하는 코드
# 이전에 학습한 개체명 인식 모델 파일을 불러와 문장 내에 개체명을 예측

#-4
#-2,-3에서 예측된 결과(의도명, 개체명)를 이용해 학습 db에서 답변을 검색함
#학습 db에 해당하는 조건에 맞는 답변이 존재하지 않는 경우 예외 발생
#이때 해당 문장을 이해하지 못하는 문장 출력
#챗봇 엔진의 성능을 높이기 위해서는 예외 사항이 발생하는 질문 내용들을
#계속해서 모델 학습 데이터로 활용해야함