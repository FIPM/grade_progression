import numpy as np
import pandas as pd
import random

def train_val_test_split(db,propTrain=.7,propTest=.15):
    '''Function splits a dataset in train, validate, and test datasets.
    propTrain is the proportion of rows to be use in the train dataset.
    propTest is the proportion of rows to be use in the test dataset.
    propTrain+propTest+propVal=1'''
    # after train size, the remainder is splitted by propTest
    random.seed(42)    
    # Min and Max grade in database
    min_LG=np.min(db['LastGrade'].values)
    max_LG=np.max(db['LastGrade'].values)    

    # Selecting random positions for the 3 databases: Train, Test, Validation.    
    trainPosition=[]
    testPosition=[]
    validationPosition=[]
    # making sure all databases have all grades
    for g in range(min_LG,max_LG+1):
        rows=db[db['LastGrade']==g].index.tolist()
        trainPosition=trainPosition+random.sample(rows,k=np.ceil(propTrain*len(rows)).astype(int))
        rows=list(set(rows).difference(set(trainPosition)))
        validationPosition=validationPosition+random.sample(rows,k=np.ceil((1-propTest/(1-propTrain))*len(rows)).astype(int))
        testPosition=testPosition+list(set(rows).difference(set(validationPosition)))

    # Generating databases
    dbTrain=db.loc[trainPosition,:].copy()    
    dbValidation=db.loc[validationPosition,:].copy()
    dbTest=db.loc[testPosition,:].copy()
    return dbTrain, dbValidation, dbTest