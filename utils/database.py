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

#retrieves the subtopics under a certain subject from question table
def getSubtopicsNotes(subject):
  print "subject: " + subject
  initializeDB()
  q = 'SELECT "Topic_Name" FROM notes WHERE subject=?'
  info = c.execute(q, (subject,))
  subtopics = []
  for i in info:
    subtopics.append(i)
  closeDB()
  print subtopics
  return subtopics

#getSubtopicQuestions()
#print getSubtopicNotes()


'''   
getSubjectsDefinitions()
getSubjectsNotes()
getSubjectsQuestions()
'''
