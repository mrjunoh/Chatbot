import pymysql
import pandas as pd

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
    
    #데이터 db에 추가
    students =[
        {'name':'tony', 'age':34, 'address':'pusan'},
        {'name':'jaeyoo', 'age':39, 'address':'pusan'},
        {'name':'grace', 'age':28, 'address':'changwon'},
        {'name':'jenny', 'age':20, 'address':'seoul'}
    ]
    for s in students:
        with db.cursor() as cursor:
            sql='''
            insert tb_student(name, age, address) values("%s",%d,"%s")
            ''' % (s['name'], s['age'], s['address'])
            cursor.execute(sql)
    db.commit()
    
    #30대 조회
    cond_age = 30
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        sql ='''
        select * from tb_student 
        where age > %d
        ''' % cond_age
        cursor.execute(sql)
        results = cursor.fetchall() #fetchall 함수는 select 구문으로 조회한 모든 데이터를 불러오는 함수
    print(results)
    
    #이름 검색
    cond_name = 'grace'
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        sql ='''
        select * from tb_student
        where name ="%s"
        ''' % cond_name
        cursor.execute(sql)
        result = cursor.fetchone() #fetchone은 select 구문을 통해 조회한 데이터 중 1개의 행만 불러오는 함수
    print(result['name'], result['age'])
    
    #데이터프레임 표현
    df = pd.DataFrame(results)
    print(df)
        
    
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