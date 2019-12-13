from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier

from src.modeling.model_port import train_test_model
from src.modeling.models.LogisticRegression import LogisticRegressionAdapter
from src.preparation.activities import ColumnType
from src.preparation.group_data import group_data

user_id = 3
X, y = group_data(user_id)

lr = LogisticRegressionAdapter(X)

models = [
    lr.model,
    GaussianNB(),
    KNeighborsClassifier(n_neighbors=3),
    MLPClassifier(hidden_layer_sizes=(4, 10, 10), max_iter=10000),
    DecisionTreeClassifier(),
]


X_train, X_test, y_train, y_test = train_test_split(X, y.values.ravel(), test_size=0.4, random_state=0)

print(y_test)
for model in models:
    train_test_model(X_train, X_test, y_train, y_test, model)



lr.assign_coef_features()
print(lr.get_best_features())
print(lr.get_worst_features(filter_by=ColumnType.app_type.name))

