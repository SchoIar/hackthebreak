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
		self.__execute(stmt, (id, pw, pw))
		
	# Returns 1 if user exists, 0 if not
	def userExists(self, id):
		stmt = "SELECT EXISTS(SELECT * FROM users WHERE id = %s);"
		return self.__fetch(stmt, (id,))
		
	# Gets a user info. Options are id, pw, xp, streak, lastapp
	def getUserInfo(self, id, o):
		stmt = "SELECT ? FROM users WHERE id = %s;".replace("?", o)
		return self.__fetch(stmt, (id,))
		
	# Increments a user's exp by certain amount
	def addXp(self, id, add):
		stmt = "UPDATE users SET xp = xp + %s WHERE id = %s"
		self.__execute(stmt, (add, id))
		
	# Removes a user's streak
	def removeStreak(self, id):
		stmt = "UPDATE users SET streak = 0 WHERE id = %s"
		self.__execute(stmt, (id,))
	
	# Increments a user's streak and sets the date to cur date
	def increaseStreak(self, id):
		stmt1 = "UPDATE users SET streak = streak + 1 WHERE id = %s;"
		stmt2 = "UPDATE users SET lastapp = current_date() WHERE id = %s;"
		self.__execute(stmt1, (id,))
		self.__execute(stmt2, (id,))
		
	###################################################
	#             JOB-RELATED FUNCTIONS               #
	###################################################
	
	# Create a new job with id and link. Updates itself as necessary
	def newJob(self, id, link, title, location):
		stmt = "INSERT INTO jobs (id, link, title, location) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE link = %s, title = %s, location = %s;"
		self.__execute(stmt, (id, link, title, location, link, title, location))
	
	# If a job is expired, it may be removed, which removes it from all users that saved it as well
	def removeJob(self, id):
		stmt = "DELETE FROM jobs WHERE id = %s"
		self.__execute(stmt, (id,))
		
	# Get job info. Options are id, link, title, location
	def getJobInfo(self, id, o):
		stmt = "SELECT ? FROM jobs WHERE id = %s;".replace("?", o)
		return self.__fetch(stmt, (id,))
		
	# Pull a list of every job and its title
	def getAllJobs(self):
		self.cur.execute("SELECT id, title FROM jobs;")
		return self.cur.fetchall();
		
	###################################################
	#           USER/SAVE RELATED FUNCTIONS           #
	###################################################
	
	# See if user has job saved, returns 0 if no
	# Please make sure isSaved is 1 before executing anything else
	def isSaved(self, id, jobid):
		stmt = "SELECT EXISTS(SELECT * FROM saved WHERE uid = %s AND jid = %s);"
		return self.__fetch(stmt, (id, jobid))
		
	# Save a job to a user
	def saveJob(self, id, jobid):
		stmt = "INSERT IGNORE INTO saved (uid, jid) VALUES (%s, %s);"
		self.__execute(stmt, (id, jobid))
	
	# Count number of jobs user has saved
	def countJobs(self, id):
		stmt = "SELECT COUNT(uid) FROM saved WHERE uid = %s;"
		return self.__fetch(stmt, (id,))
		
	# Count number of jobs user has applied to
	def countJobsAppled(self, id):
		stmt = "SELECT COUNT(uid) FROM saved WHERE uid = %s AND applied = 1;"
		return self.__fetch(stmt, (id,))
		
	# Count number of users who have applied to a job
	def countUsersApplied(self, jobid):
		stmt = "SELECT COUNT(jid) FROM saved WHERE jid = %s AND applied = 1;"
		return self.__fetch(stmt, (jobid,))
		
	# Get info about a saved job. Options: applied, note
	def getSavedInfo(self, id, jobid, o):
		stmt = "SELECT ? FROM saved WHERE uid = %s AND jid = %s;".replace("?", o)
		return self.__fetch(stmt, (id, jobid))
		
	# Save a new user note
	def saveNote(self, id, jobid, note):
		stmt = "UPDATE saved SET notes = %s WHERE uid = %s AND jid = %s;"
		self.__execute(stmt, (note, id, jobid))
		
	# Apply to a job
	def applyTo(self, id, jobid):
		stmt = "UPDATE saved SET applied = 1 WHERE uid = %s AND jid = %s;"
		self.__execute(stmt, (id, jobid))
		
	###################################################
	#                UTILITY + PRIVATE                #
	###################################################
        
	# Should be called when program exits
	def close(self):
		self.cur.close()
		self.cnx.close()
		
	# Private function to execute table-modifying statements
	def __execute(self, stmt, info):
		self.cur.execute(stmt, info)
		self.cnx.commit()
		
	# Private function to make fetching single data pieces easier
	def __fetch(self, stmt, info):
		self.cur.execute(stmt, info)
		return self.cur.fetchone()[0]