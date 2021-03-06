import sqlite3
import os
from hashlib import sha1

def initializeDB():
  global c, db
  DIR = os.path.dirname(__file__)
  print "DIR ACCS: " + DIR
  if not DIR==".":
    DIR+= "/../"
    f = DIR+"data/admin.db"
  else:
    f = "data/admin.db"
  #print f
  db = sqlite3.connect(f)
  c = db.cursor()
  return c

def closeDB():
  global db
  db.commit()
  db.close()

def initializeAdmin():
  initializeDB()
  tableCreateQuery = "CREATE TABLE IF NOT EXISTS Accounts (username TEXT, password TEXT, salt TEXT, defaultPW TEXT)"
  c.execute(tableCreateQuery)
  user = "Admin"
  adminQuery = "INSERT INTO Accounts VALUES (?,?,?,?)"
  salt = os.urandom(10).encode('hex')
  password = sha1("pass"+salt).hexdigest()
  default = sha1("pass"+salt).hexdigest()
  c.execute(adminQuery, (user, password, salt, default))
  ret = "Admin account not created. Now login."
  closeDB()
  return ret

#print initializeAdmin()

# Returns "" if login succeeds and returns
# string of reason why login failed otherwise
def login(user,password):
  initializeDB()
  query = ("SELECT * FROM Accounts WHERE username=?")
  ret = "n/a"
  
  try: # TABLE EXISTS
    sel = c.execute(query,(user,))
    # Check if pass matches
    # record = (user, password, salt)
    for record in sel:
      password = sha1(password+record[2]).hexdigest()
      if (password==record[1]):
  	    ret = ""
      else: #password doesn't match
  	    ret = "Wrong username or password"    
    if ret=="n/a": # no records
  	  ret = "Username does not exist"
        
  except: # TABLE does NOT exist
    ret = "Admin account does not exist. Please contact administator."
  closeDB()
  #ret = ""
  return ret

#gives admin the ability to change the password
def changePass(user, pw):
  initializeDB()
  query = "SELECT * FROM Accounts WHERE username=?"
  info = c.execute(query, (user,))
  salt = ""
  ret = ""
  for record in info:
    salt = record[2]
    pw = sha1(pw+salt).hexdigest()
    changeQuery = "UPDATE Accounts SET PASSWORD = ? WHERE USERNAME = ?"
    c.execute(changeQuery, (pw, user))
    ret = "Password is now changed."
  closeDB()
  return ret
  
#changePass('administratorTetea', 'pass')
  
def getPassword(user):
  initializeDB()
  queryCheck = "SELECT * FROM Accounts WHERE username=?"
  check = c.execute(queryCheck, (user,))
  password = ""
  for record in check:
    password = record[1]
    closeDB()
  return password

def getDefault(user):
  initializeDB()
  queryCheck = "SELECT * FROM Accounts WHERE username=?"
  check = c.execute(queryCheck, (user,))
  password = ""
  for record in check:
    password = record[3]
    closeDB()
  return password

#initializeAdmin()
#print getDefault("Admin")
#print changePass("Admin","passChanged!")
#print getPassword("Admin")

# Checks if user already exists
# Returns True if exists, False if doesn't
def duplicate(user):
  db = connect(f)
  c = db.cursor()
  query = ("SELECT * FROM Accounts WHERE username=?")
  sel = c.execute(query,(user,))
  ret = False
  for record in sel:
    # if any records, must be true
    ret = True
    break
  db.commit()
  db.close()
  return ret

# TESTS:
#clear accounts
#db = connect(f)
#c = db.cursor()
#c.execute("DELETE FROM Accounts WHERE username=='EmmaVook'")
#db.commit()
#db.close()

# run actual tests
#print login("EmmaVook", "softDev123")
#print register("EmmaVook", "softDev123", "Bayless")
#print register("EmmaVook", "softDev123", "softDev123")
#print login("EmmaVook", "softDev123")
#print login("EmmaVook", "Bayless")
