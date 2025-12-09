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
        # CSV 파일 경로 설정
        current_file = Path(__file__).resolve()
        # app/titanic/titanic_service.py -> app/resources/titanic/
        resources_dir = current_file.parent.parent / "resources" / "titanic"
        self.train_csv_path = resources_dir / "train.csv"
        self.test_csv_path = resources_dir / "test.csv"
    
    def _get_csv_path(self, filename: str) -> Path:
        """
        CSV 파일의 전체 경로를 반환
        Args:
            filename: CSV 파일명 (train.csv 또는 test.csv)
        Returns:
            CSV 파일의 Path 객체
        """
        if filename == "train.csv":
            return self.train_csv_path
        elif filename == "test.csv":
            return self.test_csv_path
        else:
            # 기본적으로 resources/titanic 폴더에서 찾기
            current_file = Path(__file__).resolve()
            resources_dir = current_file.parent.parent / "resources" / "titanic"
            return resources_dir / filename

    def preprocess(self) -> Dict[str, Any]:
        """
        타이타닉 데이터 전처리 실행
        Returns:
            전처리 결과 정보 딕셔너리
        """
        ic("😎😎 전처리 시작")
        the_method = TitanicMethod()

        train_csv_path = self._get_csv_path('train.csv')
        ic(f"😎😎😎 트레인 CSV 파일 경로: {train_csv_path}")
        df_train = the_method.new_model(str(train_csv_path))
        this_train = the_method.create_train(df_train, 'Survived')
        ic(f'1. Train 의 type \n {type(this_train)} ')
        ic(f'2. Train 의 column \n {this_train.columns} ')
        ic(f'3. Train 의 상위 5개 행\n {this_train.head(5)} ')
        ic(f'4. Train 의 null 의 갯수\n {the_method.check_null(this_train)}개')

        test_csv_path = self._get_csv_path('test.csv')
        ic(f"👽👽👽 테스트 CSV 파일 경로: {test_csv_path}")
        df_test = the_method.new_model(str(test_csv_path))
        this_test = the_method.create_test(df_test, 'Survived')
        ic(f'1. Test 의 type \n {type(this_test)} ')
        ic(f'2. Test 의 column \n {this_test.columns} ')
        ic(f'3. Test 의 상위 5개 행\n {this_test.head(5)} ')
        ic(f'4. Test 의 null 의 갯수\n {the_method.check_null(this_test)}개')
        
        drop_features = ['SibSp', 'Parch', 'Cabin', 'Ticket']
        this_train , this_test = the_method.drop_feature(this_train, this_test, *drop_features)
        this_train , this_test = the_method.pclass_ordinal(this_train, this_test)
        this_train , this_test = the_method.fare_ordinal(this_train, this_test)
        this_train , this_test = the_method.embarked_ordinal(this_train, this_test)
        this_train , this_test = the_method.gender_nominal(this_train, this_test)
        this_train , this_test = the_method.extract_title(this_train, this_test)  # Name에서 Title 추출
        this_train , this_test = the_method.age_ratio(this_train, this_test)
        this_train , this_test = the_method.title_nominal(this_train, this_test)
        drop_name = ['Name']
        this_train , this_test = the_method.drop_feature(this_train, this_test, *drop_name)

        ic("😎😎😎 트레인 전처리 완료")
        ic(f'1. Train 의 type \n {type(this_train)} ')
        ic(f'2. Train 의 column \n {this_train.columns} ')
        ic(f'3. Train 의 상위 5개 행\n {this_train.head(5)} ')
        ic(f'4. Train 의 null 의 갯수\n {the_method.check_null(this_train)}개')

        ic("👽👽👽 테스트 전처리 완료")
        ic(f'1. Test 의 type \n {type(this_test)} ')
        ic(f'2. Test 의 column \n {this_test.columns} ')
        ic(f'3. Test 의 상위 5개 행\n {this_test.head(5)} ')
        ic(f'4. Test 의 null 의 갯수\n {the_method.check_null(this_test)}개')
        
        # 전처리 결과 정보 반환
        return {
            "status": "success",
            "rows": len(this_train),
            "columns": this_train.columns.tolist(),
            "column_count": len(this_train.columns),
            "null_count": int(the_method.check_null(this_train)),
            "sample_data": this_train.head(5).to_dict(orient="records"),
            "dtypes": this_train.dtypes.astype(str).to_dict()
        }

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