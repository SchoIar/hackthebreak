import os
from SQLManager import SQLManager

if __name__ == "__main__":
	sql = SQLManager()
	sql.newUser("Hello", "there")
	sql.close()