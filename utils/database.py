import csv
import sqlite3

f = "database.db"

#database headings

#definitions
#idx|Subject|Word|Definition

#notes
#idx|Subject|Form|Topic_Number|Topic_Name|SubTopic_Number|SubTopic_Name|Information_ID|Information

#questions
#ID|Test|Test Type|Year|Subject|Question Number|Part Number|Question|A|B|C|D|E|Answer|Subtopic Name|Flag|Notes

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
  q = 'SELECT "Topic_Name" FROM notes WHERE subject=?'
  c.execute(q, (subject,))
  info = c.fetchall()
  topics = []
  for i in info:
    if not i in topics:
      topics.append(i)
  closeDB()
  #print topics
  return topics
  
def getSubtopicsNotes(topic):
  print "topic: " + topic
  initializeDB()
  q = 'SELECT "Subtopic_Name" FROM notes WHERE Topic_Name=?'
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
    if sub[0] not in out:
      out.append(sub[0])
  for sub in subQue:
    if sub[0] not in out:
      out.append(sub[0])
  for sub in subNot:
    if subTranslate(sub[0]) not in out:
      out.append(subTranslate(sub[0]))
  return out
  
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

#subject,type,topic -> content. type: questions, notes, or definitions
def content(subject,tipe,topic):
  initializeDB()
  if tipe == "notes":
    q = "SELECT Information FROM notes WHERE subject =? and topic=?"
    con = c.execute(q, (subject,topic))
  if tipe == "definitions":
    q = "SELECT Word, Definition FROM definitions WHERE subject =?"
    con = c.execute(q, (subject,))
  if tipe == "questions":
    q = "SELECT Question, A, B, C, D, E, Answer FROM questions WHERE subject =?"
    con = c.execute(q, (subject,))
  content = c.fetchall()
  closeDB()
  return content


#print content('Geography','definitions','')

'''   
getSubjectsDefinitions()
getSubjectsNotes()
getSubjectsQuestions()
getSubtopicQuestions()
print getSubtopicNotes()
'''
