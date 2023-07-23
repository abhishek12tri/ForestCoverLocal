"""
Author: Abhishek
Purpose: Works as model finder, Find the model with best accuracy and AUC Score
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, accuracy_score
from App_logging.logger import App_Logger

class Model_Finder:
    def __init__(self) -> None:
        self.logger = App_Logger()
        self.clf = RandomForestClassifier()
        self.xgb = XGBClassifier(objective = 'binary:logistic')

    def best_param_model_for_xgboost(self, X_train, y_train, file_obj):
        """Description: Get the parameters for XGBoost, which gives best accuracy."""
        self.logger.log(file_obj, "Finding best params for XGBoost.")
        try:
            grid_xgboost = {
                'learning_rate': [0.5, 0.1, 0.01, 0.001],
                'max_depth': [3, 5, 10, 20],
                'n_estimators': [10, 50, 100, 200]
            }

            grid = GridSearchCV(
                XGBClassifier(objective='multi:softprob'), grid_xgboost, verbose = 1, cv=5, n_jobs=-1
            )

            grid.fit(X_train, y_train)

            learning_rate = grid.best_params_["learning_rate"]
            max_depth = grid.best_params_["max_depth"]
            n_estimators = grid.best_params_["n_estimators"]

            self.xgb = XGBClassifier(
                learning_rate = learning_rate, max_depth = max_depth, n_estimators = n_estimators
            )
            self.xgb.fit(X_train, y_train)
            self.logger.log(file_obj, "XGBoost Classifier parameters: lr="+str(learning_rate)+" max_depth="+str(max_depth)+" n_est="+str(n_estimators))
            return self.xgb
        except Exception as e:
            self.logger.log(file_obj, "Error in XGBoost: "+str(e))

    def best_param_model_for_randomforest(self, X_train, y_train, file_obj):
        """Description: Get the parameters for Random Forest, which gives best accuracy."""
        self.logger.log(file_obj, "Finding best params for random forest.")
        try:
            grid_foreest = {
                "max_depth": range(2, 6),
                "n_estimators": [10, 50, 100, 125],
                "criterion": ["gini", "entropy"],
                "max_features": ['auto', "log2"]
            }

            grid = GridSearchCV(
                self.clf, param_grid=grid_foreest, cv=5, verbose=1, n_jobs=-1
            )
            grid.fit(X_train, y_train)

            max_depth = grid.best_params_["max_depth"]
            n_estimators = grid.best_params_["n_estimators"]
            criterion = grid.best_params_["criterion"]
            max_features = grid.best_params_["max_features"]

            self.clf = RandomForestClassifier(
                n_estimators=n_estimators, criterion=criterion, max_depth=max_depth, max_features=max_features
            )

            self.clf.fit(X_train, y_train)
            self.logger.log(file_obj, "Rndm Forest Classifier parameters:  max_depth="+str(max_depth)+" n_est="+str(n_estimators)+" criterion="+str(criterion)+" max_feature="+str(max_features))
            return self.clf
        except Exception as e:
            self.logger.log(file_obj, "Error in Random forest: "+str(e))


    def get_best_model(self, X_train, y_train, X_test, y_test, file_obj):
        """Description: Finding the model having highest AUC Score."""
        self.logger.log(file_obj, "Start find best model.")

        try:
            # Best Model for XGBoost
            xgboost = self.best_param_model_for_xgboost(X_train, y_train, file_obj)
            pred_xgboost = xgboost.predict_proba(X_test)

            if len(y_test.unique()) == 1:
                xgboost_score = accuracy_score(y_test, pred_xgboost)
                self.logger.log(file_obj, "Accuracy for XGBoost: "+str(xgboost_score))
            else:
                xgboost_score = roc_auc_score(y_test, pred_xgboost, multi_class='ovr')
                self.logger.log(file_obj, "AUC for XGBoost: "+str(xgboost_score))

            # Best Model for Random Forest
            random_forest = self.best_param_model_for_randomforest(X_train, y_train, file_obj)
            pred_forest = random_forest.predict_proba(X_test)

            if len(y_test.unique()) == 1:
                rf_clf_score = accuracy_score(y_test, pred_forest)
                self.logger.log(file_obj, "Accuracy for RF: "+str(rf_clf_score))
            else:
                rf_clf_score = roc_auc_score(y_test, pred_forest, multi_class='ovr')
                self.logger.log(file_obj, "AUC for RF: "+str(rf_clf_score))

            # Model Comparison
            if xgboost_score > rf_clf_score:
                return {"name":"XGBoost", "model": xgboost}
            else:
                return {"name":"Random Forest","model": random_forest}
        except Exception as e:
            self.logger.log(file_obj, "Error in finding best model")
            self.logger.log(file_obj, str(e))
