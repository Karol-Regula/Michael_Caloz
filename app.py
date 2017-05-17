from flask import Flask, render_template, request, redirect, url_for, session
import utils
from os import urandom
from utils import database, accounts
import json

app = Flask(__name__)
app.secret_key = urandom(20)

# Returns comma-separated str of topics available
# for the requested material type
@app.route("/getSubjectByType/", methods=["GET"])
def getTopics():
        #print session['access']
	topics = []
	materialType = request.args['category']
	if materialType=='Definitions':
		topics = database.getSubjectsDefinitions()
	elif materialType=='Notes':
		topics = database.getSubjectsNotes()
	elif materialType=='Questions':
		topics = database.getSubjectsQuestions()
	else:
		print "Invalid argument"
	ret = [topic[0] for topic in topics] #bc tuple
	return ",".join(ret)

# Returns comma-separated str of subtopics available
# for the requested topic
@app.route("/getTopics/", methods=["GET"])
def getTopicsBy():
	topic = request.args['category']
        session['access'] += 1
	subs = database.getTopicsNotes(topic)
	ret = [sub[0] for sub in subs]
	return ",".join(ret)

@app.route("/")
def placeholder1():
	session['access'] = 0 #increment to record amount of time information is accessed
	print json.dumps(database.getTopicsNotes('Civics'))
	return render_template('index.html', subjects=database.getSubjects(), types=['Questions', 'Notes', 'Lessons'], topics=json.dumps(database.getTopicsNotes('Civics')));

@app.route("/slash")
def placeholder0():
	data = database.getSubjects()
	return render_template('test.html', variable = data)


if __name__ == "__main__":
    app.debug = True
    # app.config.from_object("config")
    # app.secret_key = app.config["SECRET_KEY"]
    app.run()

#next thing due:
#FRIDAY: demo of progress, site design, discuss what is being worked on/project
