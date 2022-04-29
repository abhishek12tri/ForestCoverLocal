from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.ensemble import RandomForestClassifier


class ModelFinder:
    """ Class Implements models per clusters """

    def __init__(self, file_obj, log_obj):
        self.forestClf = None
        self.fileObject = file_obj
        self.logger = log_obj
        self.rndmClassifier = RandomForestClassifier()

    def try_best_model(self, X_train, X_test, Y_train, Y_test):
        """ Finding model having the highest AUC score """
        self.logger.log(self.fileObject, 'Finding Best Model START')
        try:
            xg_boost = self.finding_XGBoost_best_params(X_train, Y_train)
            predict_xgboost = xg_boost.predict_proba(X_test)

            if len(Y_test.unique() == 1):
                xgboost_score = accuracy_score(Y_test, predict_xgboost)
                self.logger.log(self.fileObject, 'Accuracy of XGBoost: ' + str(xgboost_score))
            else:
                xgboost_score = roc_auc_score(Y_test, predict_xgboost)
                self.logger.log(self.fileObject, 'AUC for XGBoost ' + str(xgboost_score))

            random_forest = self.finding_RandomForest_best_params(X_train, Y_train)
            predict_rndmforest = random_forest.predict_proba(X_test)

            if len(Y_test.unique() == 1):
                rndmforest_score = accuracy_score(Y_test, predict_rndmforest)
                self.logger.log(self.fileObject, 'Accuracy Score Random Forest: ' + str(rndmforest_score))
            else:
                rndmforest_score = roc_auc_score(Y_test, predict_rndmforest)
                self.logger.log(self.fileObject, 'AUC for Random Forest: ' + str(rndmforest_score))

            """ Comparing and returning the better model for that cluster """
            if xgboost_score > rndmforest_score:
                return 'XGBoost', xg_boost
            else:
                return 'RandomForest', random_forest

        except Exception as bme:
            self.logger.log(self.fileObject, 'Error in Model Tuning ' + str(bme))
            raise bme

    def finding_XGBoost_best_params(self, X_train, Y_train):
        """ Getting Best Parameters for XGBoost """
        self.logger.log(self.fileObject, 'XGBoost Parameters START')
        print('XG')
        print(X_train.shape)
        print(Y_train.shape)

        try:
            grid_XGBoost = {
                'learning_rate': [0.5, 0.1, 0.01, 0.001],
                'max_depth': [3, 5, 10, 20],
                'n_estimators': [10, 50, 100, 200]
            }
            grid_XGB = GridSearchCV(XGBClassifier(objective='multi:softprob'), grid_XGBoost,
                                    verbose=3, cv=5, n_jobs=-1)
            grid_XGB.fit(X_train, Y_train)

            xg_learning = grid_XGB.best_params_['learning_rate']
            xg_max_depth = grid_XGB.best_params_['max_depth']
            xg_estimators = grid_XGB.best_params_['n_estimators']

            """ Creating Best params Model """
            xgb = XGBClassifier(
                learning_rate=xg_learning,
                max_depth=xg_max_depth,
                n_estimators=xg_estimators
            )
            xgb.fit(X_train, Y_train)
            self.logger.log(self.fileObject, 'XGBoost Parameters END')
            return xgb
        except Exception as XGe:
            self.logger.log(self.fileObject, 'Error in XGBoost Parameters: ' + str(XGe))
            raise XGe

    def finding_RandomForest_best_params(self, X_train, Y_train):
        """ Getting Best Parameters for Random Forest """
        self.logger.log(self.fileObject, 'Random Forest Parameters START')
        try:
            grid_random_forest = {
                'n_estimators': [10, 50, 100, 130],
                'criterion': ['gini', 'entropy'],
                'max_depth': range(2, 4, 1),
                'max_features': ['auto', 'log2']
            }

            rndmGrid = GridSearchCV(estimator=self.rndmClassifier, param_grid=grid_random_forest,
                                    cv=5, verbose=3, n_jobs=-1)
            rndmGrid.fit(X_train, Y_train)
            rndm_estimators = rndmGrid.best_params_['n_estimators']
            rndm_criterion = rndmGrid.best_params_['criterion']
            rndm_max_depth = rndmGrid.best_params_['max_depth']
            rndm_features = rndmGrid.best_params_['max_features']

            forestClf = RandomForestClassifier(n_estimators=rndm_estimators, criterion=rndm_criterion,
                                               max_depth=rndm_max_depth, max_features=rndm_features
                                               )
            forestClf.fit(X_train, Y_train)
            self.logger.log(self.fileObject, 'Random Forest Classifier END')
            return forestClf

        except Exception as ex:
            self.logger.log(self.fileObject, 'Random Forest Classifier Error: ' + ex)
            raise ex
