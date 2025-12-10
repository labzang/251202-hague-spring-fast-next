import pandas as pd
import numpy as np
from pandas import DataFrame
import logging
from app.seoul_crime.seoul_data import SeoulData

logger = logging.getLogger(__name__)

class SeoulMethod(object): 

    def __init__(self):
        self.dataset = SeoulData()

    def read_csv(self, fname: str) -> pd.DataFrame:
        return pd.read_csv(fname)

    def create_df(self, df: DataFrame, label: str) -> pd.DataFrame:
        """
        DataFrame을 그대로 반환합니다.
        (Survived 컬럼을 학습/평가에 활용하기 위해 제거하지 않습니다.)
        """
        return df