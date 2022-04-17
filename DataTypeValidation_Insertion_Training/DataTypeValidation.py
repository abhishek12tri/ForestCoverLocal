from application_logging.logger import App_Logger


class dBOperation:
    """Handles all the DB Operations """

    def __init__(self):
        self.path = 'Training_Database/'
        self.badFilePath = 'Training_Raw_files_validated/Bad_Raw'
        self.goodFilePath = 'Training_Raw_files_validated/Good_Raw'
        self.logger = App_Logger()
