import os
from SQLManager import SQLManager

if __name__ == "__main__":
	sql = SQLManager()
	sql.saveJob("test1", 2911283352)
	sql.applyTo("test1", 2911283352) 
	sql.saveNote("test1", 2911283352, "Hello! I hate my job!") 
	sql.close()