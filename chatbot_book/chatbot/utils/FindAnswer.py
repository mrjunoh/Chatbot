class FindAnswer:
    def __init__(self, db): # -1
        self.db = db
    
    # 검색 쿼리 생성
    def _make_query(self, intent_name, ner_tags):
        sql = "select * from chatbot_train_data"
        if intent_name != None and ner_tags == None:
            sql = sql + " where intent='{}' ".format(intent_name)

        elif intent_name != None and ner_tags != None:
            where = ' where intent="%s" ' % intent_name
            if (len(ner_tags) > 0):
                where += 'and ('
                for ne in ner_tags:
                    where += " ner like '%{}%' or ".format(ne)
                where = where[:-3] + ')'
            sql = sql + where
        
        #동일한 답변이 2개 이상인 경우 랜덤으로 선택
        sql = sql + " order by rand() limit 1"
        return sql
    
    #답변 검색ㅍ -2
    def search(self, intent_name, ner_tags):
        # 의도명, 개체명으로 답변 검색
        sql = self._make_query(intent_name, ner_tags)
        answer = self.db.select_one(sql)

        # 검색되는 답변이 없으면 의도명만 검색
        if answer is None:
            sql = self._make_query(intent_name, None)
            answer = self.db.select_one(sql)

        return (answer['answer'], answer['answer_image'])
    
    #ner 태그를 실제 입력된 단어로 변환 -3
    def tag_to_word(self, ner_predicts, answer):
        for word, tag in ner_predicts:

            # 변환해야하는 태그가 있는 경우 추가
            if tag == 'B_FOOD' or tag == 'B_DT' or tag == 'B_TI':
                answer = answer.replace(tag, word)

        answer = answer.replace('{', '')
        answer = answer.replace('}', '')
        return answer
    
    
#-1
#FindAnser 클래스 생성자 
#Database.py(데이터베이스 제어 모듈)에서 생성한 Database 인스턴스 객체를 인자로 받아 클래스 멤버 변수로 저장

#-2
#def search는 의도명(intent_name)과 개체명 태그 리스트(ner_tags)르 이용해 질문의 답변을 검색하는 메서드
#인자로 제공된 2가지 정보(의도명, 개체명 태그 리스트)로 답변 검색 시 실패 할수도 있음
#실패할 경우 의도명만 이용해 답변을 검색함
#챗봇 엔진이 찾는 정확한 조건의 답변이 없는 경우 차선책으로 동일한 의도를 가지는 답변을 검색
#의도가 동일한 경우 답변도 유사할 확률이 높음
#이 방법은 구현하기 쉽지만 학습데이터 양이 많아지고 이는 룰 베이스 기반 검색 방식의 한계를 보여줌

# def _make_query는 의도명과 개체명 태그를 기반으로 검색 쿼리를 생성하는 함수
#의도명만 검색할지, 여러 종류의 개체명 태그와 함께 검색할지 결정하는 조건을 만드는 함수

#-3
#검색된 답변 텍스트에서 NER 태그 변수를 실제 입력된 단어로 변환하는 함수
#예로 '자장면 주문' 텍스트가 입력되면 자장면은 'B_FOOD' 개체명으로 인식
#이때 검색된 답변이 {'b_food'} 주문 처리 완료되었습니다. 주문해주셔서 감사합니다.
#라 하면 답변 내용속 {b_food}를 자장면으로 변환해주는 함수 