"""
Author: Abhishek
Purpose: Handles model operations like save and load model
"""
import pickle
import os
import json
from App_logging.logger import App_Logger
from log_files import logs_list

class FileOperation:
    def __init__(self) -> None:
        self.logger = App_Logger()
        self.files_list = logs_list()

    def save_label_data(self, data_dict):
        """Description: Saves the label data."""
        label_file = self.files_list["label_json"]
        with open(label_file, "w") as f:
            f.write(json.dumps(data_dict))

    def load_label_data(self, file_obj):
        """Description: Saves the label data."""
        try:
            label_file = self.files_list["label_json"]
            with open(label_file, "r") as f:
                labels = json.loads(f.read())
            return labels
        except Exception as e:
            self.logger.log(file_obj, "error in loading label data")

    def save_model(self, model, filepath, file_obj):
        """Description: Saves the model."""
        try:
            # if os.path.isdir(self.files_list["model_dir"]):
            #     shutil.rmtree(self.files_list["model_dir"])
            if not os.path.isdir(self.files_list["model_dir"]):
                os.makedirs(self.files_list["model_dir"])

            with open(filepath+".sav", "wb") as f:
                pickle.dump(model, f)

            self.logger.log(file_obj, "Model file saved at "+filepath)


        except Exception as e:
            self.logger.log(file_obj, "Error in saving ", e)
            raise e
        
    def load_model(self, filepath, file_obj):
        """Description: Load saved model from filepath."""
        try:
            with open(filepath, 'rb') as f:
                model_file = pickle.load(f)
            self.logger.log(file_obj, "Loaded model: "+filepath)
            return model_file

        except Exception as e:
            self.logger.log(file_obj, "Error in load_model: "+str(e))
            raise e
        
    def find_correct_model(self, cluster_number, file_obj):
        try:
            model_file = ""
            saved_files = os.listdir(self.files_list["model_dir"])
            for each_file in saved_files:
                splitted = os.path.splitext(each_file)
                name_split = splitted[0].split("_")
                try:
                    if int(name_split[-1])==cluster_number:
                        model_file = os.path.join(self.files_list["model_dir"], each_file)
                        break
                except Exception as e:
                    self.logger.log(file_obj, "Filename arrangement error: "+str(e))
                    pass

            if model_file == "":
                self.logger.log(file_obj, "Did not find the model.")
                return None
            else:
                return model_file
        except Exception as e:
            self.logger.log(file_obj, "Error in finding model.")
            raise e
