from sklearn.pipeline import Pipeline

import os
from pathlib import Path
import sys

PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))

from prediction_model.config import config
import prediction_model.processing.preprocessing as pp
from prediction_model.model import stacking_clf

classification_pipeline = Pipeline(
    [
        ('FeaturesEngineering', pp.FeaturesEngineering(variables=config.FEATURES, label=config.TARGET)),
        ('StackingModel', stacking_clf)
    ]
)
