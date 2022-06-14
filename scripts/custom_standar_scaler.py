from sklearn.base import TransformerMixin, BaseEstimator
import pandas as pd

class CustomStandarScaler(TransformerMixin, BaseEstimator):
    def __init__(self):
        self.mean=None
        self.std=None
        
    def fit(self,db):
        dm=db.groupby(['Cod_Estab']).agg(
            measure_L_std=('measure_L',lambda x:x.std()),
            measure_M_std=('measure_M',lambda x:x.std())
            )
        dm.reset_index(inplace=True)
        self.std = dm
        return self
    
    def transform(self,db):
        db = db.merge(self.std,how='left',left_on='Cod_Estab',right_on='Cod_Estab')
        db['measure_M_std']=db['measure_M']/db['measure_M_std']
        db['measure_L_std']=db['measure_L']/db['measure_L_std']

        db = db[db.measure_M_std > -20]
        db = db[db.measure_L_std > -20]
        return db
        