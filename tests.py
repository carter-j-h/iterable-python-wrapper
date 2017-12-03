from unittest import mock

# from iterable_wrapper import IterableAPI
import iterable_wrapper

# init class so we can test wrapper effectiveness
API_KEY= "94c3333a8e224b32b93a40788d1927cc"
# ic= IterableAPI(api_key=API_KEY)

# class WrapperTestCase(unittest.TestCase):
#     """Tests for `iterable_wrapper.py`."""    


#     def test_users_requests(self):
#         """Is api reqeust behaving correctly?"""
#         self.assertTrue(ic.api_call(call="/api/users/getByEmail", method="GET", params={"email": "carter@iterable.com"}))

# if __name__ == '__main__':
#     unittest.main()





@mock.patch("iterable_wrapper.IterableAPI")
def mock_IterableAPI(mock_class):
	print(mock_class)
	print(iterable_wrapper.IterableAPI)

	ic = iterable_wrapper.IterableAPI(api_key=API_KEY)
	print(ic)
	
	print(mock_class.return_value)



mock_IterableAPI()


def use_wrapper():
	ic = IterableAPI(api_key=API_KEY)
	print(ic.list_channels())

# use_wrapper()




