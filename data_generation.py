import csv
import json

from datetime import datetime
from faker import Faker

from pythonwrapper.iterable_wrapper import IterableApi

#load some of my test json data for easy testing
commerce_data = json.load(open('json_data/shopping_cart.json'))
purchase_data = json.load(open('json_data/track_purchase.json'))
event_data = json.load(open('json_data/events.json'))

#list of different events to fake into Iterable instance.  Will be chosen at random
events= ['login', 'downloaded_whitepaper', 'user_signup', 'event_registration',
		'free_trial_download', 'downloaded_mobile_app', 'uploaded_profile_photo',
		]


# Iterable Instance Credentials
API_KEY = "94c3333a8e224b32b93a40788d1927cc"


class DataGeneration(IterableApi):
	'''
	docstring for DataGeneration
	'''
	def __init__(self, users=0, events=0):
		
		IterableApi.__init__(self, api_key=API_KEY)
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

		return self.track_event(email=event_data["email"],
								event_name=event_data["eventName"],
								created_at=event_data["createdAt"],
								data_fields=event_data["dataFields"])


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


	def generate_items_in_cart(self):

		return self.update_cart(user=commerce_data["user"],
							    items=commerce_data["items"])

		

	def generate_puchase_requests(self):

		return self.track_purchase(user=purchase_data["user"],
								   items=purchase_data["items"],
								   total=purchase_data["total"],
								   created_at=purchase_data["createdAt"])
	        

	

data= DataGeneration()

#print(data.generate_users())

# print(data.generate_users())

# print(data.delete_users_from_csv(csv_file='path/tofile/here'))

# data.generate_items_in_cart()

data.generate_puchase_requests()

# data.generate_events()






