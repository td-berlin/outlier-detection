from flask import Flask, render_template, request, jsonify, make_response, redirect
import json
from controllers import outlier_detection
from controllers import holt_winter

import numpy as np
from flask_cors import CORS
from flask_mail import Mail, Message


ALLOWED_EXTENSIONS = set(['xlsx'])
MAX_FILE_SIZE = 0.5 * 1024 * 1024


app = Flask(__name__)
CORS(app)
app.config["UPLOADS"] = "./files"
app.env = "development"
mail = Mail(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file_size(fileSize):
    if int(fileSize) <= app.config["MAX_FILE_SIZE"]:
        return True
    else:
        return False


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()


@app.route('/', methods=['GET'])
def hello():
    return jsonify('hello')


@app.route('/upload-file', methods=['POST'])
def uploadFile():
    try:
        if request.method == 'POST':
            if request.files:
                file = request.files['file']
                if file.filename == '':
                    data = {'message': 'Fail', 'code': 'SUCCESS'}
                if not allowed_file(file.filename):
                    data = {'message': 'Fail', 'code': 'SUCCESS'}
                else:
                    outlier_detection.addFile(file)
                    dataWithOutlier = outlier_detection.calculateOutlier()

            data = {'message': 'Done', 'code': 'SUCCESS',  'dataWithOutlier':  json.loads(json.dumps(dataWithOutlier, default=np_encoder))}
            return make_response(jsonify(data), 201)
    except Exception as e: 
        print(e) 
        data = {'message': 'Failed', 'code': 'INTERNAL SERVER ERROR'}
        return make_response(jsonify(data), 500)
        #return render_template("show_file.html")  #we can use this line instead of redirect(url_for('showFile')


@app.route('/show_graph', methods=['GET', 'POST'])
def showGraph():
    try:
        if request.method == "GET":
            rowId = request.args
            actualDataToPlot = outlier_detection.getDataById(rowId)
            EstimatedToPlot = outlier_detection.getRowToPlot(rowId)
            data = {'message': 'Done', 'code': 'SUCCESS',
                    'outlier': json.loads(json.dumps(EstimatedToPlot["outlierValue"], default=np_encoder)),
                    'outlierIndex': json.loads(json.dumps(EstimatedToPlot["outlierIndex"], default=np_encoder)),
                    'dataWithValue': json.loads(json.dumps(actualDataToPlot, default=np_encoder)),
                    'upperThreshold': json.loads(json.dumps(EstimatedToPlot["upper_bound"], default=np_encoder)),
                    'lowerThreshold': json.loads(json.dumps(EstimatedToPlot["lower_bound"], default=np_encoder))
                    #'dataWithEstimate': json.loads(json.dumps(EstimatedToPlot["estimatedValue"], default=np_encoder))
                    }
            return make_response(jsonify(data), 201)
    except Exception as e:
        print(e)
        data = {'message': 'Failed', 'code': 'INTERNAL SERVER ERROR'}
        return make_response(jsonify(data), 500)


#@app.route('/show_graph', methods=['GET', 'POST'])
#def showGraph():
#    try:
#       if request.method == "GET":
#            rowId = request.args
#            actualDataToPlot = outlier_detection.getDataById(rowId)
#            EstimatedToPlot = outlier_detection.getRowToPlot(rowId)
#            data = {'message': 'Done', 'code': 'SUCCESS',
#                    'outlier': json.loads(json.dumps(EstimatedToPlot["outlierValue"], default=np_encoder)),
#                    'outlierIndex': json.loads(json.dumps(EstimatedToPlot["outlierIndex"], default=np_encoder)),
#                    'dataWithValue': json.loads(json.dumps(actualDataToPlot, default=np_encoder)),
#                    'upperThreshold': json.loads(json.dumps(EstimatedToPlot["upper_bound"], default=np_encoder)),
#                    'lowerThreshold': json.loads(json.dumps(EstimatedToPlot["lower_bound"], default=np_encoder))
#                    #'dataWithEstimate': json.loads(json.dumps(EstimatedToPlot["estimatedValue"], default=np_encoder))
#                    }
#            return make_response(jsonify(data), 201)
#    except Exception as e:
#        print(e)
#        data = {'message': 'Failed', 'code': 'INTERNAL SERVER ERROR'}
#        return make_response(jsonify(data), 500)


@app.route("/send_mail")
def index():
    msg = Message(
        'Hello',
        sender='MAIL_USERNAME',
        recipients=['acharyasulochana21@gmail.com']
    )
    msg.body = 'Hello Flask message sent from Flask-Mail'
    mail.send(msg)
    return 'Sent'


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['JSON_SORT_KEYS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)

