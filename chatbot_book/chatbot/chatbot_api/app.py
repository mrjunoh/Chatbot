#챗봇 rest api 서버 구현
from flask import Flask, request, jsonify, abort
import socket
import json

#챗봇 엔진 서버 접속 정보 - 1
host = "127.0.0.1" #챗봇 엔진 서버 ip 주소
port = 5050 #챗봇 엔지 서버 통신 포트

#flask 애플리케이션
app = Flask(__name__)

#챗봇 엔진 서버와 통신 -2
def get_answer_form_engine(bottype, query):
    #챗봇 에진 서버 연결
    mySocket = socket.socket()
    mySocket.connect((host, port))
    
    #챗봇 엔진 질의 요청
    json_data = {
        'Query':query,
        'BotType':bottype
    }
    message = json.dumps(json_data)
    mySocket.send(message.encode())
    
    #챗봇 엔진 답변 출력
    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data)
    
    #서버 연결 소켓 닫기
    mySocket.close()
    
    return ret_data

#챗봇 에진 query 전송 api - 3
@app.route('/query/<bot_type>', methods=['POST'])
def query(bot_type):
    body = request.get_json()
    
    try:
        if bot_type == 'TEST':
            #챗봇 API 테스트
            ret = get_answer_form_engine(bottype=bot_type, query=body['query'])
            print(jsonify(ret))
            return jsonify(ret)
        else:
            #정의되지 않은 bot typeㅇ니 경우 404 오류
            abort(404)
    except Exception as ex:
        #오류 발생시 500 오류
        abort(500)

if __name__ == '__main__':
    app.run()
    
#-1
#챗봇 엔진 서버(bot.py) 접속에 필요한 host port 변수에 저장

#-2
#get_answer_form_engine() 함수는 챗봇 엔진 서버에 소켓 통신으로 질의를 전송함
#서버로부터 성공적으로 답변 데이터를 수신한 경우 응답으로 받은 json 문자열을 딕셔너리 객체로 반환함
#chatbot_client_test.py에 자세한 설명 보기

#-3
#<bot_type>동적 변수에는 api를 호출하는 메신저 플랫폼 명칭이 할당되어 있다.
#여기서는 TEST라는 명칭을 예시로 사용
#request.get_json()함수를 통해 post /query/<bot_type> api 요청 시 body에 담긴 json 데이터를 딕셔너리 형태로 가져옴
#다음 -2에서 정의한 get_answer_from_engine() 함수를 사용해 챗봇 엔진 서버로부터 답변을 받아옴