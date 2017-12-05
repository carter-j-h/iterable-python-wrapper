from unittest import mock 

import iterable_wrapper
# import iterable_wrapper

# init class so we can test wrapper effectiveness


# class WrapperTestCase(unittest.TestCase):
#     """Tests for `iterable_wrapper.py`."""    


#     def test_users_requests(self):
#         """Is api reqeust behaving correctly?"""
#         self.assertTrue(ic.api_call(call="/api/users/getByEmail", method="GET", params={"email": "carter@iterable.com"}))

# if __name__ == '__main__':
#     unittest.main()




# @mock.patch decorator passes a MagicMock object that replaces the class you are mocking into the function it is decorating.
@mock.patch("iterable_wrapper.IterableAPI")
def mock_IterableAPI(mock_class):
	print(mock_class)
	print(iterable_wrapper.IterableAPI)

	API_KEY= "94c3333a8e224b32b93a40788d1927cc"

	ic = iterable_wrapper.IterableAPI(api_key=API_KEY)
	print(ic)
	
	print(mock_class.return_value)

	mock_request = MockRequests()
	mock_request.status_code = 200
	mock_request.text = "{'channels': [{'channelType': 'Marketing', 'id': 9721, 'name': 'Push Marketing Channel', 'messageMedium': 'Push'}, {'channelType': 'Transactional', 'id': 9720, 'name': 'Transactional Channel', 'messageMedium': 'Email'}, {'channelType': 'Marketing', 'id': 9719, 'name': 'Marketing Channel', 'messageMedium': 'Email'}]}"
	response = ic.list_channels()
	self.assertTrue(response.status_code == 200)




mock_IterableAPI()


# def use_wrapper():
# 	ic = IterableAPI(api_key=API_KEY)
# 	print(ic.list_channels())

# use_wrapper()


# class APITest(unittest.TestCase):
#     @mock.patch('requests.get')
#     def test_wrapped_example(self, MockRequests):
#         mock_request = MockRequests()
#         # Set your status code you want to test against
#         mock_request.status_code = 200
#         # Set the response content you want to test against
#         mock_request.text = "{'channels': [{'channelType': 'Marketing', 'id': 9721, 'name': 'Push Marketing Channel', 'messageMedium': 'Push'}, {'channelType': 'Transactional', 'id': 9720, 'name': 'Transactional Channel', 'messageMedium': 'Email'}, {'channelType': 'Marketing', 'id': 9719, 'name': 'Marketing Channel', 'messageMedium': 'Email'}]}"
        
#         API_KEY= "94c3333a8e224b32b93a40788d1927cc"

#         ic= IterableAPI(api_key=API_KEY)
#         # Make your request
#         response = ic.list_channels()
        
#         # Test the result.
#         self.assertTrue(response.status_code == 200)


# test =APITest()

# test.test_wrapped_example(MockRequests)
# 	