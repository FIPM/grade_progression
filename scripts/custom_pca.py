from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.decomposition import PCA

class CustomPCA(TransformerMixin, BaseEstimator):
    def __init__(self, listVars):
        self.pca=PCA(n_components=1)
        self.listVars=listVars
        
    def fit(self,db):
        self.pca.fit(db[self.listVars].values)
        return self
    
    def transform(self,db):
        db['studentPerformace']= self.pca.transform(db[self.listVars].values)[:,[0]]        
        return db