from flask.ext.mongoengine.wtf import model_form
from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from nameless.models import Resume

resumes = Blueprint('resumes', __name__, template_folder='templates')


class ListView(MethodView):

    def get(self):
        resumes = Resume.objects.all()
        return render_template('resumes/list.html', resumes=resumes)


class DetailView(MethodView):

    form = model_form(Resume, exclude=['fileName'])

    def get_context(self,resumeSlug):
        resume=Resume.objects.get_or_404(resumeSlug=resumeSlug)
        form = self.form(request.form)

        context = {
                "resume": resume,
                "form": form
        }
        return context

    def get(self, resumeSlug):
        resume = Resume.objects.get_or_404(resumeSlug=resumeSlug)
        return render_template('resume/resumeDetail.html', **context)

    def post(self,resumeSlug):
        context=self.get_context(resumeSlug)
        form = content.get('form')
        if form.validate():
            resume = context.get('resume')
            resume.save()

            return redirect(url_for('resumes.resumeDetail',resumeSlug=resumeSlug))
        return render_template('resumes/resumeDetail.html', **context)


    # def postNamelessResume(self,namelessResumeSlug):
    #     context=self.get_context(namelessResumeSlug)
    #     form = content.getNamelessResume('form')
    #     if form.validate():
    #         resume = context.getNamelessResume('resume')
    #         resume.save()

    #         return redirect(url_for('resumes.resumeDetail',resumeSlug=resumeSlug))
    #     return render_template('resumes/resumeDetail.html', **context)

    # def getNamelessResume(self, namelessResumeSlug):
    #     resume = Resume.objects.get_or_404(namelessResumeSlug=namelessResumeSlug)
    #     return render_template('resume/namelessResumeDetail.html', resume=resume)


# Register the urls
resumes.add_url_rule('/', view_func=ListView.as_view('list'))
resumes.add_url_rule('/<resumeSlug>/', view_func=DetailView.as_view('resumeDetail'))
resumes.add_url_rule('/<namelessResumeSlug>/', view_func=DetailView.as_view('namelessResumeDetail'))


