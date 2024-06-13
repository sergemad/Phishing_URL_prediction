import pandas as pd
import numpy as np

import os
from pathlib import Path
import sys

PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))

from prediction_model.config import config
from prediction_model.processing.data_handling import load_dataset,save_pipeline,save_test_dataset
import prediction_model.pipeline as pipe
from sklearn.model_selection import train_test_split

def perform_training():
    X, y = load_dataset(config.DATA_FILE)
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, stratify=y, test_size=config.TEST_SIZE)
    pipe.classification_pipeline.fit(X_train, y_train)
    save_pipeline(pipe.classification_pipeline)
    save_test_dataset(X_test,y_test)

if __name__ == '__main__':
    perform_training()