
from config import (HOST, USER_NAME, PASSWORD, DATABASE)
from sqlalchemy import create_engine


class DbConnector:
	def __init__(self):
		self.engine = create_engine('mysql://'+str(USER_NAME)+":"+str(PASSWORD)+"@"+HOST+":3306/trackers", echo=False, pool_size=50, max_overflow=2)
		#self.Session = sessionmaker(bind=engine)
		
		
	def get_connection(self):
		return self.engine.connect()









		
	

