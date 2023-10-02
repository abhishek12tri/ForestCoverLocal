"""
AUthor: Abhishek
Purpose: Data base related operation for prediction
"""
import shutil
import os
import csv
import sqlite3
from App_logging.logger import App_Logger
from log_files import logs_list


class dBOperation:
    def __init__(self) -> None:
        self.log_list = logs_list()
        self.logger = App_Logger()
        self.dbname = "prediction.db"

    def database_connection(self, file_obj):
        """
        Description: Created the DB or connect if alredy exists
        """
        try:
            conn = sqlite3.connect(os.path.join(self.log_list["database"], self.dbname))
            self.logger.log(file_obj, "DB Connected.")
            return conn
        except Exception as e:
            self.logger.log(file_obj, "DB not Connected.")
            raise e
        
    def createTable(self, column_names, file_obj):
        """
        Description: Creates a table in the gived DB.
        """
        try:
            conn = self.database_connection(file_obj)
            conn.execute('DROP TABLE IF EXISTS Pred_data;')

            for key in column_names.keys():
                type = column_names[key]

                try:
                    conn.execute('ALTER TABLE Pred_data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key, dataType=type))
                except:
                    conn.execute('CREATE TABLE Pred_data ({column_name} {dataType})'.format(column_name=key, dataType=type))
            conn.close()

            self.logger.log(file_obj, "Table Created.")
        except Exception as e:
            self.logger.log(file_obj, "Error in table creation: "+ str(e))
            raise e
        
    def insertIntoTable(self, path, file_obj):
        """
        Description: Insert data into the table.
        """
        try:
            conn = self.database_connection(file_obj)
            files = [f for f in os.listdir(path)]
            for each_file in files:
                with open(os.path.join(path, each_file)) as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line_data in enumerate(reader):
                        for list_line in line_data[1]:
                            conn.execute('Insert INTO Pred_data values ({values})'.format(values=(list_line)))
                            conn.commit()
            
            conn.close()
            self.logger.log(file_obj, "Data Inserted into table.")

        except Exception as e:
            conn.rollback()
            self.logger.log(file_obj, "Error in insertIntoTable: "+ str(e))
            raise e
        
    def dataFromTableIntoCSV(self, path, file_obj):
        """
        Description: Save DB data into a prediction CSV file
        """
        try:
            conn = self.database_connection(file_obj)
            sql_data = "SELECT * FROM Pred_data"
            cursor = conn.cursor()
            cursor.execute(sql_data)
            results = cursor.fetchall()

            headers = [desc[0] for desc in cursor.description]

            csv_file = csv.writer(
                open(os.path.join(path, self.log_list["input_file"]), "w", newline=""),
                delimiter=",", lineterminator='\r\n', quoting=csv.QUOTE_ALL, escapechar='\\'
            )
            csv_file.writerow(headers)
            csv_file.writerows(results)
            self.logger.log(file_obj, "File exported from DB.")
        except Exception as e:
            self.logger.log(file_obj, "Error in file exporting: "+str(e))
            raise e