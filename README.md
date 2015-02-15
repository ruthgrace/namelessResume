#nameless resume



currently only has a database.

This was made using the Tumblelog tutorial
http://docs.mongodb.org/ecosystem/tutorial/write-a-tumblelog-application-with-flask-mongoengine/


##Run instructions

###make db:
```
mongod --dbpath myDBpath
```
instantiate db using this tutorial http://docs.mongodb.org/manual/tutorial/getting-started/#create-a-collection-and-insert-documents

###add some stuff into the db:
```
> python manage.py shell
>>> newResume = Resume(
... fileName="myResume.pdf"
... ,
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


###future directions
* gotta upload files and connect the uploaded files with the database http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
* incorporate victor's HTML resume name blinding
* make the website display original and blinded resumes on an interface
* convert PDF resumes to HTML for the blinding
