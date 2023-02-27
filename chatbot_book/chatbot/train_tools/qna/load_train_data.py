import sys, os
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))
# sys.path.append(os.path.abspath(os.path.abspath(os.path.dirname(__file__))))
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import pymysql
import openpyxl
from config.DatabaseConfig import * #db 접속 정보 불러오기

#학습 데이터 초기화 - 1
def all_clear_train_data(db):
    #기존 학습 데이터 삭제
    sql = '''
    delete from chatbot_train_data
    ''' #delete 명령어를 이용해 테이블 내용 삭제 시켜주고
    with db.cursor() as cursor:
        cursor.execute(sql)
    
    #auto increment 초기화
    sql = '''
    ALTER TABLE chatbot_train_data AUTO_INCREMENT=1
    ''' #auto_increment 속성을 1로 초기화해줌
    with db.cursor() as cursor:
        cursor.execute(sql)
    
#db에 저장 - 2
def insert_data(db, xls_row):
    intent, ner, query, answer, answer_img_url = xls_row

    sql = '''
        INSERT chatbot_train_data(intent, ner, query, answer, answer_image) 
        values(
         '%s', '%s', '%s', '%s', '%s'
        )
    ''' % (intent.value, ner.value, query.value, answer.value, answer_img_url.value)
    
    #엑셀에서 불러온 cell에 데이터가 없는 경우 null로 처리
    sql = sql.replace("'None'", "null")

    with db.cursor() as cursor:
        cursor.execute(sql)
        print('{} 저장'.format(query.value))
        db.commit()
    
train_file = 'C:/Users/ETRI/Desktop/처음배우는 딥러닝 챗봇/chatbot/train_tools/qna/train_data.xlsx'
db= None
try:
    db = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        db=DB_NAME,
        charset='utf8'
    )
    
    #기존 학습 데이터 초기화 - 1
    all_clear_train_data(db)
    
    #학습 엑셀 파일 불러오기 - 2
    wb = openpyxl.load_workbook(train_file)
    sheet = wb['Sheet1'] #엑셀에서 1번 시트를 지정 해서 
    for row in sheet.iter_rows(min_row=2): #헤더는 불러오지 않음 #즉 min_row=2는 2번 시트부터 출력한다는 뜻
        #데이터 저장
        insert_data(db, row)
    
    wb.close()
except Exception as e:
    print(e)
finally:
    if db is not None:
        db.close()
        

#-1
#load_train_data 프로그램을 실행할 때마다 엑셀 파일 내부의 데이터와 
#db 내 학습 데이터를 동일하게 유지하기 위해 db 데이터를 초기화함
#all_clear_train_data 함수 내에서 
#delete 명령어를 이용해 테이블 내용 삭제 시켜주고
#auto_increment 속성을 1로 초기화해줌

#-2
#openpyxl 모듈을 이용해 엑셀 파일을 일겅와 db에 데이터를 저장
#insert_data함수는 INSERT 명령어를 사용해 엑셀에서 불러온 데이터 열을 db에 저장하는 함수