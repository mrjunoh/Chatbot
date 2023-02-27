#단어 '사전' 생성
#챗봇에서 사용하는 사전 파일 생성
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils.Preprocess import Preprocess
from tensorflow.keras import preprocessing
import pickle

#말뭉치 데이터 읽어오기
def read_corpus_data(filename):
    with open(filename, 'r' , encoding='utf8') as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        data = data[1:] # 헤더 제거 즉 엑셀에서 1번 column은 제거 하겠다는 뜻
    return data

#말뭉치 데이터 가져오기 - 1
corpus_data = read_corpus_data('C:/Users/ETRI/Desktop/처음배우는 딥러닝 챗봇/chatbot/train_tools/dict/corpus.txt')

#말뭉치 데이터에서 키워드만 추출해서 사전 리스트 생성 - 2
p = Preprocess()
dict = []
for c in corpus_data:
    pos = p.pos(c[1])
    for k in pos:
        dict.append(k[0])

#사전에 사용될 word2index 생성 - 3
#사전의 첫 번째 인덱스에는 oov 사용
tokenizer = preprocessing.text.Tokenizer(oov_token='OOV')
tokenizer.fit_on_texts(dict)
word_index = tokenizer.word_index

#사전 파일 생성 - 4
f = open("chatbot_dict.bin", "wb")
try:
    pickle.dump(word_index, f)
except Exception as e:
    print(e)
finally:
    f.close()
    

#-1
#말뭉치 데이터를 불러옴
#read_corpus_data함수는 말뭉치 파일(corpus.txt)을 읽어와 리스트로 반환함
# corpus.txt 파일은 네이버 영화 리뷰 말뭉치 데이터
#라인마다 tab('\t')을 사용하여 id, document, label 컬럼으로 데이터를 구분했음
#read_corpus_data함수는 말뭉치 데이터를 각 라인별로 읽어와 \t를 기준으로 데이터를 분리함

#-2
#1에서 불러온 말뭉치 데이터 리스트에서 문장을 하나씩 불러와 POS태깅함 
#형태소 분석 결과를 단어 리스트(dict)에 저장함

#-3
#토크나이저를 이용해 2에서 만들어진 단어 리스트(dict)를 단어 인덱스 딕셔너리(word_index) 데이터로 만듦

#-4
#생성된 단어 인덱스 딕셔너리(word_index) 객체 파일로 저장함
#그럼 chatbot 메인 경로에 chatbot_dict.bin 파일이 생성됨