#functions for doing stuff with access.db

import sqlite3
import json
import os

DIR = os.path.dirname(__file__)
if DIR==".":
  DIR+= "/"
  f = DIR+"access.db"
else:
  f = "data/access.db"
  #print f

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

#currently adds entry to database table
#converting time to nice time: time.asctime(localtime())
def addAccessEntry(time, subject, tipe, topic):
  initializeAccessDB()
  q = 'INSERT INTO clicks VALUES(?,?,?,?)'
  try:
    c.execute(q, (time, subject, tipe, topic))
  except:
    c.execute("CREATE TABLE clicks (time TEXT, subject TEXT, tipe TEXT, topic TEXT)")
    c.execute(q, (time, subject, tipe, topic))
  closeDB()

#retrieves the amount of times the info for each subject is accessed
#dictionary format: {subject: freq}
#eventually, this should be by month eventually
def getInfo():
  initializeAccessDB()
  q = 'SELECT * FROM clicks'
  try:
    c.execute(q)
  except:
    c.execute("CREATE TABLE clicks (time TEXT, subject TEXT, tipe TEXT, topic TEXT)")
    c.execute(q)
    
  totalDB = c.fetchall()
  retFormat = {}
  for i in range(len(totalDB)):
    subject = totalDB[i][1]
    if subject in retFormat:
      retFormat[subject]+=1
    else:
      retFormat[subject] = 1
  closeDB()
  return retFormat

def getInfoArray():
    dictionary = getInfo()
    retArray = [["subject","frequency"]]
    for item in dictionary:
        if item != "":
            retArray.append([item, dictionary[item], "#01b230"])
    return retArray

#print getInfo()
#print getInfoArray()    

