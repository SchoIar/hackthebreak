import os
from SQLManager import SQLManager

if __name__ == "__main__":
	sql = SQLManager()
	sql.newUser("test1", "test2")
	print(sql.userExists("test1"))
	print(sql.userExists("test2"))
	print(sql.getUserInfo("test1", "xp"))
	sql.addXp("test1", 100)
	sql.removeStreak("test1")
	sql.newJob(1111, "https://github.com", "Githubber", "Github")
	sql.newJob(1112, "https://youtube.com", "Youtuber", "Hell")
	print(sql.getAllJobs())
	sql.close()