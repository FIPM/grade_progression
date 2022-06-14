from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from scipy import stats
import pandas as pd
import numpy as np

class CustomEnsembleModel(BaseEstimator, ClassifierMixin):
    def __init__(self, grades, listFeatures):
        self.listModelsByGrade=None
        self.listFeatures=listFeatures
        self.grades=grades
        
    def transform(self, db, y=None):
        pass
    
    def fit(self, db, y=None):
    
        # To keep track of models, features selected
        listModelsByGrade=[[],[],[],[]]
        listFeatures = self.listFeatures
        grades = self.grades
        

        # Model estimation
        for grade in grades:
            # SVC
            types_svc=[]
            models_svc=[]
            for i3 in ['rbf','linear']:
                config=(i3,[])
                type='SVC'
                model=self.trainFunc(db,listFeatures,config,type,grade)
                types_svc=types_svc+[type]
                models_svc=models_svc+model   
            # KNC
            types_knn=[]
            models_knn=[]
            for i1 in [1]:
                for i2 in ['distance','uniform']:
                    for i3 in ['ball_tree', 'kd_tree', 'brute']:
                        config=(i1,i2,i3)
                        type='KNC'
                        model=self.trainFunc(db,listFeatures,config,type,grade)
                        types_knn=types_knn+[type]
                        models_knn=models_knn+model       
            # DTC
            types_tree=[]
            models_tree=[]        
            for i4 in ['best','random']:
                config=(i4,[])
                type='DTC'
                model=self.trainFunc(db,listFeatures,config,type,grade)
                types_tree=types_tree+[type]
                models_tree=models_tree+model 

            # One position by grade
            listModelsByGrade.append([types_svc,models_svc,types_knn,models_knn,types_tree,models_tree])
            self.listModelsByGrade=listModelsByGrade
        return self
    
    def trainFunc(self, db, listFeatures, input, type, Grade):    
        X=db[listFeatures].values
        db['LastGrade_aux']=1*(db['LastGrade']>=Grade)
        y=db['LastGrade_aux'].values
        if type=='KNC':    
            # KNC
            knn_k=input[0]
            knn_weights=input[1]    
            knn_algorithm=input[2]
            y=pd.get_dummies(db[['LastGrade_aux']].astype(str))
            y=y[y.columns].values
            knn_clf = KNeighborsClassifier(n_neighbors=knn_k, weights=knn_weights,algorithm=knn_algorithm)
            knn_clf.fit(X, y)
            output=knn_clf
        elif type=='SVC':
            # SVC
            svc_kernel=input[0]
            svm_clf = SVC(gamma="auto", kernel=svc_kernel,random_state=42)
            svm_clf.fit(X, y) 
            output=svm_clf
        elif type=='DTC':
            # DTC
            tree_splitter=input[0]
            tree_dtc = DecisionTreeClassifier(random_state=42,splitter=tree_splitter)
            tree_dtc.fit(X, y) 
            output=tree_dtc
        return [output]
    
    def prediction(self, dbP, models, types, Grade):
        dbP['LastGrade_aux']=1*(dbP['LastGrade']>=Grade)
        X=dbP[self.listFeatures].values
        for m in range(0,len(models)):
            model=models[m]
            if types[m]=='KNC':   
                if m==0:
                    preds=model.predict(X)@np.sort(dbP['LastGrade_aux'].unique())[:,np.newaxis]
                else:                                
                    preds=np.concatenate((preds,model.predict(X)@np.sort(dbP['LastGrade_aux'].unique())[:,np.newaxis]),axis=1)                
            else:
                if m==0:
                    preds=model.predict(X)[:,np.newaxis]
                else:                
                    preds=np.concatenate((preds,model.predict(X)[:,np.newaxis]),axis=1)                
        return preds
    
    def voter(self, dbP, preds, Grade):
        dbP['LastGrade_aux']=1*(dbP['LastGrade']>=Grade)
        m = stats.mode(preds,axis=1)
        y_pred=m[0].ravel()*(m[1].ravel()>=np.max(m[1].ravel()))
        dbP['y_pred']=y_pred
        y=dbP['LastGrade_aux'].values    
        Precision=np.sum((y_pred==1)*(y==1))/np.sum(y_pred==1)
        Recall=np.sum((y_pred==1)*(y==1))/np.sum(y==1)
        F1=2*(Precision*Recall)/(Precision+Recall) 
        Precision=np.round(Precision,decimals=2)
        Recall=np.round(Recall,decimals=2)
        F1=np.round(F1,decimals=2)
        return [Precision,Recall,F1,y_pred]
    
    def predict(self, db):
    
        listPreds=[] # keep track of best prediction by model type
        grades = self.grades
        listModelsByGrade = self.listModelsByGrade

        for grade in grades:

            # access trained models 
            types_svc = listModelsByGrade[grade][0]
            models_svc = listModelsByGrade[grade][1]
            types_knn = listModelsByGrade[grade][2]
            models_knn =  listModelsByGrade[grade][3]
            types_tree = listModelsByGrade[grade][4]
            models_tree = listModelsByGrade[grade][5]

            # SVC
            preds=self.prediction(db,models_svc,types_svc,grade)   
            metric=self.voter(db,preds,grade) # find the best prediction
            listPreds=metric[3][:,np.newaxis]

            # KNC
            preds=self.prediction(db,models_knn,types_knn,grade)   
            metric=self.voter(db,preds,grade) # find the best prediction
            listPreds=np.concatenate((listPreds,metric[3][:,np.newaxis]),axis=1)

            # TREE
            preds=self.prediction(db,models_tree,types_tree,grade)   
            metric=self.voter(db,preds,grade) # find the best prediction
            listPreds=np.concatenate((listPreds,metric[3][:,np.newaxis]),axis=1)

            metric=self.voter(db,listPreds,grade) # find the best of best predictions
            
            name='PrecisionLastGrade_'+str(grade)
            db[name]=metric[0] #saving for ploting

            name='RecallLastGrade_'+str(grade)
            db[name]=metric[1] #saving for ploting

            name='F1LastGrade_'+str(grade)        
            db[name]=metric[2] #saving for ploting

            name='predLastGrade_'+str(grade)
            db[name]=metric[3] #To identify students

            print('Grade='+str(grade)+' Precision='+str(np.round(metric[0],decimals=2))+' Recall='+str(np.round(metric[1],decimals=2))+' F1='+str(np.round(metric[2],decimals=2)))
        return db
    