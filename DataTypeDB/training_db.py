"""
AUthor: Abhishek
Purpose: Handles type validation through DBOperations
"""
import shutil
import sqlite3
import os
import csv
from App_logging.logger import App_Logger
from log_files import logs_list

class DBOperation:
    def __init__(self) -> None:
        self.logs_list = logs_list()
        self.logger = App_Logger()
        self.raw_table = "Good_Raw_Data"
    
    def dbConnection(self, DBName, file_obj):
        """Description: Connect Database function."""
        try:
            conn = sqlite3.connect(os.path.join(self.logs_list["database"], DBName)+".db")
            return conn
        
        except Exception as e:
            self.logger.log(file_obj, "DBConnection error: %s"%e)
            raise e
        
    def createTable(self, DBName, column_names, file_obj):
        """Description: Creates table in DB, used to insert good data."""
        try:
            conn = self.dbConnection(DBName, file_obj)
            cursor = conn.cursor()

            cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Good_Raw_Data'")
            if cursor.fetchone()[0] == 1:
                conn.close()

                self.logger.log(file_obj, "Table already created in DB")
            else:
                for key in column_names.keys():
                    column_type = column_names[key]

                    try:
                        conn.execute(
                            'ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key, dataType=column_type)
                        )
                    except:
                        conn.execute(
                            'CREATE TABLE Good_Raw_Data ({column_name} {dataType})'.format(column_name=key, dataType=column_type)
                        )
                conn.close()

                self.logger.log(file_obj, "Table created successfully.")

        except Exception as e:
            conn.close()
            self.logger.log(file_obj, "Error in table creation: %s"%e)
            raise e

    def insert_into_table(self, DBName, file_obj):
        """Description: Insert good data into DB."""
        conn = self.dbConnection(DBName, file_obj)
        all_files = [f for f in os.listdir(self.logs_list["good_raw"])]
        
        count = 1
        for file in all_files:
            try:
                with open(os.path.join(self.logs_list["good_raw"], file), "r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter='\n')
                    for line in enumerate(reader):
                        for s_cl in (line[1]):
                            try:
                                conn.execute('INSERT INTO {good_table} values ({values})'.format(
                                    good_table=self.raw_table, values=s_cl))
                                
                                conn.commit()
                                print("row: " + str(count))
                                count += 1
                            except Exception as e:
                                raise e
                    self.logger.log(file_obj, "Data Inserted in DB.")
            
            except Exception as e:
                conn.rollback()
                self.logger.log(file_obj, "Data Insertion Error: %s".format(e))
                shutil.move(os.path.join(self.logs_list["good_raw"], file), self.logs_list["bad_raw"])
        conn.close()

    def selectingDataToCSV(self, DBName, file_obj):
        """Descrion: Exports DB data in CSV."""
        fileFromDb = self.logs_list["file_from_DB"]
        try:
            conn = self.dbConnection(DBName, file_obj)
            sql_qr = "Select * from " + self.raw_table + ";"
            cursor = conn.cursor()
            cursor.execute(sql_qr)
            results = cursor.fetchall()

            headers = [i[0] for i in cursor.description]
            if not os.path.isdir(fileFromDb):
                os.makedirs(fileFromDb)

            csvfile = csv.writer(open( os.path.join(fileFromDb, self.logs_list["inputfile"]), 'w', newline=''),
                                 delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_ALL, escapechar='\\')
            csvfile.writerow(headers)
            csvfile.writerows(results)

            self.logger.log(file_obj, 'File Successfully Exported.')
        except Exception as e:
            self.logger.log(file_obj, 'File Export Failed: %s' % e)
            raise e
