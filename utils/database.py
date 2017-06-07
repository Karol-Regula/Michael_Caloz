import time, csv, sqlite3, json, os, random

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
  #print "subject: " + subject
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

#retrieves subtopics under certain topic from notes table
def getSubtopicsNotes(topic):
  #print "topic: " + topic
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
      note = i[0].replace('\\n', '<br />')
      ret.append(note)

  if tipe == "Definitions":
    q = "SELECT Word, Definition FROM definitions WHERE subject =?"
    c.execute(q, (subject,))
    whole = c.fetchall()
    for i in whole:
      ret.append({'Word': i[0], 'Definition':i[1]})
      
  if tipe == "Questions":
    q = "SELECT Question, A, B, C, D, E, Answer FROM questions WHERE subject =? AND Flag==?"
    c.execute(q, (subject,""))
    whole = c.fetchall()
    for i in whole:
      if (i[6] != ''):
        ret.append({"Question": i[0], "A": i[1], "B": i[2], "C": i[3], "D":i[4], "E":i[5], "Answer": i[6]})
  closeDB()
  #print ret
  return json.dumps(ret)

#returns dict of 10 random questions
def getRandomQuestions(subject):
  initializeDB()
  ret = []
  q = "SELECT Question, A, B, C, D, E, Answer FROM questions WHERE subject =? AND Flag==?"
  c.execute(q, (subject,""))
  whole = c.fetchall()
  for i in whole:
    if (i[6] != ''):
      ret.append({"Question": i[0], "A": i[1], "B": i[2], "C": i[3], "D":i[4], "E":i[5], "Answer": i[6]})
  closeDB()
  lenRet = len(ret)
  newRet = []
  while len(newRet) < 10:
    ran = random.randint(0,lenRet-1)
    if ret[ran] not in newRet:
      newRet.append(ret[ran])
  return json.dumps(newRet)
  #return newRet   

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
    elif (i[0] not in ret[subTranslate(i[1])]):
      ret[subTranslate(i[1])].append(i[0])
  closeDB()
  return json.dumps(ret)
  
#returns data for requested quiz, scalable
def returnQuiz(quizNumber, subject):
  initializeDB()
  quizNumber = int(quizNumber)
  out = []
  q = "SELECT Question, A, B, C, D, E, Answer FROM questions WHERE subject =? and Flag==?"
  c.execute(q, (subject,""))
  whole = c.fetchall()
  for i in whole:
    if (i[6] != ''):
      out.append({"Question": i[0], "A": i[1], "B": i[2], "C": i[3], "D":i[4], "E":i[5], "Answer": i[6]})
  a = (quizNumber * 10) - 10
  b = (quizNumber * 10)
  #print "a: " + str(a) + "b: " + str(b)
  out = out[a:b]
  closeDB()
  return json.dumps(out)

#returns amount of available quizes for a particular subject, use for returnQuiz()
def returnQuizAmount(subject):
  initializeDB()
  out = []
  q = "SELECT Question, A, B, C, D, E, Answer FROM questions WHERE subject =? AND Flag==?"
  c.execute(q, (subject,""))
  whole = c.fetchall()
  for i in whole:
    if (i[6] != ''):
      out.append({"Question": i[0], "A": i[1], "B": i[2], "C": i[3], "D":i[4], "E":i[5], "Answer": i[6]})
  #print "len(out): " + str(len(out))
  a = (len(out) / 10)
  if a * 10 < len(out):
    a += 1
  closeDB()
  #print "a: " + str(a)
  return a

#returns data for requested definition set, scalable
def returnDefinition(definitionNumber, subject):
  initializeDB()
  definitionNumber = int(definitionNumber)
  out = []
  q = "SELECT Word, Definition FROM definitions WHERE subject =?"
  c.execute(q, (subject,))
  whole = c.fetchall()
  for i in whole:
    out.append({'Word': i[0], 'Definition':i[1]})
  a = (definitionNumber * 10) - 10
  b = (definitionNumber * 10)
  #print "a: " + str(a) + "b: " + str(b)
  out = out[a:b]
  closeDB()
  return json.dumps(out)

#returns amount of available definition sets for a particular subject, use for returnDefinition()
def returnDefinitionAmount(subject):
  initializeDB()
  out = []
  q = "SELECT Word, Definition FROM definitions WHERE subject =?"  
  c.execute(q, (subject,))
  whole = c.fetchall()
  for i in whole:
    out.append({'Word': i[0], 'Definition':i[1]})
  #print "len(out): " + str(len(out))
  a = (len(out) / 10)
  if a * 10 < len(out):
    a += 1
  closeDB()
  #print "a: " + str(a)
  return a
  
#returns data for requested definition set starting with a particular letter of the alphabet, scalable
def returnDefinitionLetter(definitionLetter, subject):
  initializeDB()
  out = []
  nums = ['0','1','2','3','4','5','6','7','8','9']
  q = "SELECT Word, Definition FROM definitions WHERE subject =?"
  c.execute(q, (subject,))
  whole = c.fetchall()
  for i in whole:
    if (i[0][0].upper() == definitionLetter):
      out.append({'Word': i[0], 'Definition':i[1]})
    if (definitionLetter == '#' and str(i[0][0]) in nums):
      out.append({'Word': i[0], 'Definition':i[1]})
  closeDB()
  out.sort(key=lambda x: x['Word']) #sort by word
  return json.dumps(out)
  
#returns list of letters for which definitions exist
def returnDefinitionLetterAmount(subject):
  initializeDB()
  out = []
  num = 0
  nums = ['0','1','2','3','4','5','6','7','8','9']
  letLow = [str(chr(i)) for i in range(ord('a'),ord('z')+1)]
  letUp = [x.upper() for x in letLow] #yay list comprehensions are useful!
  q = "SELECT Word, Definition FROM definitions WHERE subject =?"  
  c.execute(q, (subject,))
  whole = c.fetchall()
  for i in whole:
    if (i[0][0].upper() not in out):
      if (i[0][0] in letLow or i[0][0] in letUp):
        out.append(str(i[0][0]).upper())
      elif (str(i[0][0]) in nums):
        num = 1
  if (num == 1):
    out.append('#')
  out.sort()
  closeDB()
  return json.dumps(out)
  
  
def convertDB(filename):
  os.system('./utils/sqlToSqlite.sh uploads/' + filename +  '| sqlite3 data/databaseNEW.db')
  os.rename('data/database.db', 'data/databaseOLD.db'); #uncomment this to make this function live
  os.rename('data/databaseNEW.db', 'data/database.db'); #change database1 to database to make this function live
  os.rename('uploads/'+ filename, 'uploads/database.sql')
  os.system('mv uploads/database.sql data/')
  #deduplicateDatabase();
  return


#convertDB('sqlDbORIGINAL.sql')

  
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

#deduplicateDatabase()
#print getRandomQuestions('History')
