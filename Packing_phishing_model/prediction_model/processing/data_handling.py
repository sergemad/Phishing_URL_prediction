import os
import pandas as pd
import joblib


from pathlib import Path
import sys

PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))
from prediction_model.config import config

#Load the dataset
def load_dataset(file_name):
    if file_name == config.TEST_FILE:
        filepath = os.path.join(config.TEST_DATAPATH,file_name)
        dataset = pd.read_csv(filepath) 
    else:
        filepath = os.path.join(config.DATAPATH,file_name)
        dataset = pd.read_csv(filepath)

    return dataset[config.X], dataset[config.TARGET]

#Save the test dataset
def save_test_dataset(X,y):
    filepath = os.path.join(config.TEST_DATAPATH,config.TEST_FILE)
    
    if isinstance(X, pd.DataFrame) == False:
        X = pd.DataFrame(X)
    if isinstance(y, pd.Series) == False:
        y = pd.Series(y)
    
    X[config.TARGET] = y
    
    X.to_csv(filepath, index=False)

# Serialization
def save_pipeline(pipeline_to_save):
    save_path = os.path.join(config.SAVE_MODEL_PATH, config.MODEL_NAME)
    joblib.dump(pipeline_to_save, save_path)
    print(f"The Model has been saved under the name {config.MODEL_NAME}")

# Deserialization
def load_pipeline():
    save_path = os.path.join(config.SAVE_MODEL_PATH, config.MODEL_NAME)
    model_loaded = joblib.load(save_path)
    print(f"The Model has been loaded")
    return model_loaded