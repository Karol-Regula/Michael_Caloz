import csv
import sqlite3

f = "database.db"


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
  closeDB
  return out
