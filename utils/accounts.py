from sqlite3 import connect
from os import urandom
from hashlib import sha1

tableCreateQuery = "CREATE TABLE Accounts (username TEXT, password TEXT, salt TEXT)"

f = "tetea.db"

# Returns "" if login succeeds and returns
# string of reason why login failed otherwise
def login(user,password):
	db = connect(f)
	c = db.cursor()

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
		c.execute(tableCreateQuery)
		ret = "Create an account!" # account could not exist

	db.commit()
	db.close()
	return ret

#Arguments: username, two attempts at password
#Returns success message or error
def register(user, password, p2):
	if not password==p2:
		return "Password attempts differ"

	db = connect(f)
	c = db.cursor()
	ret = ""
	try:
		c.execute("SELECT * FROM Accounts")
		reg = regReqs(user, password)
		if reg == "": #no error from args
			#hash pass and add
			salt = urandom(10).encode('hex')
			query = ("INSERT INTO Accounts VALUES (?, ?, ?)")
			password = sha1(password+salt).hexdigest()
			c.execute(query, (user,password,salt))
			ret = "Account created!"
		else: # return error from args
			ret = reg
	except: #create table and now register
		c.execute(tableCreateQuery)
		ret = register(user,password,p2)
	db.commit()
	db.close()
	return ret

# Does basic checks on username and password
# for general strength (length, characters)
# REQUIREMENTS:
	# password between 8 and 32 characters
	# username between 5 and 32 characters
	# no spaces in username or password
	# username and password must be different
def regReqs(user, password):
	if len(password) < 8 or len(password) > 32:
		return "Password must be 8-32 characters"
	if len(user) < 5 or len(user) > 32:
		return "Username must be 8-32 characters"
	if duplicate(user):          #checks if username already exists
		return "Username already exists"
	if " " in user or " " in password:
		return "Spaces not allowed in user or password"
	if user==password:
		return "Username and password must be different"
	return ""

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