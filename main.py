from flask import Flask, request, Response, jsonify, render_template
from wsgiref import simple_server
import os
from flask_cors import CORS, cross_origin
import flask_monitoringdashboard as dashboard
from training_Validation_Insertion import train_validation
from trainingModel import trainModel

app = Flask(__name__)
dashboard.bind(app)
CORS(app)


@app.route('/', methods=['GET'])
@cross_origin()
def home_train_predict_form():
    return render_template('index.html')


@app.route('/train', methods=['POST'])
@cross_origin()
def clf_training_part():
    if request.method == 'POST':
        if request.form['btn-submit'] == 'Submit':
            try:
                if request.form['csv-folder-path'] is not None:
                    path = request.form['csv-folder-path']
                    # train_valobj = train_validation(path)
                    # """ Training Validation START """
                    # train_valobj.train_validation()

                    """ Training Model """
                    trainModelObj = trainModel()
                    trainModelObj.trainingModel()

            except ValueError:
                return Response('ValueError Occurred %s' % ValueError)
            except KeyError:
                return Response('KeyError Occurred %s' % KeyError)
            except Exception as e:
                return Response('Error Occurred %s' % e)
            return Response('Training Successful')
        return jsonify(request.form)


if __name__ == "__main__":
    host = '0.0.0.0'
    port = int(os.getenv('PORT', 5001))
    httpd = simple_server.make_server(host, port, app)
    httpd.serve_forever()
