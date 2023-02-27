import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.Preprocess import Preprocess
sent = "내일 오전 10시에 탕수육 주문하고 싶어"

#전처리 객체 생성
p = Preprocess(userdic='')