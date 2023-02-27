#동적 변수 처리 방법

from flask import Flask 
app = Flask(__name__) 

@app.route('/') 
def hello():
    return 'hello flask'

@app.route('/info/<name>') #-1
def get_name(name):
    return "hello {}".format(name)

@app.route('/user/<int:id>') #-2
def get_user(id):
    return "user id is {}".format(id)

#-3
@app.route('/json/<int:dest_id>/<message>') 
@app.route('/JSON/<int:dest_id>/<message>')
def send_message(dest_id, message):
    json = {
        "bot_id":dest_id,
        "message":message
    }
    return json

if __name__ =='__main__': 
    app.run() #app.run(host='127.0.0.1', port='5000')이 생략되어있음
    

#-1
#'/info/<name>' URI와 연결된 뷰 함수 이다. 
#여기서 <name>은 URI에서 사용되는 동적 변수이다.
#/info/junoh로 접속하면 해당 uri와 연결된 get_name(name) 뷰 함수를 호출한다. 
#이때 뷰 함수 인자 name에는 'junoh'가 입력됨

#-3
#하나의 뷰 함수에 여러 개의 URI를 지정할 수 있다.
#파이썬에서 딕셔너리를 이용해 JSON 데이터를 표현할 수 있다.