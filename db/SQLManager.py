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
		
	###################################################
	#             USER-RELATED FUNCTIONS              #
	###################################################

	# Creates a new user in the database. Can also be used to change password
	# id is the username, and pw is the user's password
	def newUser(self, id, pw):
		stmt = "INSERT INTO users (id, pw) VALUES (%s, %s) ON DUPLICATE KEY UPDATE pw = %s;"
		__execute(stmt, (id, pw, pw))
		
	# Returns 1 if user exists, 0 if not
	def userExists(self, id):
		stmt = "SELECT EXISTS(SELECT * FROM users WHERE id = %s);"
		return __fetch(stmt, (id,))
		
	# Gets a user info. Options are id, pw, xp, streak, lastapp
	def getUserInfo(self, id, o):
		stmt = "SELECT ? FROM users WHERE id = %s;".replace("?", o)
		return __fetch(stmt, (id,))
		
	# Increments a user's exp by certain amount
	def addXp(self, id, add):
		stmt = "UPDATE users SET xp = xp + %s WHERE id = %s"
		__execute(stmt, (add, id))
		
	# Removes a user's streak
	def removeStreak(self, id):
		stmt = "UPDATE users SET streak = 0 WHERE id = %s"
		__execute(stmt, (id,))
	
	# Increments a user's streak and sets the date to cur date
	def increaseStreak(self, id):
		stmt1 = "UPDATE users SET streak = streak + 1 WHERE id = %s;"
		stmt2 = "UPDATE users SET lastapp = current_date() WHERE id = %s;"
		__execute(stmt1, (id,))
		__execute(stmt2, (id,))
		
	###################################################
	#             JOB-RELATED FUNCTIONS               #
	###################################################
	
	# Create a new job with id and link. Updates itself as necessary
	def newJob(self, id, link, title, location):
		stmt = "INSERT INTO jobs (id, link, title, location) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE link = %s, title = %s, location = %s;"
		__execute(stmt, (id, link, title, location, link, title, location))
	
	# If a job is expired, it may be removed, which removes it from all users that saved it as well
	def removeJob(self, id):
		stmt = "DELETE FROM jobs WHERE id = %s"
		____execute(stmt, (id,))
		
	# Get job info. Options are id, link, title, location
	def getJobInfo(self, id, o):
		stmt = "SELECT ? FROM jobs WHERE id = %s;".replace("?", o)
		return __fetch(stmt, (id,))
		
	###################################################
	#                UTILITY + PRIVATE                #
	###################################################
        
	# Should be called when program exits
	def close(self):
		self.cur.close()
		self.cnx.close()
		
	# Private function to execute table-modifying statements
	def __execute(stmt, info):
		self.cur.execute(stmt, info)
		self.cnx.commit()
		
	# Private function to make fetching single data pieces easier
	def __fetch(stmt, info):
		self.cur.execute(stmt, info)
		return self.cur.fetchone()[0]