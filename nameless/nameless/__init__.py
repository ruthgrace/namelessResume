import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from flask.ext.mongoengine import MongoEngine

UPLOAD_FOLDER = '/resumeStorage'
ALLOWED_EXTENSIONS = set(['pdf','html'])

app = Flask(__name__)
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
