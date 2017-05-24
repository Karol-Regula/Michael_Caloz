#functions for doing stuff with access.db

import sqlite3
import json

f = "data/access.db"

def initializeAccessDB():
  global c, db
  db = sqlite3.connect(f)
  c = db.cursor()
  #initialize.createDB()
  return c

def closeDB():
  global db
  db.commit()
  db.close()


#converting time to nice time: time.asctime(localtime())
def addAccessEntry(time, subject, tipe, topic):
  initializeAccessDB()
  q = 'INSERT INTO clicks VALUES(?,?,?,?)'
  try:
    c.execute(q, (time, subject, tipe, topic))
  except:
    c.execute("CREATE TABLE clicks (time TEXT, subject TEXT, tipe TEXT, topic TEXT)")
    return addAccessEntry(time,subject,tipe,topic)
  closeDB()

#somehow, this should be by month eventually
def getInfo():
  q = 'SELECT * FROM clicks'
  c.execute(q)
  totalDB = c.fetchall()
  #retFormat = subject: freq
  retFormat = {}
  for i in totalDB:
    if totalDB[1] in retFormat:
      retFormat[subject]+=1
    else:
      retFormat[subject] = 1
      
    
    

