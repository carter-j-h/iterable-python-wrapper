import unittest

from iterable_wrapper import IterableAPI

# init class so we can test wrapper 
API_KEY= "94c3333a8e224b32b93a40788d1927cc"
ic= IterableAPI(api_key=API_KEY)

class WrapperTestCase(unittest.TestCase):
    """Tests for `iterable_wrapper.py`."""    


    def test_users_requests(self):
        """Is api reqeust behaving correctly?"""
        self.assertTrue(ic.api_call(call="/api/users/getByEmail", method="GET", params={"email": "carter@iterable.com"}))

if __name__ == '__main__':
    unittest.main()
