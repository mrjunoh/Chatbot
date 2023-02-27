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
    #테이블 생성 sql 정의
    sql = '''
    CREATE TABLE tb_student(
        id int primary key auto_increment not null,
        name varchar(32),
        age int,
        address varchar(32)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    '''
    #테이블 생성
    with db.cursor() as cursor:
        cursor.execute(sql)
    
except Exception as e:
    print(e) #연결 실패 오류
finally:
    if db is not None: #db가 연결된 경우에만 접속 닫기 시도
        db.close()
        print('닫기 성공')


#연결한 db와 상호 작용하러면 cursor객체가 필요ㅑ함
#cursor 객체는 우리가 임의로 생성할 수 없으며 db 호스트에 연결된 객체(db)의 cursor()함수로 cursor객체를 받아와야함
#cursor 객체의 execute() 함수로 sql 구문을 실행함
#with 구문 내에서 cursor 객체를 사용하기 때문에 사용 후에는 자동으로 메모리에서 해제됨

#ssd