import os
import sys
import unittest
import warnings
import json
import random

# Add the path of the parent directory to sys.path so amb_api can be accessed IF test_all.py is in the "tests" folder
# sys.path.append(os.path.dirname(os.path.dirname(os.path.relpath(__file__))))
from starter import amb_api
import tests.lib as lib

class TestBasic(unittest.TestCase):

    def setUp(self):
        # Ignore third-party warnings from setup phase..
        warnings.simplefilter('ignore')
        # Initialize Flask server hosting api
        self.amb_api = amb_api.test_client()

    # Functions to help with unit tests

    def _call_check_quality(self, req):
        return self.amb_api.post(
            '/check-quality',
            data=lib.API_INPUT_FORMAT.replace('{{requirement}}', req),
            follow_redirects=True)

    def _get_single_item_from_response(self, response, title):
        # Get JSON from response
        resp_json = json.loads(response.get_data())['1']
        item_l = [item for item in resp_json if item['title'] == title]
        if item_l:
            return random.choice(item_l)
        else:
            return None

    # Unit tests

    def test_responsive(self):
        # Test if APIs are responding to a proper request
        response = self._call_check_quality('This is actually a good requirement.')
        self.assertEqual(response._status_code, 200, msg='API should be responsive with 200 status code')

    # This no longer functions since we longer offer an html UI this way.
    # The API doesn't serve HTML pages anymore
    # def test_responsive_html_ui(self):
    #     # Test if html ui is responding to a proper request
    #     response = self.amb_api.get(
    #         '/',
    #         follow_redirects=True)
    #     self.assertEqual(response._status_code, 200, msg='API should be responsive with 200 status code')

    def test_api_error_handling_empty_body(self):
        # Check if requests reject when "doc" is not in body
        response = self.amb_api.post(
            '/check-quality',
            data='{{}}',
            follow_redirects=True)
        self.assertEqual(response._status_code, 400, msg='API should handle an empty body')

    def test_api_error_handling_missing_key(self):
        # Check if requests reject when "doc" is not in body
        response = self.amb_api.post(
            '/check-quality',
            data='{"wrong_key": true}',
            follow_redirects=True)
        self.assertEqual(response._status_code, 400, msg='API should handle a body with missing keys')

    def test_return_proper_json(self):
        # Check if APIs return the proper JSON

        response = self._call_check_quality('This is actually a good requirement.')
        result = json.loads(response.get_data())

        self.assertIsInstance(result, dict, msg='API should return a dict')
        self.assertIn('1', result, msg='API result should be structured based on input')
        self.assertIsInstance(result['1'], list, msg='API results should be in a list')
        self.assertIsInstance(random.choice(result['1']), dict, msg='API should return a list with dicts inside')
        result_list = result['1']
        self.assertIn('title', random.choice(result_list), msg='API returned object missing attribute: title')
        self.assertIn('text', random.choice(result_list), msg='API returned object missing attribute: text')
        self.assertIn('description', random.choice(result_list), msg='API returned object missing attribute: description')
        self.assertIn('index_start', random.choice(result_list), msg='API returned object missing attribute: index_start')
        self.assertIn('index_end', random.choice(result_list), msg='API returned object missing attribute: index_end')

    def test_return_title(self):
        response = self._call_check_quality('This is actually a good requirement.')
        item = self._get_single_item_from_response(response, 'Actually')
        # Check if the indexes are correct
        self.assertEqual(item['title'], 'Actually')

    def test_return_description(self):
        response = self._call_check_quality('This is actually a good requirement.')
        item = self._get_single_item_from_response(response, 'Actually')
        # Check if the indexes are correct
        self.assertEqual(item['description'], 'Requirements shall avoid possibilities.')

    def test_return_text(self):
        response = self._call_check_quality('This is actually a good requirement.')
        item = self._get_single_item_from_response(response, 'Actually')
        # Check if the indexes are correct
        self.assertEqual(item['text'], 'actually')

    def test_return_indexes(self):
        response = self._call_check_quality('This is actually a good requirement.')
        item = self._get_single_item_from_response(response, 'Actually')
        # Check if the indexes are correct
        self.assertEqual(item['index_start'], 8)
        self.assertEqual(item['index_end'], 16)

if __name__ == '__main__':
    # Run the TestBasic unit tests
    unittest.main(verbosity=2)
