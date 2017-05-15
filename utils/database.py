import csv
import sqlite3

f = "database.db"


def initializeDB():
  global c, db
  file = '../data/database.db'
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
  closeDB
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
    print allSubjects
    
def getSubjectsNotes():
    initializeDB()
    q = 'SELECT subject FROM notes'
    c.execute(q)
    subjects = c.fetchall()
    allSubjects = []
    for i in subjects:
        if not i in allSubjects:
            allSubjects.append(i)
    print allSubjects
    
def getSubjectsQuestions():
    initializeDB()
    q = 'SELECT subject FROM questions'
    c.execute(q)
    subjects = c.fetchall()
    allSubjects = []
    for i in subjects:
        if not i in allSubjects:
            allSubjects.append(i)
    print allSubjects

getSubjectsDefinitions()
getSubjectsNotes()
getSubjectsQuestions()
