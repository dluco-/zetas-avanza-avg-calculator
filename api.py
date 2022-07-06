import os

from flask import Flask, flash, redirect, request, send_from_directory
from werkzeug.utils import secure_filename

from calculate import main as do_calculation

UPLOAD_FOLDER = f"{os.getcwd()}/uploads"
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET'])
def index():
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action=/upload method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
        </form>
        '''


@app.route('/calculate', methods=['POST'])
def calculate():
    filename = request.form['filename']
    return do_calculation(os.path.join(
        app.config['UPLOAD_FOLDER'], filename))


@app.route("/upload", methods=["POST"])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return "No file part", 400
        # return redirect(request.url)

    file = request.files['file']

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return "No selected file", 400
        # return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully', 200
        # return redirect(url_for('uploaded_file', filename=filename))

    return "File not allowed", 400
