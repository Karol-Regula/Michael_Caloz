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
