import os
import random
import json
import mysql.connector

class SQLManager:
	def __init__(self):
		with open('mysql.json') as mysql_info:
			config = json.load(mysql_info)
		self.cnx = mysql.connector.connect(**config)
		self.cur = self.cnx.cursor()

	# Creates a new user in the database. Can also be used to change password
	# id is the username, and pw is the user's password
	def newUser(self, id, pw):
		info = (id, pw, pw)
		stmt = "INSERT INTO users (id, pw) VALUES (%s, %s) ON DUPLICATE KEY UPDATE pw = %s;"
		self.cur.execute(stmt, info)
		self.cnx.commit()
		
	# Returns 1 if user exists, 0 if not
	def userExists(self, id):
		info = (id,)
		stmt = "SELECT EXISTS(SELECT * FROM users WHERE id = %s);"
		self.cur.execute(stmt, info)
		return self.cur.fetchone()[0]
		
	# Gets a user info. Options are id, pw, xp, streak, lastapp
	def getUserInfo(self, id, o):
		info = (id,)
		stmt = "SELECT ? FROM users WHERE id = %s;".replace("?", o)
		self.cur.execute(stmt, info)
		return self.cur.fetchone()[0]
		
	# Increments a user's exp by certain amount
	def addXp(self, id, add):
		info = (add, id)
		stmt = "UPDATE users SET xp = xp + %s WHERE id = %s"
		self.cur.execute(stmt, info)
		self.cnx.commit()
		
	# Removes a user's streak
	def removeStreak(self, id):
		info = (id,)
		stmt = "UPDATE users SET streak = 0 WHERE id = %s"
		self.cur.execute(stmt, info)
		self.cnx.commit()
	
	# Increments a user's streak and sets the date to cur date
	def increaseStreak(self, id):
		info = (id,)
		stmt1 = "UPDATE users SET streak = streak + 1 WHERE id = %s;"
		stmt2 = "UPDATE users SET lastapp = current_date() WHERE id = %s;"
		self.cur.execute(stmt1, info)
		self.cur.execute(stmt2, info)
		self.cnx.commit()
        
	def close(self):
		self.cur.close()
		self.cnx.close()