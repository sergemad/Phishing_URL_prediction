from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold

import os
from pathlib import Path
import sys

PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))

from prediction_model.config import config



base_models = [
    ('rf', RandomForestClassifier(n_estimators=config.N_ESTIMATORS,max_features=config.MAX_FEATURES)),
    ('xgb', XGBClassifier(n_estimators=config.N_ESTIMATORS,booster=config.BOOSTER))
]

meta_model = LogisticRegression()

stacking_clf = StackingClassifier(estimators=base_models, final_estimator=meta_model, cv=KFold(n_splits=2))