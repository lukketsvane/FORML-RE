import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge


def predict(features, y_train):
    # Hypothesis (round 1): catalogue geometry depends on period non-linearly
    # and through period x material/technique interactions, which a purely
    # additive linear ridge cannot represent. Average the reference ridge with
    # a heavily smoothed random forest (large leaves) on the same four frozen
    # feature matrices, so the linear signal is kept and only coarse
    # non-linear structure is added.
    names = ("year", "technique", "origin", "materials")
    train = np.column_stack([features[name][0] for name in names])
    test = np.column_stack([features[name][1] for name in names])
    linear = Ridge(alpha=20.0).fit(train, y_train).predict(test)
    forest = RandomForestRegressor(
        n_estimators=500,
        min_samples_leaf=10,
        max_features=0.5,
        random_state=0,
    ).fit(train, y_train).predict(test)
    return 0.5 * linear + 0.5 * forest
