"""
Author: Abhishek
Version: 1.0
Purpose: Handles all the functionality realed to training
"""
from trainingValidation import trainValidation
from trainingModel import trainModel
import os


if __name__ == "__main__":
    raw_path = "rawdata"

    """Prepare data for training"""
    # validate_obj = trainValidation(raw_path)
    # validate_obj.train_validate()

    """Training Model"""
    train_obj = trainModel()
    train_obj.training_model()