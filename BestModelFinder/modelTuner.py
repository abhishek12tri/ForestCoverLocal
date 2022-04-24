from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score


class ModelFinder:
    """ Class Implements models per clusters """
    def __init__(self, file_obj, log_obj):
        self.fileObject = file_obj
        self.logger = log_obj

    def try_best_model(self, X_train, Y_train, X_test, Y_test):
        """ Finding model having the highest AUC score """
        self.logger.log(self.fileObject, 'Finding Best Model START')
        try:
            xg_boost = self.finding_XGBoost_best_params(X_train, Y_train)
            predict_xgboost = xg_boost.predict(X_test)

            if len(Y_test.unique() == 1):
                xgboost_score = accuracy_score(Y_test, predict_xgboost)
                self.logger.log(self.fileObject, 'Accuracy of XGBoost: '+str(xgboost_score))
            else:
                


        except Exception as bme:
            raise bme


    def finding_XGBoost_best_params(self, X_train, Y_train):
        """ Getting Best Parameters for XGBoost """
        self.logger.log(self.fileObject, 'XGBoost Parameters START')
        try:
            grid_XGBoost = {
                'learning_rate' : [0.5, 0.1, 0.01, 0.001],
                'max_depth'     : [3, 5, 10, 20],
                'n_estimators'  : [10, 50, 100, 200]
            }
            grid_XGB = GridSearchCV( XGBClassifier(objective = 'multi:softprob'), grid_XGBoost,
                                     verbose=3, cv=5, n_jobs=-1)
            grid_XGB.fit(X_train, Y_train)

            xg_learning = grid_XGB.best_params_['learning_rate']
            xg_max_depth = grid_XGB.best_params_['max_depth']
            xg_estimators = grid_XGB.best_params_['n_estimators']

            """ Creating Best params Model """
            xgb = XGBClassifier(
                learning_rate = xg_learning,
                max_depth = xg_max_depth,
                n_estimators = xg_estimators
            )
            xgb.fit(X_train, Y_train)
            self.logger.log(self.fileObject, 'XGBoost Parameters END')
            return xgb
        except Exception as XGe:
            self.logger.log(self.fileObject, 'Error in XGBoost Parameters: '+str(XGe))
            raise XGe

    def finding_RandomForest_best_params(self):

