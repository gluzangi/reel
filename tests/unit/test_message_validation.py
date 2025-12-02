import unittest
from eel import EelApplication

class TestMessageValidation(unittest.TestCase):
    def setUp(self):
        self.app = EelApplication()

    def test_valid_call_message(self):
        msg = {'call': 1.234, 'name': 'test_func', 'args': [1, 2, 3]}
        self.assertTrue(self.app._validate_message(msg))

    def test_invalid_call_missing_name(self):
        msg = {'call': 1.234, 'args': []}
        self.assertFalse(self.app._validate_message(msg))

    def test_invalid_call_wrong_type(self):
        msg = {'call': '123', 'name': 'test', 'args': []}
        self.assertFalse(self.app._validate_message(msg))
        
    def test_invalid_call_args_not_list(self):
        msg = {'call': 1.0, 'name': 'test', 'args': 'not a list'}
        self.assertFalse(self.app._validate_message(msg))

    def test_valid_return_message(self):
        msg = {'return': 1.234, 'status': 'ok', 'value': 'result'}
        self.assertTrue(self.app._validate_message(msg))
        
    def test_invalid_return_missing_status(self):
        msg = {'return': 1.234, 'value': 'result'}
        self.assertFalse(self.app._validate_message(msg))

    def test_unknown_message_type(self):
        msg = {'unknown': 'type'}
        self.assertFalse(self.app._validate_message(msg))

if __name__ == '__main__':
    unittest.main()
