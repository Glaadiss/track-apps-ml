from sklearn.model_selection import train_test_split

from src.modeling.model_port import train_test_model
from src.modeling.models.LogisticRegression import LogisticRegressionAdapter
from src.preparation.activities import ColumnType
from src.preparation.group_data import group_data


def get_report(user_id):
    X, y = group_data(user_id)

    lr = LogisticRegressionAdapter(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y.values.ravel(), test_size=0.4, random_state=0)
    train_test_model(X_train, X_test, y_train, y_test, lr.model)
    lr.assign_coef_features()

    report = {
        "bestApps": lr.get_best_features(n=3, filter_by=ColumnType.app_name.name),
        "worstApps": lr.get_worst_features(n=3, filter_by=ColumnType.app_name.name),

        "bestType": lr.get_best_features(n=1, filter_by=ColumnType.app_type.name)[0],
        "worstType": lr.get_worst_features(n=1, filter_by=ColumnType.app_type.name)[0],

        "bestDayPart": lr.get_best_features(n=1, filter_by=ColumnType.day_part.name)[0],
        "worstDayPart": lr.get_worst_features(n=1, filter_by=ColumnType.day_part.name)[0],
    }

    return report



