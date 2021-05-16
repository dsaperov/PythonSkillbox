import unittest
from unittest.mock import Mock
import handling_external_data

_test_data = """
1234567
12345
123456789
12
"""


class ExternalResourceGetterTest(unittest.TestCase):

    def test_normal(self):
        getter = handling_external_data.ExternalResourceGetter(url='')
        fake_response = Mock()
        fake_response.text = _test_data
        handling_external_data.requests.get = Mock(return_value=fake_response)
        result = getter.run()
        self.assertEqual(result, 9)


if __name__ == '__main__':
    unittest.main()
