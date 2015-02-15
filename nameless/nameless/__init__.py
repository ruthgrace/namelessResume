import os
from flask import Flask, request, redirect, url_for, send_from_directory, Request
from werkzeug import secure_filename
from flask.ext.mongoengine import MongoEngine

UPLOAD_FOLDER = './resumeStorage'
ALLOWED_EXTENSIONS = set(['pdf','html'])

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
            newResume.namelessResumeSlug = os.path.join(app.config['UPLOAD_FOLDER'], 'nameless_'.join(filename))
            newResume.otherInfo = ""
            # setattr(newResume,fileName,filename)
            # setattr(newResume,resumeSlug,os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # setattr(newResume,namelessResumeSlug,os.path.join(app.config['UPLOAD_FOLDER'], 'nameless_'.join(filename)))
            # setattr(newResume,otherInfo,"")
            newResume.save()
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



    # def get_context(self,resumeSlug):
    #     resume=Resume.objects.get_or_404(resumeSlug=resumeSlug)
    #     form = self.form(request.form)

    #     context = {
    #             "resume": resume,
    #             "form": form
    #     }
    #     return context

	# def get(self, resumeSlug):
	#     resume = Resume.objects.get_or_404(resumeSlug=resumeSlug)
	#     return render_template('resume/resumeDetail.html', **context)


	# def post(self,resumeSlug):
	#     context=self.get_context(resumeSlug)
	#     form = content.get('form')
	#     if form.validate():
	#         resume = context.get('resume')
	#         resume.save()

	#         return redirect(url_for('resumes.resumeDetail',resumeSlug=resumeSlug))
	#     return render_template('resumes/resumeDetail.html', **context)




















@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)