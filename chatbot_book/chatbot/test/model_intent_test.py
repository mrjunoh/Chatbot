import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.Preprocess import Preprocess
from models.intent.IntentModel import IntentModel

p = Preprocess(word2index_dic='C:/Users/ETRI/Desktop/처음배우는 딥러닝 챗봇/chatbot/chatbot_dict.bin',
               userdic='../utils/user_dic.tsv')

intent = IntentModel(model_name='C:/Users/ETRI/Desktop/처음배우는 딥러닝 챗봇/chatbot/intent_model.h5', preprocess=p)
query = "오늘 탕수육 주문 가능한가요?"
predict = intent.predict_class(query)
predict_label = intent.labels[predict]

print(query)
print("의도 예측 클래스 : ", predict)
print("의도 예측 레이블 : ", predict_label)

