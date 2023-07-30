"""
Author: Abhishek
Purpose: App entry point
"""
import os
from wsgiref import simple_server
from flask import Flask, request, render_template, Response
from flask_cors import CORS, cross_origin
from PredictionValidate.predictValidation import PredictionValidation
from prediction import Predict


os.putenv("LANG", "en_US.UTF-8")
os.putenv("LC_ALL", "en_US.UTF-8")

app = Flask(__name__)
CORS(app)
app.config.update(
    TEMPLATES_AUTO_RELOAD=True
)


@app.route("/", methods=["GET"])
@cross_origin()
def home_page():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
@cross_origin()
def predictRouteClient():
    try:
        if request.form is not None:
            path = request.form["file_path"]
            #pred_val = PredictionValidation(path)
            #pred_val.prediction_validation()

            predict = Predict(path)
            pred_path = predict.predict_data()
        
            return Response("Predicted file path %s"%pred_path)
        else:
            return Response("Error Occurred in getting request data.")
    except Exception as e:
        return Response("Error Occurred %s" %e)




port = int(os.getenv("PORT", 5001))
if __name__ == "__main__":
    host = "0.0.0.0"
    serve = simple_server.make_server(host, port, app)
    serve.serve_forever()