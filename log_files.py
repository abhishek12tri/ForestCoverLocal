"""
Author: Abhishek
Purpose: Stores all log_files, used in whole appkication
"""
import os

def logs_list():
    train_log = os.path.join("Training_Logs", "Training_Log.txt")
    model_train = os.path.join("Training_Logs", "Model_train_log.txt")
    raw_validated = "RawValidated"
    good_raw = os.path.join(raw_validated, 'good_data')
    bad_raw = os.path.join(raw_validated, 'bad_data')
    archive_bad = "TrainingArchiveBadData"
    database = "Database"
    file_from_DB = "TrainingFileFromDB"
    inputfile = "InputFile.csv"
    elbow_file = os.path.join("Training_Logs", "K-Means_Elbow.png")
    model_dir = "models/"
    kmeans_model = os.path.join(model_dir, 'KMeans')

    return {
        "train_log": train_log,
        "good_raw": good_raw,
        "bad_raw": bad_raw,
        "archive_bad": archive_bad,
        "database": database,
        "file_from_DB": file_from_DB,
        "inputfile": inputfile,
        "model_train": model_train,
        "elbow_file": elbow_file,
        "model_dir": model_dir,
        "kmeans_model": kmeans_model,
        "xgboost": "Xgboost",
        "rmmodel": "RandomForest"
    }