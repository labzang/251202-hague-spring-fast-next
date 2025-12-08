"""
타이타닉 데이터 서비스
판다스, 넘파이, 사이킷런을 사용한 데이터 처리 및 머신러닝 서비스
"""
import sys
from pathlib import Path
from typing import List, Dict, Optional, Any, ParamSpecArgs
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from icecream import ic
from app.titanic.titanic_method import TitanicMethod

# 공통 모듈 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))




class TitanicService:
    """타이타닉 데이터 처리 및 머신러닝 서비스"""
    
    def __init__(self):
        pass

    def preprocess(self):
        ic("😎😎 전처리 시작")
        the_method = TitanicMethod()
        df_train = the_method.new_model('train.csv')
        df_test = the_method.new_model('test.csv')
        this_train = the_method.create_train(df_train, 'Survived')
        this_test = the_method.create_train(df_test, 'Survived')
        ic(f'1. Train 의 type \n {type(this_train)} ')
        ic(f'2. Train 의 column \n {this_train.columns} ')
        ic(f'3. Train 의 상위 1개 행\n {this_train.head()} ')
        ic(f'4. Train 의 null 의 갯수\n {this_train.isnull().sum()}개')
        ic(f'5. Test 의 type \n {type(this_test)}')
        ic(f'6. Test 의 column \n {this_test.columns}')
        ic(f'7. Test 의 상위 1개 행\n {this_test.head()}개')
        ic(f'8. Test 의 null 의 갯수\n {this_test.isnull().sum()}개')
        ic("😎😎 전처리 완료")

    def modeling(self):
        ic("😎😎 모델링 시작")
        ic("😎😎 모델링 완료")

    def learning(self):
        ic("😎😎 학습 시작")
        ic("😎😎 학습 완료")

    def evaluate(self):
        ic("😎😎 평가 시작")
        ic("😎😎 평가 완료")


    def submit(self):
        ic("😎😎 제출 시작")
        ic("😎😎 제출 완료")