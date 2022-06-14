# imports
import pandas as pd
import os
from sklearn.pipeline import make_pipeline
from data_processing import train_val_test_split
from custom_standar_scaler import CustomStandarScaler
from custom_pca import CustomPCA
from custom_ensemble_model import CustomEnsembleModel


if __name__=='__main__':
    
    # Loading data
    file_path = os.path.join('.','raw_data','data.csv')
    db = pd.read_csv(file_path)
    
    dbTrain, dbValidation, dbTest = train_val_test_split(db,propTrain=.7,propTest=.15)

    # Measures to extract student performance at school
    listFeaturesPCA=['measure_M_std','measure_L_std']
    
    # features for model training
    listFeatures=['studentPerformace']
    
    # models to train
    grades=[4,5,6,7,8,9] 

    # pipeline
    pipe = make_pipeline(
        CustomStandarScaler(),
        CustomPCA(listFeaturesPCA),        
        )
    
    pipeline = make_pipeline(
        pipe,
        CustomEnsembleModel(grades, listFeatures),    
        )

    # model train and validation
    print('Training the model')
    pipeline.fit_transform(dbTrain)
    print('Validating the model')
    dbValidation = pipeline.predict(dbValidation)
    
    # testing the model
    print('Testing the model')
    dbTest = pipeline.predict(dbTest)
    dbTest.to_csv(os.path.join('.','data','Fig4.csv'))
    
    print('Generating database for figure')
    db_Fig3 = pipe.fit_transform(db)
    db_Fig3.to_csv(os.path.join('.','data','Fig3.csv'))
    
    print('Done')
    
    
    
