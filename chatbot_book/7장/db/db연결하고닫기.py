import pymysql

db = None
try:
    #db호스트 정보에 맞게 입력
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='qkrwnsdh123@',
        db='homestead',
        charset='utf8'
    )
    print('연결 성공')
except Exception as e:
    print(e) #연결 실패 오류
finally:
    if db is not None: #db가 연결된 경우에만 접속 닫기 시도
        db.close()
        print('닫기 성공')
