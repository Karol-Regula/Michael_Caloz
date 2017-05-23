#!/usr/bin/python
'''
initializing second database file that tallies the clicks on the website
'''
import sqlite3   #enable control of an sqlite database
import os


f = "access.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#------------------------create tables---------------------------------------
q = "CREATE TABLE clicks (time FLOAT, subject TEXT, tipe TEXT, topic TEXT)"
c.execute(q)



db.commit()
db.close()
