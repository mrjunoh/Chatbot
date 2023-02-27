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
    #데이터 삽입 sql 정의
    sql = '''
    INSERT tb_student(name, age, address) value('Kei', 35, 'Korea')
    '''
    #데이터 삽입
    with db.cursor() as cursor:
        cursor.execute(sql)
    db.commit()
    
except Exception as e:
    print(e) #연결 실패 오류
finally:
    if db is not None: #db가 연결된 경우에만 접속 닫기 시도
        db.close()
        print('닫기 성공')