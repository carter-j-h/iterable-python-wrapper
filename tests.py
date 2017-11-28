import unittest

from iterable_wrapper import IterableAPI

class WrapperTestCase(unittest.TestCase):
    """Tests for `iterable_wrapper.py`."""

    


    def test_users_requests(self):
        """Is api reqeust behaving correctly?"""
        self.assertTrue(IterableAPI.api_call(call="/api/users/getByEmail", method="GET", params={"email": "carter@iterable.com"}))

if __name__ == '__main__':
    unittest.main()
