import csv

from datetime import datetime
from faker import Faker

from iterable_wrapper import IterableAPI

# Iterable Instance Credentials
API_KEY = "94c3333a8e224b32b93a40788d1927cc"


class DataGeneration(IterableAPI):
	'''
	docstring for DataGeneration
	'''
	def __init__(self, users=0, events=0):
		
		IterableAPI.__init__(self, api_key=API_KEY)
		self.users = users
		self.events = events


	def generate_users(self):
		# initiate Faker
		fake=Faker()

		for i in range(0,self.users):
			i = fake.profile()

			email = str(i["mail"])

			i.pop("mail")
			i.pop("current_location")

		return self.update_user(email=email, data_fields=i, user_id=None, merge_nested_objects=None)

	def generate_events(self):

		return self.track_event(email="carter+test@iterable.com", event_name="login",
								created_at=str(datetime.now()),
								data_fields={"device": "Macbook Pro",
											 "location": "San Francisco, CA",
											  "website":"iterable"})


	def delete_users_from_csv(self, csv_file=None):

		"""
		This will delete each user based on their email address in the passed csv file.  
		The email field must be exactly formatted as 
		"""
		with open(csv_file) as csvfile:

			readCSV = csv.reader(csvfile, delimiter=',')

			# grab headers
			headers = next(readCSV, None)

			if "email" in headers:

				# find out which column emails are stored in
				index = headers.index("email")

				# ignore first row
				next(readCSV, None)

				for row in readCSV:			

					self.delete_user(email=str(row[index]))
	        

	

data= DataGeneration(users=1, events=1)

#print(data.generate_users())

# print(data.generate_users())

print(data.delete_users_from_csv(csv_file='path/tofile/here'))







