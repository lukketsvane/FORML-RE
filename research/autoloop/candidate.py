import numpy as np
from sklearn.linear_model import Ridge


def predict(features, y_train):
    names = ("year", "technique", "origin", "materials")
    train = np.column_stack([features[name][0] for name in names])
    test = np.column_stack([features[name][1] for name in names])
    return Ridge(alpha=20.0).fit(train, y_train).predict(test)
