"""
Author: Abhishek
Purpose: Stores all log_files, used in whole appkication
"""
import os

def logs_list():
    train_log = os.path.join("Training_Logs", "Training_Log.txt")
    raw_validated = "RawValidated"
    good_raw = os.path.join(raw_validated, 'good_data')
    bad_raw = os.path.join(raw_validated, 'bad_data')
    archive_bad = "TrainingArchiveBadData"
    database = "Database"

    return {
        "train_log": train_log,
        "good_raw": good_raw,
        "bad_raw": bad_raw,
        "archive_bad": archive_bad,
        "database": database,
    }