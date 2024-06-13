import pathlib
import os
import prediction_model

PACKAGE_ROOT = pathlib.Path(prediction_model.__file__).resolve().parent

DATAPATH = os.path.join(PACKAGE_ROOT,"datasets")
TEST_DATAPATH = os.path.join(PACKAGE_ROOT,"testdata")

TEST_FILE = 'test.csv'
DATA_FILE = 'dataset.csv'


MODEL_NAME = 'phishing_url_prediction.pkl'
SAVE_MODEL_PATH = os.path.join(PACKAGE_ROOT,'trained_models')

TARGET = 'label'
X = 'domain'

CLASS_NAMES = ['Legitime','Phishing']


FEATURES = ['nbr_https', 'nbr_http', 'nbr_doubleSlash',
       'nbr_www', 'nbr_slash', 'nbr_@', 'nbr_-', 'nbr_?', 'nbr_%', 'nbr_=',
       'nbr_.', 'length', 'phishing_words',
       'cont_digit', 'length_domain', 'short_url', 'bad_url', 'nbr_spe_c',
       'hexa', 'nbr_param']


N_ESTIMATORS = 100

MAX_FEATURES = "sqrt"

BOOSTER='dart'

TEST_SIZE = 0.2