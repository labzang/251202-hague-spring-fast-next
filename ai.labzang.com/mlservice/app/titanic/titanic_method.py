from pathlib import Path
from typing import Tuple
import pandas as pd
import numpy as np
from pandas import DataFrame
from app.titanic.titanic_dataset import TitanicDataSet
from icecream import ic

class TitanicMethod(object): 

    def __init__(self):
        self.dataset = TitanicDataSet()

    def read_csv(self, train_fname: str, test_fname: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return ( pd.read_csv(train_fname) , pd.read_csv(test_fname))

    def create_df(self, train_df: DataFrame, test_df: DataFrame, label: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return (train_df.drop(columns=[label]), test_df.drop(columns=[label]))

    def create_label(self, train_df: DataFrame, test_df: DataFrame, label: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return (train_df[[label]], test_df[[label]])

    def drop_feature(self, train_df: DataFrame, test_df: DataFrame, *feature: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return (train_df.drop(columns=[x for x in feature]), test_df.drop(columns=[x for x in feature]))

    def check_null(self, train_df: DataFrame, test_df: DataFrame) -> int:
        return int(train_df.isnull().sum().sum(), test_df.isnull().sum().sum())
    
    def extract_title_from_name(self, train_df: DataFrame, test_df: DataFrame):
        # for i in [df.train, df.test]:
        #     i['Title'] = i['Name'].str.extract('([A-Za-z]+)\.', expand=False) 

        [i.__setitem__('Title', i['Name'].str.extract('([A-Za-z]+)\.', expand=False)) 
         for i in [train_df, test_df]]
            # expand=False 는 시리즈 로 추출
        return (train_df, test_df)
    

    def remove_duplicate_title(self, train_df: DataFrame, test_df: DataFrame):
        a = []
        for i in [train_df, test_df]:
            # a.append(i['Title'].unique())
            a += list(set(i['Title'])) # train, test 두번을 누적해야 해서서
        a = list(set(a)) # train, test 각각은 중복이 아니지만, 합치면서 중복발생
        print("🐞🐞🐞")
        print(a)
        # ['Mr', 'Miss', 'Dr', 'Major', 'Sir', 'Ms', 'Master', 'Capt', 'Mme', 'Mrs', 
        #  'Lady', 'Col', 'Rev', 'Countess', 'Don', 'Mlle', 'Dona', 'Jonkheer']
        '''
        ['Mr', 'Sir', 'Major', 'Don', 'Rev', 'Countess', 'Lady', 'Jonkheer', 'Dr',
        'Miss', 'Col', 'Ms', 'Dona', 'Mlle', 'Mme', 'Mrs', 'Master', 'Capt']
        Royal : ['Countess', 'Lady', 'Sir']
        Rare : ['Capt','Col','Don','Dr','Major','Rev','Jonkheer','Dona','Mme' ]
        Mr : ['Mlle']
        Ms : ['Miss']
        Master
        Mrs
        '''
        title_mapping = {'Mr': 1, 'Ms': 2, 'Mrs': 3, 'Master': 4, 'Royal': 5, 'Rare': 6}
        
        return (train_df, test_df)
    

    def title_nominal(self, train_df: DataFrame, test_df: DataFrame, title_mapping):
        for i in [train_df, test_df]:
            i['Title'] = i['Title'].replace(['Countess', 'Lady', 'Sir'], 'Royal')
            i['Title'] = i['Title'].replace(['Capt','Col','Don','Dr','Major','Rev','Jonkheer','Dona','Mme'], 'Rare')
            i['Title'] = i['Title'].replace(['Mlle'], 'Mr')
            i['Title'] = i['Title'].replace(['Miss'], 'Ms')
            # Master 는 변화없음
            # Mrs 는 변화없음
            i['Title'] = i['Title'].fillna(0)
            i['Title'] = i['Title'].map(title_mapping)
            
        return (train_df, test_df)          
        


    def pclass_ordinal(self, df: DataFrame):
        return df

    def gender_nominal(self, df: DataFrame):

        gender_mapping = {'male': 0, 'female': 1}
        # for i in [df.train, df.test]:
        #     i["Gender"] = i["Sex"].map(gender_mapping)
        [i.__setitem__('Gender',i['Sex'].map(gender_mapping)) 
         for i in [df.train, df.test]]
        return df

    def age_ratio(self, df: DataFrame):
        
        self.get_count_of_null(df,"Age")
        for i in [df.train, df.test]:
            i['Age'] = i['Age'].fillna(-0.5)
        self.get_count_of_null(df,"Age")
        train_max_age = max(df.train['Age'])
        test_max_age = max(df.test['Age'])
        max_age = max(train_max_age, test_max_age)
        print("🌳👀🦙⭕🛹최고령자", max_age)
        bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf]
        labels = ['Unknown','Baby','Child','Teenager','Student','Young Adult','Adult', 'Senior']
        age_mapping = {'Unknown':0 , 'Baby': 1, 'Child': 2, 'Teenager' : 3, 'Student': 4,
                       'Young Adult': 5, 'Adult':6,  'Senior': 7}
        for i in [df.train, df.test]:
            i['AgeGroup'] = pd.cut(i['Age'], bins, labels=labels).map(age_mapping)
        
        return df
    
    def get_count_of_null( self, df: DataFrame, feature):
        for i in [df.train, df.test]:
            null_count = i[feature].isnull().sum()
            print("🌳👀🦙⭕🛹빈값의 갯수", null_count)
    

    def fare_orinal(self, df: DataFrame):
        for i in [df.train, df.test]:
            i['FareBand'] = pd.qcut(i['Fare'], 4, labels={1,2,3,4})

        df.train = df.train.fillna({'FareBand': 1})
        df.test = df.test.fillna({'FareBand': 1})
        
        return df


    def embarked_nominal(self, df: DataFrame):
        for i in [df.train, df.test]:
            i['Embarked'] = i['Embarked'].fillna('S')# 사우스햄튼이 가장 많으니까
        embarked_mapping = {'S':1, 'C':2, 'Q':3}
        df.train['Embarked'] = df.train['Embarked'].map(embarked_mapping)
        df.test['Embarked'] = df.test['Embarked'].map(embarked_mapping)
        return df

    def kwargs_sample(**kwargs) -> None:
        # for key, value in kwargs.items():
        #     print(f'키워드: {key} 값: {value}')
        {print(''.join(f'키워드: {key} 값: {value}')) for key, value in kwargs.items()}

