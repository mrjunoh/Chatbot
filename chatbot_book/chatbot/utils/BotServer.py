#챗봇 서버 모듈
import socket

class BotServer:
    def __init__(self, srv_port, listen_num): #-1
        self.port = srv_port
        self.listen = listen_num
        self.mySock = None
        
    #sock 생성 -2
    def create_sock(self):
        self.mySock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySock.bind(("0.0.0.0", int(self.port)))
        self.mySock.listen(int(self.listen))
        return self.mySock
    
    #client 대기 -3
    def ready_for_client(self):
        return self.mySock.accept()
    
    #sock 반환 - 4
    def get_sock(self):
        return self.mySock

#-1
#botserver 객체의 생성자 
#인자로 사용된 생성할 소켓 서버의 포트번호(srv_port)와 동시에 연결을 수락할 클라이언트 수 (client_num)를 변수로 저장

#-2
#botserver의 소켓을 생성하는 메서드 
#tcp/ip 소켓을 생성한 뒤 지정한 서버 포트(self.port)로 지정한 연결 수(self.listen)만큼 클라이언트 연결을 수락하도록 함

#-3
#챗봇 클라이언트 연결을 대기하고 있다가 연결을 수락하는 메서드
#서버 소켓은 우리가설정한 주소와 통신에 바인드되어 클라이언트 연결을 주시(listening socket)하고 있어야함
#client가 연결을 요청하는 즉시 accept()함수는 클라이언트와 통신할 수 있는 클라이언트용 소켓 객체를 반환함