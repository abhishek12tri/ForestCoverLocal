# ForestCoverLocal
Project decription and data provided by iNeuron, I have completed it using various python and machine learning libraries.

## Files
ForestCoverLocal/         (Root dir)
├─TrainingFileFromDB/     (Single CSV file ready to train)
│ └─InputFile.csv
├─PredictFiles/           (All files which will be used for prediction)
│ ├─PredictInput.csv
│ ├─Predictions.csv
│ └─forest_cover_28011992_120212.csv
├─DataPreprocessing/      (Files related to data processing- CLustering and preprocessing)
│ ├─clustering.py
│ ├─__pycache__/
│ │ ├─clustering.cpython-310.pyc
│ │ └─preprocessing.cpython-310.pyc
│ └─preprocessing.py
├─details                  (Basic development details)
├─DataTypeDB/              (Handles type validation through DBOperations)
│ ├─__pycache__/
│ │ └─training_db.cpython-310.pyc
│ └─training_db.py
├─Operational/             (Covers operations related to model save, load and finding best model for the data group)
│ ├─model_opeartion.py
│ ├─tuner.py
│ └─__pycache__/
│   ├─tuner.cpython-310.pyc
│   └─model_opeartion.cpython-310.pyc
├─training.py              (Data training handler)
├─DataTransformation/      (Transform the data brfore traing and prediction)
│ ├─__pycache__/
│ │ └─train_transform.cpython-310.pyc
│ └─train_transform.py
├─PredictionValidate/      (All files related to prediction)
│ ├─predInsertion.py
│ ├─rawValidation.py
│ ├─__pycache__/
│ │ ├─predictValidation.cpython-310.pyc
│ │ ├─predInsertion.cpython-310.pyc
│ │ └─rawValidation.cpython-310.pyc
│ └─predictValidation.py
├─trainingValidation.py    (Validated the training data)
├─Training_Logs/           (Has all the training logs)
│ ├─K-Means_Elbow.png
│ ├─Training_Log.txt
│ └─Model_train_log.txt
├─App_logging/             (Logger file for logging the events)
│ ├─logger.py
│ └─__pycache__/
│   └─logger.cpython-310.pyc
├─TrainingArchiveBadData/  (Data failed in validation)
│ └─BadData_2023-07-01_095117/
│   └─forest_cover_28011999_120259.csv
├─README.md
├─RawValidation/           (Used to validate the raw data)
│ ├─validation.py
│ └─__pycache__/
│   └─validation.cpython-310.pyc
├─PredictionLogs/          (Has all the prediction logs)
│ ├─PredValidation.txt
│ └─Prediction.txt
├─templates/               (HTML template)
│ └─index.html
├─main.py                  (App entrypoint)
├─rawdata/                 (All raw data files)
│ ├─forest_cover_28011991_120211.csv
│ ├─forest_cover_28011997_120217.csv
│ ├─forest_cover_28011999_120259.csv
│ ├─forest_cover_28011993_120213.csv
│ ├─forest_cover_28011995_120215.csv
│ ├─forest_cover_28011994_120214.csv
│ ├─forest_cover_28011999_120219.csv
│ ├─forest_cover_28012000_120220.csv
│ ├─forest_cover_28011998_120218.csv
│ ├─forest_cover_28011992_120212.csv
│ └─forest_cover_28011996_120216.csv
├─trainingModel.py          (Training the model file)
├─schema_prediction.json    (Prediction file schema)
├─log_files.py              (All constants, to direct the app and follow the same structure)
├─prediction.py             (Handle prediction)
├─Database/                 (Training and prediction DB- Data Ingestion)
│ ├─prediction.db
│ └─Training.db
├─schema_training.json      (Training file schema)
├─DataIngestion/            (Data Ingestion part)
│ ├─ingestion_operation.py
│ └─__pycache__/
│   └─ingestion_operation.cpython-310.pyc
└─models/                   (Saves all the models related to the project)
  ├─KMeans.sav
  ├─XGBoost_2.sav
  ├─XGBoost_0.sav
  ├─labels.json
  └─XGBoost_1.sav

## Training
