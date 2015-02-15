import datetime
from flask import url_for
from nameless import db


class Resume(db.Document):
#    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
#    title = db.StringField(max_length=255, required=True)
    fileName = db.StringField(max_length=255, required=True)
    resumeSlug = db.StringField(max_length=255, required=True)
    namelessResumeSlug = db.StringField(max_length=255, required=True)
    otherInfo = db.StringField()
#    body = db.StringField(required=True)
#    comments = db.ListField(db.EmbeddedDocumentField('Comment'))

    def get_resume_url(self):
        return url_for('post', kwargs={"resumeSlug": self.resumeSlug})

    def get_nameless_resume_url(self):
        return url_for('post', kwargs={"namelessResumeSlug": self.namelessResumeSlug})

#    def get_url(self):
#        return url_for('post', kwargs={"slug": self.slug})

#    def __unicode__(self):
#        return self.title

    def __unicode__(self):
        return self.fileName


    meta = {
        'allow_inheritance': True,
        'indexes': ['-fileName'],
        'ordering': ['-fileName']
    }


#class Comment(db.EmbeddedDocument):
#    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
#    body = db.StringField(verbose_name="Comment", required=True)
#    author = db.StringField(verbose_name="Name", max_length=255, required=True)
