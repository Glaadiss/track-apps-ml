from _operator import itemgetter

import pandas as pd
from sklearn.linear_model import LogisticRegression


class LogisticRegressionAdapter:
    def __init__(self, df: pd.DataFrame):
        self.features = list(df)
        self.coef_features = []
        self.model = LogisticRegression()

    def get_top_features(self, n, reverse=False, filter_by=None):
        features = self.coef_features
        if filter_by is not None:
            features = filter(lambda x: x[0].startswith(filter_by), features)

        features = sorted(features, key=itemgetter(1), reverse=reverse)[:n]
        return [feature_score[0] for feature_score in features]

    def get_best_features(self, n=5, filter_by=None):
        return self.get_top_features(n, reverse=True, filter_by=filter_by)

    def get_worst_features(self, n=5, filter_by=None):
        return self.get_top_features(n, filter_by=filter_by)

    def assign_coef_features(self):
        coefs = self.model.coef_[0]
        coef_dict = {}
        for coef, feat in zip(coefs, self.features):
            coef_dict[feat] = coef
        self.coef_features = coef_dict.items()
