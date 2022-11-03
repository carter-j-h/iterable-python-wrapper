import csv
import json
import pdb
import requests
import time

from datetime import datetime


class IterableApi():
	"""
	This is a python wrapper for the Iterable API

	We are using the 'Requests' HTTP python library, which I 
	have found very flexible to accomodate the various methods
	that customers leverage to interact with our API.  'Requests' 
	documentation is also excellent, enabling our team to 
	quickly update this wrapper to support a wide range of use cases.  

	"""	

	def __init__(self, api_key):
		"""
		This preforms the necessary initialization parameters for the
		Iterable API wrapper. It stores the base URI, the API key for the 
		project, and headers that shoudl be consistent across all requests. 

		"""
		self.api_key = api_key
		self.base_uri = "https://api.iterable.com"
		self.headers = {
						"Content-type": "application/json",
						"Api-Key": self.api_key
						}		

	def api_call(self, call, method, params=None, headers=None, data=None,
				 json=None):
		"""
		This is our generic api call function.  We will route all calls except
		requests that do not return JSON ('Export' and 'Experiment Metrics' are
		examples where this is the case).  This is beneficial because:
			1. Allows for easier debugging if a request fails
			2. Currently, Iterable only needs the API key from a security
			standpoint. In the future, if it were to require an  
			access token for each request we could easily manage the granting
			and expiration management of such a token.  

		"""

		# params(optional) Dictionary or bytes to be sent in the query string for the Request.
		if params is None:
			params = {}
		# data- dict or list of tuples to be sent in body of Request
		if data is None:
			data = {}
		# json- data to be sent in body of Request
		if json is None:
			json ={}

		# make the request following the 'requests.request' method
		r = requests.request(method=method, url=self.base_uri+call, params=params,
							 headers=self.headers, data=data, json=json)	

		response = {			
			"body": r.json(),			
			"code": r.status_code,
			"headers": r.headers,
			"url": r.url
		}

		return response

	def export_data_api(self, call,
						params, path, 
						chunk_size=None, 
						return_response_object=None):

		r = requests.request(method="GET", url=self.base_uri+call, params=params,
							 headers=self.headers, stream=True)

		if r.status_code == 200:
			
			if return_response_object is (not None and True):

				return r


			if "csv" in r.url:
				local_filename = 'iterable_' + params['dataTypeName'] + str(round(time.time())) + '.csv'
			if "experiments" in r.url:
				local_filename = 'iterable_experiment_ids_' + str(",".join(list(params.values()))) + "_" + str(round(time.time())) + '.csv'
			if "userEvents" in r.url:
				local_filename = 'iterable_user_events' + str(round(time.time())) + '.csv'
			if "json" in r.url:
				local_filename = 'iterable_' + params['dataTypeName'] + str(round(time.time())) + '.json'

			with open(path+local_filename, 'wb') as write_file:
				
				for chunk in r.iter_content(chunk_size=chunk_size):
					if chunk:
						write_file.write(chunk)
			
			return True

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	Iterable Campaign Requests

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	def list_campaign_metadata(self):

		call="/api/campaigns"

		return self.api_call(call=call, method="GET")

	def create_campaign(self, name, list_ids, template_id,
						suppression_list_ids=None, send_at=None,
						send_mode=None, start_time_zone=None,
						default_time_zone=None, data_fields=None):

		call = "/api/campaigns/create"

		payload ={}

		payload["name"]= str(name)

		if isinstance(list_ids, list):
			payload["listIds"]= list_ids

		else:
			raise TypeError('ListIds are not in the required Array format')

		payload["templateId"]= template_id

		if suppression_list_ids is not None:
			payload["supressionListIds"]= suppression_list_ids

		if send_at is not None:
			payload["sendAt"]= str(send_at)

		if send_mode is not None:
			payload["sendMode"]= str(send_mode)

		if start_time_zone is not None:
			payload["startTimeZone"]= str(start_time_zone)

		if default_time_zone is not None:
			payload["defaultTimeZone"]= str(default_time_zone)

		if data_fields is not None:
			payload["dataFields"]= data_fields

		return self.api_call(call=call, method="POST", json=payload)

	def get_campaign_metrics(self, campaign_id, start_date_time=None,
							 end_date_time=None, use_new_format=None):

		call= "/api/campaigns/metrics"

		payload ={}

		if isinstance(campaign_id, list):
			if len(campaign_id)>=1:
				payload["campaignId"]= campaign_id
			else:
				raise ValueError('You need to pass in at least 1 campaign id')
		else:
			raise TypeError('campaign ids are not stored in list format')

		if isinstance(start_date_time, datetime.datetime):			
			payload["startDateTime"]= start_date_time
		else:
			raise TypeError('Start date is in incorrect format')

		if isinstance(end_date_time, datetime.datetime):
			
			payload["endDateTime"]= end_date_time
		else:
			raise TypeError('End date is in incorrect format')

		if use_new_format is not None:
			payload["useNewFormat"]= use_new_format

		return self.api_call(call=call, method="GET", params=payload)

	def get_child_campaigns(self, campaign_id):

		call = "/api/campaigns/recurring/"+str(campaign_id)+"/childCampaigns"

		return self.api_call(call=call, method="GET")

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	Iterable Channel Requests


	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	def get_channels(self):

		call="/api/channels"

		return self.api_call(call=call, method="GET")

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	Iterable Commerce Reqeusts

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	def track_purchase(self, user, items, total, purchase_id= None, campaign_id=None, 
					   template_id=None, created_at=None,
					   data_fields=None):
		"""
			The 'purchase_id' argument maps to 'id' for this API endpoint.
			This name is used to distinguish it from other instances where
			'id' is a part of the API request with other Iterable endpoints.
		"""

		call="/api/commerce/trackPurchase"

		payload ={}
	
		if isinstance(user, dict):
			payload["user"]= user
		else:
			raise TypeError('user key is not in Dictionary format')

		if isinstance(items, list):
			payload["items"]= items
		else:
			raise TypeError('items are not in Array format')

		if isinstance(total, float):
			payload["total"]= total
		else:
			raise TypeError('total is not in correct format')

		if purchase_id is not None:
			payload["id"]= str(purchase_id) 

		if campaign_id is not None:
			payload["campaignId"]= campaign_id

		if template_id is not None:
			payload["templateId"]= template_id		

		if created_at is not None:
			payload["createdAt"]= created_at

		if data_fields is not None:
			payload["dataFields"]= data_fields

		return self.api_call(call=call, method="POST", json=payload)

	def update_cart(self, user=None, items=None):

		call="/api/commerce/updateCart"

		payload ={}

		if isinstance(user, dict):
			payload["user"]= user
		else:
			raise Exception('user is not in Dictionary format')

		if isinstance(items, list):
			payload["items"]= items
		else:
			raise Exception('items are not in Array format')

		return self.api_call(call=call, method="POST", json=payload)

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	Iterable Email Requests

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	def send_email(self, campaign_id, recipient_email,
				   message_medium, data_fields=None,
				   send_at=None, allow_repeat_marketing_sends=None,
				   metadata=None):

		call="/api/email/target"

		payload ={}

		payload["campaignId"]= campaign_id

		payload["recipientEmail"]= str(recipient_email)

		if isinstance(message_medium, dict):
			payload["messageMedium"]= message_medium
		else:
			raise Exception('message medium is not in Dictionary format')

		if data_fields is not None:
			payload["dataFields"]= data_fields

		if send_at is not None:
			payload["sendAt"]= send_at

		if allow_repeat_marketing_sends is not None:
			payload["allowRepeatMarketingSends"]= allow_repeat_marketing_sends

		if metadata is not None:
			payload["metadata"]= metadata		

		return self.api_call(call=call, method="POST", json=payload)

	def view_email_in_browser(self, email, message_id):

		call = "/api/email/viewInBrowser"

		payload ={}

		payload["email"]= str(email)

		payload["messageId"]= str(message_id)

		return self.api_call(call=call, method="GET", params=payload)

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

		Iterable Event Requests

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	def get_events(self, email, limit=None):

		call="/api/events/"+str(email)

		payload={}

		if limit is not None and limit <= 200:
			payload["limit"]= limit

		return self.api_call(call=call, method="GET", params=payload)

	def consume_in_app_notification(self, message_id, email=None,
									user_id=None, button_index=None):

		call = "/api/events/inAppConsume"

		payload ={}

		payload["messageId"]= str(message_id)

		if email is not None:
			payload["email"]=email

		if user_id is not None:
			payload["userId"]=user_id

		if button_index is not None:
			payload["buttonIndex"]= button_index

		return self.api_call(call=call, method="POST", json=payload)

	def track_event(self, event_name, event_id=None, email=None, 
					created_at=None, data_fields=None, user_id=None,
					campaign_id=None,template_id=None):

		call="/api/events/track"

		payload={}

		payload["eventName"]= str(event_name)

		if event_id is not None:
			payload["id"]= str(event_id)

		if email is not None:
			payload["email"]=email

		if created_at is not None:
			payload["createdAt"]=created_at

		if data_fields is not None:
			payload["dataFields"]= data_fields

		if user_id is not None:
			payload["userId"]=user_id

		if campaign_id is not None:
			payload["campaignId"]= campaign_id

		if template_id is not None:
			payload["templateId"]= template_id

		return self.api_call(call=call, method="POST", json=payload)

	def track_in_app_click(self, message_id, email=None,
						   user_id=None, button_index=None):

		call="/api/events/trackInAppClick"

		payload={}

		payload["messageId"]= str(message_id)

		if email is not None:
			payload["email"]= email

		if user_id is not None:
			payload["userId"]=user_id

		if button_index is not None:
			payload["buttonIndex"]=button_index

		return self.api_call(call=call, method="POST", json=payload)

	def track_in_app_open(self, message_id, email=None,
						  user_id=None, button_index=None):

		call="/api/events/trackInAppOpen"

		payload={}

		payload["messageId"]=str(message_id)

		if email is not None:
			payload["email"]= email

		if user_id is not None:
			payload["userId"]=user_id

		if button_index is not None:
			payload["buttonIndex"]=button_index

		return self.api_call(call=call, method="POST", json=payload)

	def track_push_open(self, campaign_id, email=None, user_id=None,
						template_id=None, message_id=None, created_at=None,
						data_fields=None):

		call="/api/events/trackPushOpen"

		payload={}

		payload["CampaignId"]= campaign_id

		if email is not None:
			payload["email"]=email

		if user_id is not None:
			payload["userId"]=user_id

		if template_id is not None:
			payload["templateId"]=template_id

		if message_id is not None:
			payload["messageId"]=message_id

		if created_at is not None:
			payload["createdAt"]= created_at

		if data_fields is not None:
			payload["dataFields"]=data_fields

		return self.api_call(call=call, method="POST", json=payload)

	def track_web_push_click(self, email=None, user_id=None,
							 message_id=None, campaign_id=None,
							 template_id=None):

		call ="/api/events/trackWebPushClick" 

		payload={}

		payload["messageId"]=str(message_id)

		if email is not None:
			payload["email"]=email

		if user_id is not None:
			payload["userId"]=user_id

		if campaign_id is not None:
			payload["campaignId"]=campaign_id

		if template_id is not None:
			payload["templateId"]=template_id

		return self.api_call(call=call, method="POST", json=payload)

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
		
	Iterable Experiment Requests

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	def get_experiment_metrics(self, path, return_response_object= None,
							   experiment_id=None, campaign_id=None,
							   start_date_time=None, end_date_time=None
							   ):
		"""
			This endpoint doesn't return a JSON object, instead it returns
			a series of rows, each its own object. Given this setup, it makes 
			sense to treat it how we handle our Bulk Export reqeusts.

			Arguments:

			path: the directory on your computer you wish the file to be downloaded into.
			
			return_response_object: recommended to be set to 'False'.  If set to 'True', 
			will just return the response object as defined by the 'python-requests' module.
			"""

		call="/api/experiments/metrics"

		if isinstance(return_response_object, bool) is False:
			raise ValueError("'return_iterator_object'parameter must be a boolean") 

		payload={}

		if experiment_id is not None:
			payload["experimentId"]=experiment_id

		if campaign_id is not None:
			payload["campaignId"]=campaign_id

		if start_date_time is not None:
			payload["startDateTime"]=start_date_time

		if end_date_time is not None:
			payload["endDateTime"]=end_date_time

		return self.export_data_api(call=call, path=path, params=payload)

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
	
	Export Requests

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	def export_data_csv(self, data_type_name=None, date_range=None,
						delimiter=None, start_date_time=None,
						end_date_time=None, omit_fields=None,
						only_fields=None, campaign_id=None,
						path=None):

		call="/api/export/data.csv"

		payload={}

		if data_type_name is not None:
			payload["dataTypeName"]= data_type_name

		if date_range is not None:
			payload["range"]= date_range

		if delimiter is not None:
			payload["delimiter"]= delimiter

		if start_date_time is not None:
			payload["startDateTime"]= start_date_time

		if end_date_time is not None:
			payload["endDateTime"]= end_date_time

		if omit_fields is not None:
			payload["omitFields"]= omit_fields

		if only_fields is not None and isinstance(only_fields, list):
			payload["onlyFields"]= only_fields

		if campaign_id is not None:
			payload["campaignId"]= campaign_id

		return self.export_data_api(call=call, params=payload, path=path)

	def export_data_json(self, return_response_object, 
						chunk_size=1024, 
						path=None,
						data_type_name=None, date_range=None,
						delimiter=None, start_date_time=None,
						end_date_time=None, omit_fields=None,
						only_fields=None, campaign_id=None):

		"""
		Custom Keyword arguments:

		1. return_response_object:
			if set to 'True', the 'r' response object will be returned.  The
			benefit of this is that you can manipulate the data in any way you
			want.  If set to false, we will write the response to a file where each
			Iterable activity you're exporting is a single-line JSON object.
		2. chunk_size:
			Chunk size is used as a paremeter in the r.iter_content(chunk_size) method
			that controls how big the response chunks are (in bytes).  Depending on the
			device used to make the request, this might change depending on the user. 
			Default is set to 1 MB. 
		3. path:
			Allows you to choose the directory where the file is downloaded into.
				Example: "/Users/username/Desktop/"
			If not set the file will download into the current directory.
			
		"""
		call="/api/export/data.json"

		# make sure correct ranges are being used
		date_ranges = ["Today", "Yesterday", "BeforeToday", "All"]		
		
		if isinstance(return_response_object, bool) is False:
			raise ValueError("'return_iterator_object'parameter must be a boolean") 
		
		if chunk_size is not None and isinstance(chunk_size, int):
			pass
		else:
			raise ValueError("'chunk_size' parameter must be a integer")

		payload={}

		if data_type_name is not None:
			payload["dataTypeName"]= data_type_name

		if date_range is not None and date_range in date_ranges:
			payload["range"]= date_range

		if start_date_time is not None:
			payload["startDateTime"]= start_date_time

		if end_date_time is not None:
			payload["endDateTime"]= end_date_time

		if omit_fields is not None:
			payload["omitFields"]= omit_fields

		if only_fields is not None and isinstance(only_fields, list):
			payload["onlyFields"]= only_fields

		if campaign_id is not None:
			payload["campaignId"]= campaign_id

		return self.export_data_api(call=call, chunk_size=chunk_size, 
									params=payload, path=path,
									return_response_object=return_response_object)


	def export_user_events(self, email, include_custom_events,
						   path, return_response_object= None):

		call ="/api/export/userEvents"

		if isinstance(include_custom_events, bool) is False:
			raise ValueError("'include_custom_events' parameter must be a boolean")

		payload = {}

		payload["email"]= str(email)

		payload["includeCustomEvents"] = include_custom_events

		return self.export_data_api(call=call, params=payload, path=path)

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
	
	Iterable inApp Requests

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	def get_in_app_messages(self, email, count, user_id=None,
							platform=None, sdk_version=None):

		call = "/api/inApp/getMessages"

		payload={}

		payload["email"]=str(email)

		payload["count"]= count

		if user_id is not None:
			payload["userId"]=str(user_id)	

		if platform is not None:
			payload["platform"]=str(platform)

		if sdk_version is not None:
			payload["SDKVersion"]= sdk_version

		return self.api_call(call=call, method="GET", params=payload)

	def send_in_app_notification(self, campaign_id, recipient_email,
								 message_medium, data_fields=None,
								 send_at=None,								 
								 allow_repeat_marketing_sends=None):

		call="/api/inApp/target"

		payload={}

		payload["campaignId"]=campaign_id

		payload["recipientEmail"]=recipient_email

		if isinstance(message_medium, dict):
			payload["messageMedium"]= message_medium
		else:
			raise Exception('message medium is not in Dictionary format')

		if data_fields is not None:
			payload["dataFields"]=data_fields

		if send_at is not None:
			payload["sendAt"]=send_at

		if allow_repeat_marketing_sends is not None:
			payload["allowRepeatMarketingSends"]= allow_repeat_marketing_sends

		return self.api_call(call=call, method="POST", json=payload)

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
		
		Iterable List requests


	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	def get_lists(self):

		call = "/api/lists"

		return self.api_call(call=call, method="GET")

	def create_static_list(self, list_name):

		call = "/api/lists"

		payload ={}

		payload["name"]= str(list_name)

		return self.api_call(call=call, method="POST", json=payload)

	def delete_static_list(self, list_id):

		call = "/api/lists/"+str(list_id)

		return self.api_call(call=call, method="DELETE")

	def count_of_users_in_list(self, list_id):

		call = "/api/lists/"+str(list_id)+"/size"

		return self.api_call(call=call, method="GET")

	def get_users_in_list(self, list_id):

		call = "/api/lists/getUsers"

		payload ={}

		payload["listId"]= list_id

		return self.api_call(call=call, method="GET", params=payload)

	def add_subscribers_to_list(self, list_id, subscribers):

		call = "/api/lists/subscribe"

		payload = {}

		payload["listId"]= list_id

		if isinstance(subscribers, list):
			payload["subscribers"]= subscribers

		else:
			raise TypeError('subscribers are not stored in list format')

		return self.api_call(call=call, method="POST", json=payload)

	def remove_subscribers_to_list(self, list_id, subscribers,
								   campaign_id=None, channel_unsubscribe=False):

		call = "/api/lists/unsubscribe"

		payload = {}

		payload["listId"]= list_id

		if isinstance(subscribers, list):
			payload["subscribers"]= subscribers

		else:
			raise TypeError('subscribers are not stored in list format')

		if campaign_id is not None:
			payload["campaignId"]= campaign_id

		if channel_unsubscribe is not None:
			payload["channelUnsubscribe"]= channel_unsubscribe

		return self.api_call(call=call, method="POST", json=payload)

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
	
	Iterable MessageType Requests


	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	def list_message_types(self):

		call="/api/messageTypes"

		return self.api_call(call=call, method="GET")

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	Iterable Metadata Requests


	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
	
	def list_available_tables(self):

		call="/api/metadata"

		return self.api_call(call=call, method="GET")

	def delete_all_metadata_from_table(self, table):

		call="/api/metadata"+str(table)

		return self.api_call(call=call, method="DELETE")

	def list_keys_in_table(self, table, next_marker=None):

		call= "/api/metadata/"+str(table)

		payload ={}

		if next_marker is not None:
			payload["nextMarket"]=next_marker

		return self.api_call(call=call, method="GET", params=payload)

	def delete_single_metadata_key_value(self, table, key):
		
		call="/api/metadata/"+ str(table) + "/" + str(key)

		return self.api_call(call=call, method="DELETE")

	def get_single_metadata_key_value(self, table, key):

		call="/api/metadata/"+ str(table) + "/" + str(key)

		return self.api_call(call=call, method="GET")

	def create_or_replace_metadata(self, table, key, value):

		call="/api/metadata/"+ str(table) + "/" + str(key)

		payload={}

		if isinstance(value, dict):
			payload["value"]= value
		else:
			raise TypeError('value is not in object format')

		return self.api_call(call=call, method="PUT", json=payload)

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	Iterable Push Requests

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	def send_push_notification(self, campaign_id, recipient_email, 
							   message_medium, data_fields=None,
							   send_at=None, 
							   allow_repeat_marketing_sends=None,
							   metadata=None):

		call="/api/push/target"

		payload={}

		payload["campaignId"]= campaign_id

		payload["recipientEmail"]= recipient_email

		if isinstance(message_medium, dict):
			payload["messageMedium"]= message_medium
		else:
			raise Exception('message medium is not in Dictionary format')

		if data_fields is not None:
			payload["dataFields"]= data_fields

		if send_at is not None:
			payload["sendAt"]= send_at

		if allow_repeat_marketing_sends is not None:
			payload["allowRepeatMarketingSends"]= allow_repeat_marketing_sends

		if metadata is not None:
			payload["metadata"]= metadata

		return self.api_call(call=call, method="POST", json=payload)

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	Iterable SMS Requests

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	def send_sms_message(self, campaign_id, recipient_email, 
					     message_medium, data_fields=None,
					     send_at=None, 
					     allow_repeat_marketing_sends=None,
					     ):

		call="/api/sms/target"

		payload={}

		payload["campaignId"]= campaign_id

		payload["recipientEmail"]= recipient_email

		if isinstance(message_medium, dict):
			payload["messageMedium"]= message_medium
		else:
			raise Exception('message medium is not in Dictionary format')

		if data_fields is not None:
			payload["dataFields"]= data_fields

		if send_at is not None:
			payload["sendAt"]= send_at

		if allow_repeat_marketing_sends is not None:
			payload["allowRepeatMarketingSends"]= allow_repeat_marketing_sends		

		return self.api_call(call=call, method="POST", json=payload) 

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	Iterable Template Requests

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	def get_templates(self, template_type=None, 
								  message_medium=None,
								  start_date_time=None,
								  end_date_time=None):

		call="/api/templates"

		payload={}

		iterable_template_types = ["Base", "Blast", "Triggered", "Workflow"]

		iterable_message_mediums = ["Email", "Push", "InApp", "SMS"]

		if template_type is not None and template_type in iterable_template_types:			
			payload["templateType"]= template_type

		elif template_type is not None and template_type not in iterable_template_types:
			raise Exception("It looks like you listed an incorrect template type '%s'" % template_type)	

		if message_medium is not None and message_medium in iterable_message_mediums:			
			payload["messageMedium"]= message_medium		

		elif message_medium is not None and message_medium not in iterable_message_mediums:
			raise Exception("It looks like you listed an incorrect message medium '%s'" % message_medium)
			
		if start_date_time is not None:
			payload["startDateTime"]= start_date_time

		if end_date_time is not None:
			payload["endDateTime"]= end_date_time

		return self.api_call(call = call, method = "GET", params = payload)

	def get_email_template_by_templateId(self, template_id, locale=None):

		call="/api/templates/email/get"

		payload={}

		payload["templateId"]=template_id

		if locale is not None:
			payload["locale"]= locale

		return self.api_call(call=call, method="GET", params=payload)

	def update_email_template(self, template_id, metadata=None,
							  name=None, from_name=None, from_email=None,
							  reply_to_email=None, subject=None,
							  preheader_text=None, cc_emails=None,
							  bcc_emails=None, html=None,
							  plain_text=None,
							  google_analytics_campaign_name=None,
							  link_parameters=None, data_feed_id=None,
							  cache_data_feed=None,
							  merge_data_feed_context=None,
							  client_template_id=None, locale=None,
							  message_type_id=None, creator_user_id=None):

		call="/api/templates/email/update"

		payload={}

		payload["templateId"]= template_id

		if metadata is not None:
			payload["metadata"]= metadata

		if name is not None:
			payload["name"]= name

		if from_name is not None:
			payload["fromName"]= from_name

		if from_email is not None:
			payload["fromEmail"]= from_email

		if reply_to_email is not None:
			payload["replyToEmail"]= reply_to_email

		if subject is not None:
			payload["subject"]= subject

		if preheader_text is not None:
			payload["preheaderText"]= preheader_text

		if cc_emails is not None:
			payload["ccEmails"]= cc_emails

		if bcc_emails is not None:
			payload["bccEmails"]= bcc_emails

		if html is not None:
			payload["html"]= html

		if plain_text is not None:
			payload["planText"]= plain_text

		if google_analytics_campaign_name is not None:
			payload["googleAnalyticsCampaignName"]= google_analytics_campaign_name

		if link_parameters is not None:
			payload["linkParams"]= link_parameters

		if data_feed_id is not None:
			payload["dataFeedId"]= data_feed_id

		if cache_data_feed is not None:
			payload["cacheDataFeed"]= cache_data_feed

		if merge_data_feed_context is not None:
			payload["mergeDataFeedContext"]= merge_data_feed_context

		if client_template_id is not None:
			payload["clientTemplateId"]= client_template_id

		if locale is not None:
			payload["locale"]= locale

		if message_type_id is not None:
			payload["messageTypeId"]= message_type_id

		if creator_user_id is not None:
			payload["creatorUserId"]= creator_user_id

		return self.api_call(call=call, method="POST", json=payload)

	def upsert_email_template(self, client_template_id,
							  name=None, from_name=None, from_email=None,
							  reply_to_email=None, subject=None,
							  preheader_text=None, cc_emails=None,
							  bcc_emails=None, html=None,
							  plain_text=None,
							  google_analytics_campaign_name=None,
							  link_parameters=None, data_feed_id=None,
							  cache_data_feed=None,
							  merge_data_feed_context=None,
							  locale=None,
							  message_type_id=None, creator_user_id=None):

		call="/api/templates/email/upsert"

		payload={}

		payload["clientTemplateId"]= str(client_template_id)

		if name is not None:
			payload["name"]= name

		if from_name is not None:
			payload["fromName"]= from_name

		if from_email is not None:
			payload["fromEmail"]= from_email

		if reply_to_email is not None:
			payload["replyToEmail"]= reply_to_email

		if subject is not None:
			payload["subject"]= subject

		if preheader_text is not None:
			payload["preheaderText"]= preheader_text

		if cc_emails is not None:
			payload["ccEmails"]= cc_emails

		if bcc_emails is not None:
			payload["bccEmails"]= bcc_emails

		if html is not None:
			payload["html"]= html

		if plain_text is not None:
			payload["planText"]= plain_text

		if google_analytics_campaign_name is not None:
			payload["googleAnalyticsCampaignName"]= google_analytics_campaign_name

		if link_parameters is not None:
			payload["linkParams"]= link_parameters

		if data_feed_id is not None:
			payload["dataFeedId"]= data_feed_id

		if cache_data_feed is not None:
			payload["cacheDataFeed"]= cache_data_feed

		if merge_data_feed_context is not None:
			payload["mergeDataFeedContext"]= merge_data_feed_context

		if locale is not None:
			payload["locale"]= locale

		if message_type_id is not None:
			payload["messageTypeId"]= message_type_id

		if creator_user_id is not None:
			payload["creatorUserId"]= creator_user_id

		return self.api_call(call=call, method="POST", json=payload)

	def get_email_template_by_client_templateId(self, client_template_id):

		call="/api/templates/getClientTemplateId"

		payload={}

		payload["clientTemplateId"]= client_template_id

		return self.api_call(call=call, method="GET", params=payload)

	def get_push_template(self, template_id, locale=None):

		call="/api/templates/push/get"

		payload={}

		payload["templateId"]= template_id

		if locale is not None:
			payload["locale"]= locale

		return self.api_call(call=call, method="GET", params=payload)

	def update_push_template(self, template_id, created_at=None,
							 updated_at=None, name=None, message=None,
							 payload_content=None, badge=None, locale=None,
							 message_type_id=None, sound=None,
							 deeplink=None, client_template_id=None,
							 campaign_id=None):

		call="/api/templates/push/update"

		payload = {}

		payload["templateId"]= template_id

		if created_at is not None:
			payload["createdAt"]= created_at

		if updated_at is not None:
			payload["updatedAt"]= updated_at

		if name is not None:
			payload["name"]= name

		if message is not None:
			payload["message"]= message

		if payload_content is not None:
			payload["payload"]= payload_content

		if badge is not None:
			payload["badge"]= badge

		if locale is not None:
			payload["locale"]= locale

		if message_type_id is not None:
			payload["messageTypeId"]= message_type_id

		if sound is not None:
			payload["sound"]= sound

		if deeplink is not None:
			payload["deeplink"]= deeplink

		if client_template_id is not None:
			payload["clientTemplateId"]= client_template_id

		if campaign_id is not None:
			payload["campaignId"]= campaign_id

		return self.api_call(call=call, method="POST", json=payload)

	def upsert_push_template(self, client_template_id, name=None,
							 message=None, payload_content=None, 
							 badge=None, locale=None,
							 message_type_id=None, sound=None,
							 deeplink=None, campaign_id=None):

		call="/api/templates/push/upsert"

		payload = {}

		payload["clientTemplateId"]= client_template_id

		if name is not None:
			payload["name"]= name

		if message is not None:
			payload["message"]= message

		if payload_content is not None:
			payload["payload"]= payload_content

		if badge is not None:
			payload["badge"]= badge

		if locale is not None:
			payload["locale"]= locale

		if message_type_id is not None:
			payload["messageTypeId"]= message_type_id

		if sound is not None:
			payload["sound"]= sound

		if deeplink is not None:
			payload["deeplink"]= deeplink

		if campaign_id is not None:
			payload["campaignId"]= campaign_id

		return self.api_call(call=call, method="POST", json=payload)

	def get_sms_template(self, template_id, locale=None):

		call="/api/templates/sms/get"

		payload={}

		payload["templateId"]= template_id

		if locale is not None:
			payload["locale"]= locale

		return self.api_call(call=call, method="GET", params=payload)

	def update_sms_template(self, template_id, created_at=None,
							updated_at=None, name=None, message=None,
							locale=None, message_type_id=None,
							image_url=None, client_template_id=None,
							campaign_id=None):

		call="/api/templates/sms/update"

		payload= {}

		payload["templateId"]= template_id

		if created_at is not None:
			payload["createdAt"]= created_at

		if updated_at is not None:
			payload["updatedAt"]= updated_at

		if name is not None:
			payload["name"]= name

		if message is not None:
			payload["message"]= message

		if locale is not None:
			payload["locale"]= locale

		if message_type_id is not None:
			payload["messageTypeId"]= message_type_id

		if image_url is not None:
			payload["imageUrl"]= image_url

		if client_template_id is not None:
			payload["clientTemplateId"]= client_template_id

		if campaign_id is not None:
			payload["campaignId"]= campaign_id

		return self.api_call(call=call, method="POST", json=payload)

	def upsert_sms_template(self, client_template_id,
							name=None, message=None, locale=None,
							message_type_id=None, image_url=None,
							campaign_id=None):

		call="/api/templates/sms/upsert"

		payload= {}

		payload["clientTemplateId"]= client_template_id

		if name is not None:
			payload["name"]= name

		if message is not None:
			payload["message"]= message

		if locale is not None:
			payload["locale"]= locale

		if message_type_id is not None:
			payload["messageTypeId"]= message_type_id

		if image_url is not None:
			payload["imageUrl"]= image_url

		if campaign_id is not None:
			payload["campaignId"]= campaign_id

		return self.api_call(call=call, method="POST", json=payload)			

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	Iterable User Requests


	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	def delete_user_by_email(self, email):
	
		"""
		This call will delete a user from the Iterable database.  
		This call requires a path parameter to be passed in, 'email'
		in this case, which is why we're just adding this to the 'call'
		argument that goes into the 'api_call' request. 		
		"""
		call = "/api/users/"+ str(email)

		return self.api_call(call=call, method="DELETE")

	def get_user_by_email(self, email):
		"""This function gets a user's data field and info"""

		call = "/api/users/"+ str(email)

		return self.api_call(call=call, method="GET")

	def bulk_update_user(self, users):

		"""
		The Iterable 'Bulk User Update' api Bulk update user data or adds 
		it if does not exist. Data is merged - missing fields are not deleted

		The body of the request takes 1 keys:
			1. users -- in the form of an array -- which is the list of users
				that we're updating in sets of 50 users at a time, which is the 
				most that can be batched in a single request.  
		"""

		call = "/api/users/bulkUpdate"		
		
		payload = {}

		if isinstance(users, list):
			payload["users"] = users
		else:
			raise TypeError ('users are not in Arrary format')		

		return self.api_call(call=call, method="POST", json=payload)

	def bulk_update_subscriptions(self, update_subscriptions_requests):

		call ="/api/users/bulkUpdateSubscriptions"

		payload = {}

		if isinstance(update_subscriptions_requests, list):
			payload["updateSubscriptionsRequests"] = update_subscriptions_requests
		else:
			raise TypeError ('subscription requests are not in Arrary format')	

		return self.api_call(call=call, method="POST", json=payload)

	def get_users_by_userid(self, user_id):

		call = "/api/users/byUserId"

		payload ={}

		payload["userId"] = str(user_id)

		return self.api_call(call=call, method="GET", params=payload)

	def delete_users_by_userid_userid(self, user_id):

		call = "/api/users/byUserId/"+str(user_id)			

		return self.api_call(call=call, method="DELETE")

	def get_users_by_userid_userid(self, user_id):

		call = "/api/users/byUserId/" + str(user_id)

		return self.api_call(call=call, method="GET")

	def disable_device(self, token, email=None, user_id=None):
		"""
		This request manually disable pushes to a device until it comes
		online again.

		"""

		call = "/api/users/disableDevice"

		payload ={}

		payload["token"] = str(token)

		if email is not None:	
			payload["email"] = str(email)

		if user_id is not None:
			payload["userId"] = str(user_id)

		return self.api_call(call= call, method="POST", json=payload)

	def get_user_by_email(self, email):

		call = "/api/users/getByEmail"

		payload = {}

		payload["email"]= str(email)

		return self.api_call(call=call, method="GET", params=payload)

	def get_user_fields(self):

		call = "api/users/getFields"

		return self.api_call(call=call, method="GET")

	def get_sent_messages(self, email=None, user_id=None, limit=10,
						  campaign_id=None, start_date_time=None,
						  end_date_time=None, exclude_blast_campaigns=None,
						  message_medium=None):

		call = "/api/users/getSentMessages"

		channels = ["Email", "Push", "InApp", "SMS"]

		payload ={}

		if email is not None:
			payload["email"] = str(email)

		if user_id is not None:
			payload["userId"]= str(user_id)

		if limit is not None and limit <=1000:
			payload["limit"]= int(limit)

		if campaign_id is not None:
			payload["campaignId"]= campaign_id

		if start_date_time is not None:
			payload["startDateTime"]= start_date_time

		if end_date_time is not None:
			payload["endDateTime"]= end_date_time

		if exclude_blast_campaigns is not None:
			payload["excludeBlastCampaigns"]= exclude_blast_campaigns

		if message_medium is not None and message_medium in channels:
			payload["messageMedium"]= str(message_medium)

		return self.api_call(call=call, method="GET", params=payload)

	def register_browser_token(self, browser_token, email=None,
							   user_id=None):

		call = "/api/users/registerBrowserToken"

		payload= {}

		payload["browserToken"] = str(browser_token)

		if email is not None:
			payload["email"]= email

		if user_id is not None:
			payload["userId"]= user_id

		return self.api_call(call=call, method="POST", json=payload)

	def register_device_token(self, device_token, email=None,
							  user_id=None):

		call = "/api/users/registerDeviceToken"

		payload = {}

		payload["device"] = device_token

		if email is not None:
			payload["email"]= email

		if user_id is not None:
			payload["userId"] = user_id

		return self.api_call(call=call, method="POST", json=payload)

	def update_user(self, email=None, data_fields=None, user_id=None,
					prefer_userId= None, merge_nested_objects=None):

		"""
		The Iterable 'User Update' api updates a user profile with new data 
		fields. Missing fields are not deleted and new data is merged.

		The body of the request takes 4 keys:
			1. email-- in the form of a string -- used as the unique identifier by
				the Iterable database.
			2. data fields-- in the form of an object-- these are the additional attributes
			 of the user that we want to add or update
			3. userId- in the form of a string-- another field we can use as a lookup
				of the user. 
			4. mergeNestedObjects-- in the form of an object-- used to merge top level
				objects instead of overwriting. 
		"""

		call = "/api/users/update"
		
		payload = {}

		if email is not None:
			payload["email"] = str(email)

		if data_fields is not None:
			payload["dataFields"] = data_fields

		if user_id is not None:
			payload["userId"] = str(user_id)

		if prefer_userId is not None:
			payload["preferUserId"]= prefer_userId

		if merge_nested_objects is not None:
			payload["mergeNestedObjects"] = merge_nested_objects
		
		return self.api_call(call=call, method="POST", json=payload)

	def update_email(self, new_email, current_email= None,
					 current_userid= None):

		call = "/api/users/updateEmail"

		payload = {}

		if current_email is not None:
			payload["currentEmail"] = str(current_email)

		if current_userid is not None:
			payload["currentUserId"] = str(current_userid)

		payload["newEmail"] = str(new_email)

		if ('currentEmail' or 'currentUserId') in payload == False:
			raise ValueError('You need to pass in either email or username into the function')

		return self.api_call(call=call, method="POST", json=payload)

	def update_subscriptions(self, email, email_list_ids=None,
							 unsubscribed_channel_ids=None,
							 unsubscribed_message_type_ids=None,
							 campaign_id=None, template_id=None):

		call="/api/users/updateSubscriptions"

		payload ={}

		payload["email"]= email

		if email_list_ids is not None:
			payload["emailListIds"]

		if unsubscribed_channel_ids is not None:
			payload["unsubscribedChannelIds"]= unsubscribed_channel_ids

		if unsubscribed_message_type_ids is not None:
			payload["unsubscribedMessageTypeIds"]= unsubscribed_message_type_ids

		if campaign_id is not None:
			payload["campaignId"] = campaign_id

		if template_id is not None:
			payload["templateId"]= template_id

		return self.api_call(call=call, method="POST", json=payload)

	def get_forgotten_users_in_complaince_with_gdpr(self):

		call= "/api/users/forgotten"

		return self.api_call(call=call, method="GET")

	def forget_a_user_in_compliance_with_gdpr(self, email):

		call= "/api/users/forget"

		payload ={}

		payload["email"]= email

		return self.api_call(call=call, method="POST", json=payload)

	def unforget_a_user_in_compliance_with_gdpr(self, email):

		call="/api/users/unforget"

		payload={}

		payload["email"]= email

		return self.api_call(call=call, method="POST", json=payload)

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	Iterable Web Push Requests

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	def send_web_push_notification(self, campaign_id, recipient_email,
								   message_medium, data_fields=None,
							       send_at=None, 
							       allow_repeat_marketing_sends=None):

		call="/api/webPush/target"

		payload={}

		payload["campaignId"]= campaign_id

		payload["recipientEmail"]= recipient_email

		if isinstance(message_medium, dict):
			payload["messageMedium"]= message_medium
		else:
			raise Exception('message medium is not in Dictionary format')

		if data_fields is not None:
			payload["dataFields"]= data_fields

		if send_at is not None:
			payload["sendAt"]= send_at

		if allow_repeat_marketing_sends is not None:
			payload["allowRepeatMarketingSends"]= allow_repeat_marketing_sends

		return self.api_call(call=call, method="POST", json=payload)

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	Iterable Workflow Requests

	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

	def trigger_workflow(self, workflow_id, email=None, 
						 data_fields=None, list_id=None):

		call="/api/workflows/triggerWorkflow"

		payload={}

		payload["workflowId"]= workflow_id

		if email is not None:
			payload["email"]= email

		if data_fields is not None:
			payload["dataFields"]=data_fields

		if list_id is not None:
			payload["listId"]= list_id

		return self.api_call(call=call, method="POST", json=payload)
