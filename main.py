"""
Author: Abhishek
Purpose: App entry point
"""
import os
from wsgiref import simple_server
from flask import Flask, request, render_template, Res
from flask_cors import CORS, cross_origin
from trainingValidation import trainValidation


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




port = int(os.getenv("PORT", 5001))
if __name__ == "__main__":
    host = "0.0.0.0"
    serve = simple_server.make_server(host, port, app)
    serve.serve_forever()