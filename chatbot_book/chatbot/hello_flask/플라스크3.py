#기본적인 rest api 서버 구현
from flask import Flask, request, jsonify #-1
app=Flask(__name__)

#서버 리소스 -2
resource = []

#사용자 정보 조회 -3
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for user in resource:
        if user['user_id'] is user_id:
            return jsonify(user)
    return jsonify(None)

#사용자 추가 -4
@app.route('/user', methods=['POST'])
def add_user():
    user = request.get_json() #http 요청의 body에서 json 데이터를 불러옴
    resource.append(user) #리소스 리스트에 추가
    return jsonify(resource)

if __name__ == '__main__':
    app.run()
    
#-1
#request모듈은 client로부터 http요청을 받았을 때 요청 정보를 확인할 수 있는 모듈
#jsonify 모듈은 데이터 객체를 json 응답으로 변환해주는 flask의 유틸리티 함수

#-2
#웹 서버의 리소스를 표현하기 위해 생성한 리스트 객체
#여기선 get, post 메서드로 호출된 rest api를 통해 해당 리소스에 객체를 추가하고 불러오도록 구현함

#-3
#user_id에 맞는 사용자 정보를 조회하는 GET 메서드의 rest api(/user/<int:user_id>)를 정의함
# get 메서드의 경우 methods를 생략 가능
#사용자 정보 조회 rest api에 연결되어 있는 get_user()함수는 리소스를 탐색해 user_id 값으로 저장된 데이터가 있다면 해당 객체를 json으로 응답함

#-4
#사용자 정보를 추가하는 post 메서드
#rest api에 연결된 add_user() 함수는 http 요청시 body에 포함된 json 데이터를 서버 리소스에 추가한 후
#현재 저장된 전체 리소스 데이터를 json으로 변환해 응답한다.
#request.get_josn() 함수를 통해 http 요청 body의 json 객체를 딕셔너리 형태로 가져 온다.
#jsonify() 함수를 통해 resource 리스트를 json 응답 형태로 반환함