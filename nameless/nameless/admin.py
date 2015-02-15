from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form

from nameless.auth import requires_auth
from nameless.models import Resume

admin = Blueprint('admin', __name__, template_folder='templates')


class List(MethodView):
    decorators = [requires_auth]
    cls = Resume

    def get(self):
        resumes = self.cls.objects.all()
        return render_template('admin/list.html', resumes=resumes)


class Detail(MethodView):

    decorators = [requires_auth]

    def get_context(self, resumeSlug=None):
        form_cls = model_form(Resume, exclude=('otherInfo'))

        if resumeSlug:
            resume = Resume.objects.get_or_404(resumeSlug=resumeSlug)
            if request.method == 'POST':
                form = form_cls(request.form, inital=resume._data)
            else:
                form = form_cls(obj=resume)
        else:
            resume = Resume()
            form = form_cls(request.form)

        context = {
            "resume": resume,
            "form": form,
            "create": resumeSlug is None
        }
        return context

    def get(self, resumeSlug):
        context = self.get_context(resumeSlug)
        return render_template('admin/resumeDetail.html', **context)

    # def getNamelessResume(self, namelessResumeSlug):
    #     context = self.get_context(namelessResumeSlug)
    #     return render_template('admin/namelessResumeDetail.html', **context)


    def post(self, resumeSlug):
        context = self.get_context(resumeSlug)
        form = context.get('form')

        if form.validate():
            resume = context.get('resume')
            form.populate_obj(resume)
            resume.save()

            return redirect(url_for('admin.index'))
        return render_template('admin/resumeDetail.html', **context)

    # def postNamelessResume(self, namelessResumeSlug):
    #     context = self.get_context(namelessResumeSlug)
    #     form = context.getNamelessResume('form')

    #     if form.validate():
    #         resume = context.getNamelessResume('resume')
    #         form.populate_obj(resume)
    #         resume.save()

    #         return redirect(url_for('admin.index'))
    #     return render_template('admin/namelessResumeDetail.html', **context)


# Register the urls
admin.add_url_rule('/admin/', view_func=List.as_view('index'))
admin.add_url_rule('/admin/create/', defaults={'resumeSlug': None}, view_func=Detail.as_view('create'))
admin.add_url_rule('/admin/<resumeSlug>', view_func=Detail.as_view('editResume'))
admin.add_url_rule('/admin/<namelessResumeSlug>/', view_func=Detail.as_view('editNamelessResume'))
