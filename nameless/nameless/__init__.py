import os
from flask import Flask, request, redirect, url_for, send_from_directory, Request
from werkzeug import secure_filename
from flask.ext.mongoengine import MongoEngine
from subprocess import call

UPLOAD_FOLDER = './resumeStorage'
ALLOWED_EXTENSIONS = set(['pdf','html','htm'])

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config["MONGODB_SETTINGS"] = {'DB': "resumeDB"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = MongoEngine(app)

if __name__ == '__main__':
    app.run()

def register_blueprints(app):
    # Prevents circular imports
    from nameless.views import resumes
    from nameless.admin import admin
    app.register_blueprint(resumes)
    app.register_blueprint(admin)

register_blueprints(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    from nameless.models import Resume
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            newResume = Resume()
            newResume.fileName = filename
            newResume.resumeSlug = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            newResume.namelessResumeSlug = os.path.join(app.config['UPLOAD_FOLDER'], 'nameless_'+filename)
            newResume.otherInfo = ""
            newResume.save()
            call(["./Scan1", newResume.fileName, "to", "Scan1"])
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/admin/resumeStorage/<filename>')
def previously_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
