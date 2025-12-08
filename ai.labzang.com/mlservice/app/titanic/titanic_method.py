from pathlib import Path
import pandas as pd
from app.titanic.titanic_dataset import TitanicDataSet

class TitanicMethod(object): 

    def __init__(self):
        self.dataset = TitanicDataSet()

    def new_model(self) -> pd.DataFrame:
        return pd.read_csv("train.csv")

    def create_train(self) -> pd.DataFrame:
        return self.new_model().drop(columns=['Survived'])

    def create_label(self) -> pd.DataFrame:
        return self.new_model()[['Survived']]