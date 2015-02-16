#nameless resume

Companies and institutions try very hard to have unbiased hiring, but the fact of the matter is that if you have a female name or a stereotypically black name, you are less likely to be hired than your white male counterparts, despite identical experience.

Even STEM professors rate a female applicant for a research assistant position as less hireable and less competent compared to an identical male applicant. They even offer the female a lower starting salary on average, and are less willing to want to mentor her.

The problem lies in unconscious bias, and the solution is to blind names on resumes.

###development process

This was made Frankensteining the Tumblelog mongodb/flask tutorial
http://docs.mongodb.org/ecosystem/tutorial/write-a-tumblelog-application-with-flask-mongoengine/
and the flask file upload tutorial
http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
with a C++ script to find and remove the names from resumes.

Everything was uploaded to GitHub by Ruth, but the development team included David Wang and Victor Duan from the University of Waterloo, and Bhaag Marway from McMaster University.

We are thankful for the mentorship received from Sophia from Waterloo, Shy from MLH, and Alex from Morgan Stanley

##Run instructions

###requirements
mongoDB
http://www.mongodb.org/downloads
```
pip install virtualenv
pip install flask
pip install flask-script
pip install WTForms
pip install mongoengine
pip install flask_mongoengine
```

###make db:
```
mongod --dbpath myDBpath
```
instantiate db using this tutorial http://docs.mongodb.org/manual/tutorial/getting-started/#create-a-collection-and-insert-documents

###add some stuff into the db:
```
> python manage.py shell
>>> from models import Resume
>>> newResume = Resume(
... fileName="myResume.pdf",
... resumeSlug="myResume.pdf",
... namelessResumeSlug="nameless_myResume.pdf"
... )
>>> newResume.save()
>>> newResume2 = Resume(
... fileName="myResume2.pdf",
... resumeSlug="myResume2Slug.pdf",
... namelessResumeSlug="myNamelessResume2Slug.pdf"
... )
>>> newResume2.save()
```

###run server
python manage.py runserver
access server by going to http://localhost:5000/

###edit database manually
open mongo shell
```
> mongo
> use resumeDB
> db.resumeDB.remove({})
```

###get input files
resumes must be in html format. you can convert PDF resumes to HTML using http://www.pdfonline.com/convert-pdf-to-html/

##future directions
* convert PDF resumes to HTML for the blinding
