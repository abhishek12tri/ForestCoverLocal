import os
import sqlite3
import csv
import shutil
from application_logging.logger import App_Logger


class dBOperation:
    """Handles all the DB Operations """

    def __init__(self):
        self.fileName = None
        self.fileFromDb = None
        self.path = 'Training_Database/'
        self.badFilePath = 'Training_Raw_files_validated/Bad_Raw/'
        self.goodFilePath = 'Training_Raw_files_validated/Good_Raw/'
        self.raw_table = 'Good_Raw_Data'
        self.logger = App_Logger()

    def dataBaseConnection(self, db_name):
        """ Connects with the DB """
        try:
            conn = sqlite3.connect(self.path + db_name + '.db')
            file = open('Training_Logs/DataBaseConnectionLog.txt', 'a+')
            self.logger.log(file, 'Training DB %s connected' % db_name)
            file.close()
        except ConnectionError:
            file = open('Training_Logs/DataBaseConnectionLog.txt', 'a+')
            self.logger.log(file, 'DB Connection %s failed' % db_name)
            file.close()
            raise ConnectionError
        return conn

    def createTableDB(self, dbname, column_names):
        """ Create DB Tables """
        try:
            conn = self.dataBaseConnection(dbname)
            c = conn.cursor()
            c.execute("SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'Good_Raw_Data'")
            if c.fetchone()[0] == 1:
                conn.close()
                file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
                self.logger.log(file, "Tables created successfully!!")
                self.logger.log(file, "Closed %s database successfully" % dbname)
                file.close()

            else:
                for key in column_names.keys():
                    type = column_names[key]

                    try:
                        conn.execute(
                            'ALTER table Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,
                                                                                                     dataType=type))
                    except:
                        conn.execute('CREATE TABLE Good_Raw_Data ({column_name} {dataType})'.format(column_name=key,
                                                                                                    dataType=type))
                conn.close()

                file = open('Training_Logs/DataBaseConnectionLog.txt', 'a+')
                self.logger.log(file, 'Training DB Created.')
                self.logger.log(file, 'DB Closed.')
                file.close()

        except Exception as e:
            file = open('Training_Logs/DataBaseConnectionLog.txt', 'a+')
            self.logger.log(file, 'Error while creating Training DB: %s.' % e)
            raise e

    def insertionIntoGoodDB(self, trainingDB):
        """ Method Used to Good Data insertion operation to the DB """
        conn = self.dataBaseConnection(trainingDB)
        all_files = [f for f in os.listdir(self.goodFilePath)]
        logfile = open('Training_Logs/DataBaseConnectionLog.txt', 'a+')
        count = 1
        for file in all_files:
            try:
                with open(self.goodFilePath + file, 'r') as f:
                    next(f)
                    reader = csv.reader(f, delimiter='\n')
                    for line in enumerate(reader):
                        for s_cl in (line[1]):
                            try:
                                conn.execute('INSERT INTO {good_table} values ({values})'.format(
                                    good_table=self.raw_table, values=s_cl))
                                self.logger.log(logfile, "%s: Loaded Successfully" % file)
                                conn.commit()
                                print("row: " + str(count))
                                count += 1
                            except Exception as e:
                                raise e
            except Exception as er:
                conn.rollback()
                self.logger.log(logfile, 'Error in Insertion: %s' % er)
                shutil.move(self.goodFilePath + file, self.badFilePath)
                self.logger.log(logfile, 'Bad files Moved: %s' % er)
                logfile.close()
                conn.close()
                raise er
        conn.close()
        logfile.close()

    def selectdatafromtableintoCSV(self, trainingDB):
        """ Export table data into CSV """
        self.fileFromDb = 'Training_FileFromDB/'
        self.fileName = 'InputFile.csv'
        logfile = open("Training_Logs/ExportToCsv.txt", 'a+')
        try:
            conn = self.dataBaseConnection(trainingDB)
            sql_qr = "Select * from " + self.raw_table + ";"
            cursor = conn.cursor()
            cursor.execute(sql_qr)
            results = cursor.fetchall()

            headers = [i[0] for i in cursor.description]
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            csvfile = csv.writer(open(self.fileFromDb + self.fileName, 'w', newline=''),
                                 delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_ALL, escapechar='\\')
            csvfile.writerow(headers)
            csvfile.writerows(results)

            self.logger.log(logfile, 'File Successfully Exported.')
            logfile.close()
        except Exception as e:
            self.logger.log(logfile, 'File Export Failed: %s' % e)
            logfile.close()
            raise e
