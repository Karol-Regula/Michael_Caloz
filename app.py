from flask import Flask, render_template, request, redirect, url_for, session
import utils, datetime, time
from os import urandom
from utils import database, accounts, accessDB
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
        #session['access'] += 1
	subs = database.getTopicsNotes(topic)
	ret = [sub[0] for sub in subs]
	return ",".join(ret)
	
# Returns number of available quizzes
@app.route("/getQuizAmount/", methods=["GET"])
def getQuizAmount():
	subject = request.args['subject']
	print "getQuizAmount():"
	amount = database.returnQuizAmount(subject)
	return str(amount)
	
# Returns content of the reuqested quiz
@app.route("/getQuiz/", methods=["GET"])
def getQuiz():
	subject = request.args['subject']
	number = request.args['number']
	return database.returnQuiz(number, subject)

@app.route("/")
def placeholder1():
        #homepage changes depending on whether admin is logged in or not
        if 'username' in session:
                admin = True
	return render_template('index.html', subjects=database.getSubjects(), types=['Questions', 'Notes', 'Definitions'], topics=database.subjectTopic())
#, admin=admin);

@app.route("/slash")
def placeholder0():
	data = database.getSubjects()
	return render_template('test.html', variable = data)

@app.route("/getContent/", methods=["GET"])
def getContent():
	#print request.args.keys()
	subj = request.args['subject']
	theType = request.args['type']
	topic = request.args['topic']
        time = datetime.datetime.now()
        accessDB.addAccessEntry(time, subj, theType, topic)
	return database.content(subj, theType, topic)

@app.route("/login", methods=["POST"])
def login():
        user = request.form["admin"]
        pw = request.form["pass"]
        text = account.login(un, pw)#error message
        if text == "":#if no error message, succesful go back home
                session["username"] = user
                print text
                return redirect("/")
        else:
                return render_template("login.html", login_error=text)
        
@app.route("/admin")
def admin():
        #add something that shows data from access.db
        info = accessDB.getInfoArray()
        return render_template('admin.html', subjects=info);

@app.route("/logout/", methods=['POST'])
def logout():
        session.pop("username")
        return redirect("/")

if __name__ == "__main__":
        app.debug = True
        # app.config.from_object("config")
        # app.secret_key = app.config["SECRET_KEY"]
        app.run()

#next thing due:
#FRIDAY: demo of progress, site design, discuss what is being worked on/project
