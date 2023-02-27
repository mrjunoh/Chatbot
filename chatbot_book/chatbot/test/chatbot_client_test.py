import socket
import json

# 챗봇 엔진 서버 접속 정보 - 1
host = "127.0.0.1"  # 챗봇 엔진 서버 IP 주소
port = 5050  # 챗봇 엔진 서버 통신 포트

# 클라이언트 프로그램 시작 - 2
while True:
    print("질문 : ")
    query = input()  # 질문 입력 2.1
    if(query == "exit"):
        exit(0)
    print("-" * 40)

    # 챗봇 엔진 서버 연결 2.2
    mySocket = socket.socket()
    mySocket.connect((host, port))

    # 챗봇 엔진 질의 요청 2.3
    json_data = {
        'Query': query,
        'BotType': "MyService"
    }
    message = json.dumps(json_data)
    mySocket.send(message.encode())

    # 챗봇 엔진 답변 출력 2.4
    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data)
    print("답변 : ")
    print(ret_data['Answer'])
    print(ret_data)
    print(type(ret_data))
    print("\n")

    # 챗봇 엔진 서버 연결 소켓 닫기
    mySocket.close()

#-1
#챗봇 엔진 서버 접속에 필요한 정보를 host와 port 변수에 정의함

#-2
#while 문한루프를 돌면서 질문을 입력할 때마다 챗봇 엔진 서버에 연결해 답변을 받아옴

#2.1
#챗봇클라이언트가 서버에서 질의를 요청하는 방법은
#input()함수를 이용해 콘솔 상에서 질문 문자열을 입력받음
#이 함수를 호출하면 키보드 입력이 있을 때까지 블로킹됨
#만약 입력이 exit면 종료

#2.2
#input()함수로 문자열이 입력되면 챗봇 엔진 서버에 연결을 시도함.
#챗봇 엔진 서버에 접속할 수 없는 경우에는 ConnectionRefusedError 예외가 발생함

#2.3
#입력 받은 질문 텍스트를 사전에 약속한 프로토콜 포맷으로 JSON 객체를 생성한 뒤 데이터 전송이 가능한 문자열 형태로 변환
#이후 utf8로 인코딩하고 챗봇 엔진 server에 문자열 데이터를 전송함

#2.4
#server로부터 응답 데이터가 수신될 때까지 기다린다.
#응답이 수신되면 해당 문자열 데이터를 유니코드로 디코딩한 후 다시 json 객체로 변환한다.
#그리고 챗봇 답변을 출력한다.