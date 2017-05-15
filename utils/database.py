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
  
  
#database headings
  
#definitions
#idx|Subject|Word|Definition

#notes
#idx|Subject|Form|Topic_Number|Topic_Name|SubTopic_Number|SubTopic_Name|Information_ID|Information

#questions
#ID|Test|Test Type|Year|Subject|Question Number|Part Number|Question|A|B|C|D|E|Answer|Subtopic Name|Flag|Notes
