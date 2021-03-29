import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from controllers.comprehend import Comprehend 
from db.sqlite import ConMan
from controllers.conlist import GetConList
from waitress import serve

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

with ConMan() as con:
    con._create_tables();
if not os.path.exists('temp'):
    os.makedirs('temp')
    
def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)

@app.route('/', methods=['POST'])
def upload_files():
    try:
        uploaded_file = request.files['file']
        password = request.form['password']
        print(password)
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            # file_ext = os.path.splitext(filename)[1]
            # if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
            #         file_ext != validate_image(uploaded_file.stream):
            #     return "Invalid image", 400
            pdfFileName = os.path.join(app.config['UPLOAD_PATH'], filename)
        uploaded_file.save(pdfFileName)

        with Comprehend() as comprehend:
            uuid = comprehend.Start(filename=pdfFileName, password=password, decrypt=True)
            resultList = GetConList(uuid)
            # return jsonify(resultList)
            return render_template('result.html', rows=resultList)
    except Exception as e:
        return str(e)

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/conlist/<uuid>')
def getConList(uuid):
    resultList = GetConList(uuid)
    for r in resultList:
        print(r[0])
    print(resultList)
    return render_template('result.html', rows=resultList)

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    #We now use this syntax to server our app. 
    serve(app, host='0.0.0.0', port=8080)