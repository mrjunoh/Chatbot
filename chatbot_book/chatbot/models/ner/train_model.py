import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import preprocessing
from sklearn.model_selection import train_test_split
import numpy as np
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils.Preprocess import Preprocess

# 학습 파일 불러오기
def read_file(file_name):
    sents = []
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for idx, l in enumerate(lines):
            if l[0] == ';' and lines[idx + 1][0] == '$':
                this_sent = []
            elif l[0] == '$' and lines[idx - 1][0] == ';':
                continue
            elif l[0] == '\n':
                sents.append(this_sent)
            else:
                this_sent.append(tuple(l.split()))
    return sents

p = Preprocess(word2index_dic='C:/Users/ETRI/Desktop/처음배우는 딥러닝 챗봇/chatbot/chatbot_dict.bin',
               userdic='C:/Users/ETRI/Desktop/처음배우는 딥러닝 챗봇/chatbot/utils/user_dic.tsv')

# 학습용 말뭉치 데이터를 불러옴 - 1
corpus = read_file('C:/Users/ETRI/Desktop/처음배우는 딥러닝 챗봇/chatbot/models/ner/ner_train.txt')

# 말뭉치 데이터에서 단어와 BIO 태그만 불러와 학습용 데이터셋 생성 - 2
sentences, tags = [], []
for t in corpus:
    tagged_sentence = []
    sentence, bio_tag = [], []
    for w in t:
        tagged_sentence.append((w[1], w[3]))
        sentence.append(w[1])
        bio_tag.append(w[3])
    
    sentences.append(sentence)
    tags.append(bio_tag)


print("샘플 크기 : \n", len(sentences))
print("0번 째 샘플 단어 시퀀스 : \n", sentences[0])
print("0번 째 샘플 bio 태그 : \n", tags[0])
print("샘플 단어 시퀀스 최대 길이 :", max(len(l) for l in sentences))
print("샘플 단어 시퀀스 평균 길이 :", (sum(map(len, sentences))/len(sentences)))

# 토크나이저 정의 - 3
tag_tokenizer = preprocessing.text.Tokenizer(lower=False) # 태그 정보는 lower=False 소문자로 변환하지 않는다.
tag_tokenizer.fit_on_texts(tags)

# 단어사전 및 태그 사전 크기
vocab_size = len(p.word_index) + 1
tag_size = len(tag_tokenizer.word_index) + 1
print("BIO 태그 사전 크기 :", tag_size)
print("단어 사전 크기 :", vocab_size)

# 학습용 단어 시퀀스 생성 - 4
x_train = [p.get_wordidx_sequence(sent) for sent in sentences]
y_train = tag_tokenizer.texts_to_sequences(tags)

index_to_ner = tag_tokenizer.index_word # 시퀀스 인덱스를 NER로 변환 하기 위해 사용
index_to_ner[0] = 'PAD'

# 시퀀스 패딩 처리 - 5
max_len = 40
x_train = preprocessing.sequence.pad_sequences(x_train, padding='post', maxlen=max_len)
y_train = preprocessing.sequence.pad_sequences(y_train, padding='post', maxlen=max_len)

# 학습 데이터와 테스트 데이터를 8:2의 비율로 분리 - 6
x_train, x_test, y_train, y_test = train_test_split(x_train, y_train,
                                                    test_size=.2,
                                                    random_state=1234)

# 출력 데이터를 one-hot encoding
y_train = tf.keras.utils.to_categorical(y_train, num_classes=tag_size)
y_test = tf.keras.utils.to_categorical(y_test, num_classes=tag_size)

print("학습 샘플 시퀀스 형상 : ", x_train.shape)
print("학습 샘플 레이블 형상 : ", y_train.shape)
print("테스트 샘플 시퀀스 형상 : ", x_test.shape)
print("테스트 샘플 레이블 형상 : ", y_test.shape)


# 모델 정의 (Bi-LSTM) - 7
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Embedding, Dense, TimeDistributed, Dropout, Bidirectional
from tensorflow.keras.optimizers import Adam

model = Sequential()
model.add(Embedding(input_dim=vocab_size, output_dim=30, input_length=max_len, mask_zero=True))
model.add(Bidirectional(LSTM(200, return_sequences=True, dropout=0.50, recurrent_dropout=0.25)))
model.add(TimeDistributed(Dense(tag_size, activation='softmax')))
model.compile(loss='categorical_crossentropy', optimizer=Adam(0.01), metrics=['accuracy'])
model.fit(x_train, y_train, batch_size=128, epochs=10)

print("평가 결과 : ", model.evaluate(x_test, y_test)[1])
model.save('ner_model.h5')


# 시퀀스를 NER 태그로 변환
def sequences_to_tag(sequences):  # 예측값을 index_to_ner를 사용하여 태깅 정보로 변경하는 함수.
    result = []
    for sequence in sequences:  # 전체 시퀀스로부터 시퀀스를 하나씩 꺼낸다.
        temp = []
        for pred in sequence:  # 시퀀스로부터 예측값을 하나씩 꺼낸다.
            pred_index = np.argmax(pred)  # 예를 들어 [0, 0, 1, 0 ,0]라면 1의 인덱스인 2를 리턴한다.
            temp.append(index_to_ner[pred_index].replace("PAD", "O"))  # 'PAD'는 'O'로 변경
        result.append(temp)
    return result


# f1 스코어 계산을 위해 사용
from seqeval.metrics import f1_score, classification_report

# 테스트 데이터셋의 NER 예측 - 8
y_predicted = model.predict(x_test)
pred_tags = sequences_to_tag(y_predicted) # 예측된 NER
test_tags = sequences_to_tag(y_test)    # 실제 NER

# F1 평가 결과
print(classification_report(test_tags, pred_tags))
print("F1-score: {:.1%}".format(f1_score(test_tags, pred_tags)))



#-1
# 개체 인식 모델을 학습하기 위해 말뭉치 데이터를 불러옴

#-2
# 1에서 불러온 말뭉치 데이터에서 단어(w[1])와 bio 태그)w([3])만 불러와 학습용 데이터셋 생성

#-3
# 단어 시퀀스의 경우 preprocess 객체에서 생성하기 때문에 예제에서는 bio 태그용 토크나이저 객체만 생성함

# -4 
#모델에 입력될 문장의 경우 preprocess에서 생성한 단어 인덱스 시퀀스를 사용하며, bio태그는 3 에서 만들어진
#사전 데이터를 시퀀스 번호 형태로 인코딩함

#-5
#개체명 인식 모델의 입출력 벡터 크기를 동일하게 맞추기 위해 시퀀스 패딩 작업을 함
# 벡터 크기를 4에서 계산한 단어 시퀀스의 평균 길이보다 넉넉하게 40으로 정의함

#-7
#개체 인식 모델을 순차 모델 방식으로 구현함