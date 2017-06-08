from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import utils, datetime, time, os
from os import urandom
#from os.path import join, dirname, realpath
from utils import database, accounts, accessDB
import json



from werkzeug.utils import secure_filename

DIR = os.path.dirname(__file__)
if not DIR==".":
  DIR+= "/"
else:
  DIR = ""

UPLOAD_FOLDER = DIR + 'uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
UPLOAD_FOLDER = UPLOAD_FOLDER[1:]
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#print UPLOAD_FOLDER
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

@app.route("/getRandomQuiz/", methods=["GET"])
def getRandQs():
  subj = request.args['subject']
  qs = database.getRandomQuestions(subj)
  theType = 'quiz'
  topic = ''
  time = datetime.datetime.now()
  accessDB.addAccessEntry(time, subj, theType, topic)
  return qs

@app.route("/getRandomDefs/", methods=["GET"])
def getRandDs():
  subj = request.args['subject']
  ds = database.getRandomDefinitions(subj)
  theType = 'definition'
  topic = ''
  time = datetime.datetime.now()
  accessDB.addAccessEntry(time, subj, theType, topic)
  return ds

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
  amount = database.returnQuizAmount(subject)
  return str(amount)

# Returns content of the reuqested quiz
@app.route("/getQuiz/", methods=["GET"])
def getQuiz():
  subject = request.args['subject']
  number = request.args['number']
  theType = 'quiz'
  topic = ''
  time = datetime.datetime.now()
  accessDB.addAccessEntry(time, subject, theType, topic)
  return database.returnQuiz(number, subject)

# Returns content of the reuquested definition set
@app.route("/getDefinition/", methods=["GET"])
def getDefinition():
  subject = request.args['subject']
  number = request.args['number']
  theType = 'definition'
  topic = ''
  time = datetime.datetime.now()
  accessDB.addAccessEntry(time, subject, theType, topic)
  return database.returnDefinition(number, subject)
	
# Returns number of available definition sets
@app.route("/getDefinitionAmount/", methods=["GET"])
def getDefinitionAmount():
  subject = request.args['subject']
  amount = database.returnDefinitionAmount(subject)
  return str(amount)
  
# Returns content of the reuquested definition letter
@app.route("/getDefinitionLetter/", methods=["GET"])
def getDefinitionLetter():
  subject = request.args['subject']
  letter = request.args['letter']
  theType = 'definition'
  topic = ''
  time = datetime.datetime.now()
  accessDB.addAccessEntry(time, subject, theType, topic)
  return database.returnDefinitionLetter(letter, subject)
  
# Returns number of available definition letters
@app.route("/getDefinitionLetterAmount/", methods=["GET"])
def getDefinitionLetterAmount():
  subject = request.args['subject']
  letters = database.returnDefinitionLetterAmount(subject)
  return str(letters)


@app.route("/")
def placeholder1():
  #homepage changes depending on whether admin is logged in or not
  if 'username' in session:
    return redirect("/admin")
  return render_template('index.html', subjects=database.getSubjects(), types=['Questions', 'Notes', 'Definitions'], topics=database.subjectTopic(), title = "Text Tetea")
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

@app.route("/login/", methods=["POST"])
def login():
  user = request.form["admin"]
  pw = request.form["pass"]
  text = accounts.login(user, pw)#error message
  if text == "":#if no error message, succesful go back home
    session["username"] = user
    #print text
    return redirect("/admin")
  else:
    flash(text);
    return redirect("/")

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        
'''def admin():
info = accessDB.getInfoArray()
return render_template('admin.html', subjects=info)'''


@app.route("/admin", methods=['GET', 'POST'])
def upload_file():
  msg = ""
  title = "Tetea Admin"
  info = accessDB.getInfoArray()
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
      #flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    #print file.filename
    if file.filename == '':
      msg = "Please select a file first"
      #flash('No selected file')
      return render_template('admin.html', subjects = info, message=msg,title=title)
    if '.sql' not in file.filename:
      msg = "Only SQL files are accepted"
      return render_template('admin.html', subjects = info, message=msg, title=title)
    else:
      msg = "Your database files have been uploaded"
      filename = secure_filename(file.filename)
      #print filename
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      database.convertDB(filename)
      #print msg
      return redirect(url_for('upload_file',filename=filename, message=msg, title=title))
  return render_template('admin.html', subjects=info, message=msg, title=title)
  #return redirect("/")

@app.route('/uploads/', methods=['GET', 'POST'])
def download():
    return send_file('data/database.sql',attachment_filename='database.sql',as_attachment=True)
  
@app.route("/logout/")
def logout():
  if 'username' in session:
    session.pop("username")
  return redirect("/")

@app.route("/about", methods = ["GET"])
def about():
  admin = False
  if 'username' in session:
    admin = True
  return render_template('about.html', title = 'About', loggedin = admin)

@app.route("/contact/", methods = ["GET"])
def contact():
  admin = False
  if 'username' in session:
    admin = True
  return render_template('contact.html', title = 'Contact', loggedin = admin)
    
@app.route("/changePass/", methods=["POST"])
def changePass():
  accounts.changePass("Admin",request.form['p1'])
  return redirect("/admin")

if __name__ == "__main__":
  app.debug = True
  # app.config.from_object("config")
  # app.secret_key = app.config["SECRET_KEY"]
  app.run()
