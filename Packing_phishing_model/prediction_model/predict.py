import pandas as pd
from sklearn.metrics import classification_report, recall_score, accuracy_score

import os
from pathlib import Path
import sys

PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))

from prediction_model.config import config
from prediction_model.processing.data_handling import load_pipeline,load_dataset
import prediction_model.processing.preprocessing as pp

classification_pipeline = load_pipeline()


def predict(url):
    X = pd.DataFrame({config.X: [url]})
    Y_pred = classification_pipeline.predict(X)
    return Y_pred[0]


def generate_prediction():
    X_test, y_test = load_dataset(config.TEST_FILE)
    
    y_pred = classification_pipeline.predict(X_test)
    print(classification_report(y_test,y_pred,target_names=['legitime','phishing']))

    
    score = accuracy_score(y_test, y_pred)
    print("accuracy:   %0.3f" % score)
    r_score = recall_score(y_test, y_pred)
    print("recall:   %0.3f" % r_score)

if __name__ == '__main__':
    generate_prediction()