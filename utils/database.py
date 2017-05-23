import time
import csv
import sqlite3
import json

f = "database.db"

#database headings

#definitions
#idx|Subject|Word|Definition

#notes
#idx|Subject|Form|Topic_Number|Topic_Name|SubTopic_Number|SubTopic_Name|Information_ID|Information

#questions
#ID|Test|Test Type|Year|Subject|Question Number|Part Number|Question|A|B|C|D|E|Answer|Subtopic Name|Flag|Notes

def subTranslate(subject):
  if subject == "C":
    return "Civics"
  if subject == "Z":
    return "Chemistry"
  if subject == "P":
    return "Physics"
  if subject == "B":
    return "Biology"
  if subject == "G":
    return "Geography"
  if subject == "H":
    return "History"
  return "BROKEN"

def revSubTranslate(subject):
  if subject == "Civics":
    return "C"
  if subject == "Chemistry":
    return "Z"
  if subject == "Physics":
    return "P"
  if subject == "Biology":
    return "B"
  if subject == "Geography":
    return "G"
  if subject == "History":
    return "H"
  return "BROKEN"


def initializeDB():
  global c, db
  file = 'data/database.db'
  db = sqlite3.connect(file)
  c = db.cursor()
  #initialize.createDB()
  return c

def closeDB():
  global db
  db.commit()
  db.close()
  
    
def getSampleData():
  initializeDB()
  c.execute('SELECT * FROM questions')
  out = c.fetchall()
  closeDB()
  return out

def getSubjectsDefinitions():
  initializeDB()
  q = 'SELECT subject FROM definitions'
  c.execute(q)
  subjects = c.fetchall()
  allSubjects = []
  for i in subjects:
    if not i in allSubjects:
      allSubjects.append(i)
  closeDB()
  return allSubjects
  
def getSubjectsNotes():
  initializeDB()
  q = 'SELECT subject FROM notes'
  c.execute(q)
  subjects = c.fetchall()
  allSubjects = []
  for i in subjects:
    if not i in allSubjects:
      allSubjects.append(i)
  closeDB()
  return allSubjects
  
def getSubjectsQuestions():
  initializeDB()
  q = 'SELECT subject FROM questions'
  c.execute(q)
  subjects = c.fetchall()
  allSubjects = []
  for i in subjects:
    if not i in allSubjects:
      allSubjects.append(i)
  closeDB()
  return allSubjects

def getSubtopicNotes():
  initializeDB()
  q = 'SELECT SubTopic_Name FROM notes'
  c.execute(q)
  subjects = c.fetchall()
  allSubjects = []
  for i in subjects:
    if not i in allSubjects:
      allSubjects.append(i)
  closeDB()
  return allSubjects

def getSubtopicQuestions():
  initializeDB()
  q = 'SELECT Subtopic Name FROM questions'
  c.execute(q)
  subjects = c.fetchall()
  allSubjects = []
  for i in subjects:
    if not i in allSubjects:
      allSubjects.append(i)
  closeDB()
  return allSubjects

#retrieves the topics under a certain subject from question table
def getTopicsNotes(subject):
  print "subject: " + subject
  initializeDB()
  q = 'SELECT Topic_Name FROM notes WHERE subject=?'
  c.execute(q, (revSubTranslate(subject),))
  info = c.fetchall()
  topics = []
  for i in info:
    if not i in topics:
      topics.append(i)
  closeDB()
  #print topics
  return topics

#print getTopicsNotes("Physics")

#retrieves subtopics under certain topic from notes table
def getSubtopicsNotes(topic):
  print "topic: " + topic
  initializeDB()
  q = 'SELECT Subtopic_Name FROM notes WHERE Topic_Name=?'
  info = c.execute(q, (topic,))
  subtopics = []
  for i in info:
    if not i in subtopics:
      subtopics.append(i)
  closeDB()
  #print subtopics
  return subtopics

def getSubjects():
  subDef = getSubjectsDefinitions()
  subNot = getSubjectsNotes()
  subQue = getSubjectsQuestions()
  
  out = []
  for sub in subDef:
    #print sub
    if sub[0] not in out:
      out.append(sub[0])
  for sub in subQue:
    #print sub
    if sub[0] not in out:
      out.append(sub[0])
  for sub in subNot:
    #print sub
    if subTranslate(sub[0]) not in out:
      out.append(subTranslate(sub[0]))
  #print out
  return out
  
#subject,type,topic -> content. type: questions, notes, or definitions
#retrieves the information from specified subject in the specified type table
def content(subject,tipe,topic):
  initializeDB()
  ret = []
  if tipe == "Notes":
    subject = revSubTranslate(subject)
    q = "SELECT Information FROM notes WHERE Subject=? AND Topic_Name=?"
    c.execute(q, (subject,topic))
    for i in c.fetchall():
      ret.append(i[0])
    print ret

  if tipe == "Definitions":
    q = "SELECT Word, Definition FROM definitions WHERE subject =?"
    c.execute(q, (subject,))
    whole = c.fetchall()
    for i in whole:
      ret.append({'Word': i[0], 'Definition':i[1]})
      
  if tipe == "Questions":
    q = "SELECT Question, A, B, C, D, E, Answer FROM questions WHERE subject =?"
    c.execute(q, (subject,))
    whole = c.fetchall()
    for i in whole:
      if (i[6] != ''):
        ret.append({"Question": i[0], "A": i[1], "B": i[2], "C": i[3], "D":i[4], "E":i[5], "Answer": i[6]})
        #print "i[6]" + str(i[6])
  closeDB()
  #print ret
  return json.dumps(ret)

#print content("Physics", "Notes", "Applications of Vectors")

#return dictionary of subject:[topics] for the notes
def subjectTopic():
  initializeDB()
  q = 'SELECT Topic_Name, Subject FROM notes'
  c.execute(q)
  info = c.fetchall()
  ret = {}
  for i in info:
    if subTranslate(i[1]) not in ret:
      ret[subTranslate(i[1])] = [i[0]]
    else:
      ret[subTranslate(i[1])].append(i[0])
  for item in ret:
    ret[item] = list(set(ret[item])    )
  closeDB()
  return json.dumps(ret)
  
#removes duplicate entires from database
def deduplicateDatabase():
  initializeDB()
  q = 'DELETE FROM definitions WHERE rowid NOT IN(SELECT min(rowid) FROM definitions GROUP BY idx, Definition)'
  c.execute(q);
  q = 'DELETE FROM questions WHERE rowid NOT IN(SELECT min(rowid) FROM questions GROUP BY Question, A)'
  c.execute(q);
  q = 'DELETE FROM notes WHERE rowid NOT IN(SELECT min(rowid) FROM notes GROUP BY idx, Information)'
  c.execute(q);
  q = 'vacuum'
  c.execute(q);
  closeDB()


def initializeAccessDB():
  global c, db
  file = 'data/access.db'
  db = sqlite3.connect(file)
  c = db.cursor()
  #initialize.createDB()
  return c


#converting time to nice time: time.asctime(localtime())
def addAccessEntry(time, subject, tipe, topic):
  initializeAccessDB()
  q = 'INSERT INTO clicks VALUES(?,?,?,?)'
  c.execute(q, (time, subject, tipe, topic))
  closeDB()
    
  
#deduplicateDatabase()
  
  
#print subjectTopic()

#print content('Geography','definitions','')

'''   
getSubjectsDefinitions()
getSubjectsNotes()
getSubjectsQuestions()
getSubtopicQuestions()
print getSubtopicNotes()
'''
