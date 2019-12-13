# import matplotlib.pyplot as plt
# from sklearn.metrics import roc_auc_score, roc_curve


def train_test_model(X_train, X_test, y_train, y_test, model):
    model_name = model.__class__.__name__
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    #
    # print('Accuracy of {} classifier on test set: {:.2f}'.format(model_name, model.score(X_test, y_test)))
    # roc_auc = roc_auc_score(y_test, y_pred)
    # fpr, tpr, thresholds = roc_curve(y_test, model.predict_proba(X_test)[:, 1])
    # plt.figure()
    # plt.plot(fpr, tpr, label=model_name + ' (area = %0.2f)' % roc_auc)
    # plt.plot([0, 1], [0, 1], 'r--')
    # plt.xlim([0.0, 1.0])
    # plt.ylim([0.0, 1.05])
    # plt.xlabel('False Positive Rate')
    # plt.ylabel('True Positive Rate')
    # plt.title('Receiver operating characteristic')
    # plt.legend(loc="lower right")
    # # plt.savefig('Log_ROC')
    # plt.show()
    #

