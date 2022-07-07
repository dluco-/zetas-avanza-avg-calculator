import os

from flask import Flask, flash, request, send_from_directory
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


@app.route("/", methods=["GET", "POST"])
def main():

    if request.method == 'GET':
        fileName = request.args.get("fileName")

        if not fileName:
            return "No file name provided", 400

        if not allowed_file(fileName):
            return "File type not allowed", 400

        return do_calculation(os.path.join(
            app.config['UPLOAD_FOLDER'], fileName))

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

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return do_calculation(os.path.join(
            app.config['UPLOAD_FOLDER'], filename))

    return "File not allowed", 400
