#NerModel 테스트
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.Preprocess import Preprocess
from models.ner.NerModel import NerModel

p = Preprocess(word2index_dic='C:/Users/ETRI/Desktop/처음배우는 딥러닝 챗봇/chatbot/chatbot_dict.bin',
               userdic='../utils/user_dic.tsv')


ner = NerModel(model_name='C:/Users/ETRI/Desktop/처음배우는 딥러닝 챗봇/chatbot/ner_model.h5', proprocess=p)
query = '오늘 오전 13시 2분에 탕수육 주문 하고 싶어요'
predicts = ner.predict(query)
tags = ner.predict_tags(query)
print(predicts)
print(tags)

