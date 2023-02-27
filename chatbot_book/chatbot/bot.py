#챗봇 엔진 서버 main 프로그램

import threading
import json

from config.DatabaseConfig import *
from utils.Database import Database
from utils.BotServer import BotServer
from utils.Preprocess import Preprocess
from models.intent.IntentModel import IntentModel
from models.ner.NerModel import NerModel
from utils.FindAnswer import FindAnswer


# 전처리 객체 생성
p = Preprocess(word2index_dic='train_tools/dict/chatbot_dict.bin',
               userdic='utils/user_dic.tsv')

# 의도 파악 모델
intent = IntentModel(model_name='models/intent/intent_model.h5', preprocess=p)

# 개체명 인식 모델
ner = NerModel(model_name='models/ner/ner_model.h5', proprocess=p)


# -2 
def to_client(conn, addr, params): 
    db = params['db']

    try:
        db.connect()  # 디비 연결 2.1

        # 데이터 수신 2.2
        read = conn.recv(2048)  # 수신 데이터가 있을 때 까지 블로킹
        print('===========================')
        print('Connection from: %s' % str(addr))

        if read is None or not read:
            # 클라이언트 연결이 끊어지거나, 오류가 있는 경우
            print('클라이언트 연결 끊어짐')
            exit(0)


        # json 데이터로 변환 2.3
        recv_json_data = json.loads(read.decode())
        print("데이터 수신 : ", recv_json_data)
        query = recv_json_data['Query']

        # 의도 파악 2.4
        intent_predict = intent.predict_class(query)
        intent_name = intent.labels[intent_predict]

        # 개체명 파악
        ner_predicts = ner.predict(query)
        ner_tags = ner.predict_tags(query)


        # 답변 검색 2.5 
        try:
            f = FindAnswer(db)
            answer_text, answer_image = f.search(intent_name, ner_tags)
            answer = f.tag_to_word(ner_predicts, answer_text)

        except:
            answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."
            answer_image = None
        #2.6
        send_json_data_str = {
            "Query" : query,
            "Answer": answer,
            "AnswerImageUrl" : answer_image,
            "Intent": intent_name,
            "NER": str(ner_predicts)
        }
        message = json.dumps(send_json_data_str)
        conn.send(message.encode())

    except Exception as ex:
        print(ex)

    finally:
        if db is not None: # db 연결 끊기
            db.close()
        conn.close()


if __name__ == '__main__':

    # 질문/답변 학습 디비 연결 객체 생성
    db = Database(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME
    )
    print("DB 접속")

    port = 5050
    listen = 100

    # 봇 서버 동작 - 1
    bot = BotServer(port, listen)
    bot.create_sock()
    print("bot start")

    while True:
        conn, addr = bot.ready_for_client()
        params = {
            "db": db
        }

        client = threading.Thread(target=to_client, args=(
            conn,
            addr,
            params
        ))
        client.start()

#-1
#챗봇 서버 소켓을 생성함
# 챗봇 엔진 서버의 통신 포트는 5050, 최대 client 연결 수는 100으로 설정함
#챗봇 엔진 서버 동작 이후 챗봇 클라이언트는 서버 IP와 서버에서 설정한 포트가 오픈되어 있어야 접속 가능

#while 무한루프를 돌면서 client 연결을 기다림
#client의 server 연결 요청이 server에서 수락되는 즉시 챗봇 클라이언트의 서비스 요청을 처리할 수 있는 스레드를 생성함
#이때 생성되는 스레드는 to_client()함수를 호출함
#스레드 함수 내부에서 Database 객체에 접근할 수 있도록 파라미터에 해당 인스턴스를 넘겨줌

#-2
#to_client()는 client의 server연결 수락되는 순간 실행되는 스레드 함수
#챗봇 클라이언트에서 질의한 내용을 처리해 적절한 답변을 찾은 후 다시 챗봇 클라이언트에 응답을 전송
#챗봇 엔진의 처리 과정이 함수 내부에 구현되어있음 순서로는
#먼저 client가 server에 접속하면 먼저 학습 DB에 연결부터 한다.

#다음은 client로부터 데이털르 받기 위해 대기하는 부분이다.
#즉 위에 #데이터 수식 주석 부터이다. 2.2
#이 객체를 통해 클라이언트와 데이터를 주고받음
#recv()메서드는 데이터가 수신될 때까지 블로킹된다. 
#최대 2048바이트만큼 데이터를 수신함.
#클라이언트와의 연결이 끊어지거나 오류가 있는 경우에느 블로킹이 해제되어 None이 반환됨

#2.3 챗봇 클라이언트로부터 수신된 데이터를 JSON 객체로 변환하는 부분
#이때 json 포맷은 앞서 정의한 챗봇 클라이언트에서 server쪽으로 요청하는 json 프로토콜이다.

#2.4 챗봇 클라이언트로부터 수신된 질문 텍스트의 의도와 개체명을 파악

#2.5 분석된 의도와 개체명을 이용해 학습 DB에서 답변을 검색함

#2.6 
#검색된 답변 데이터(의도, 개체명, 답변 텍스트, 이미지 url)를 앞서 정의한 서버에서 client쪽으로 응답하는 json 포맷으로 객체로 생성함
#소켓 통신으로는 객체 형태로 데이터 송신이 불가능
#따라서 json.dump() 함수를 통해 JSON 객체를 문자열로 변환함
#데이터 전송이 완료된 이후 학습 DB와 챗봇 클라이언트와의 연결을 끊은 뒤 스레드 함수의 실행을 종료함