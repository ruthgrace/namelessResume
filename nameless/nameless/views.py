from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from nameless.models import Resume

resumes = Blueprint('resumes', __name__, template_folder='templates')


class ListView(MethodView):

    def get(self):
        resumes = Resume.objects.all()
        return render_template('resumes/list.html', resumes=resumes)


class DetailView(MethodView):

    def get(self, resumeSlug):
        resume = Resume.objects.get_or_404(resumeSlug=resumeSlug)
        return render_template('resume/resumeDetail.html', resume=resume)

    def getNameless(self, namelessResumeSlug):
        resume = Resume.objects.get_or_404(namelessResumeSlug=namelessResumeSlug)
        return render_template('resume/namelessResumeDetail.html', resume=resume)

# Register the urls
resumes.add_url_rule('/', view_func=ListView.as_view('list'))
resumes.add_url_rule('/<resumeSlug>/', view_func=DetailView.as_view('resumeDetail'))
resumes.add_url_rule('/<namelessResumeSlug>/', view_func=DetailView.as_view('namelessResumeDetail'))


