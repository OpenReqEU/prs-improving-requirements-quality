import os
import sys
import unittest
import warnings
import json
import random

import lib
# Add the path of the parent directory to sys.path so amb_api can be accessed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from starter import amb_api

# Development imports


class TestCheckPOSRegexps(unittest.TestCase):

    def setUp(self):
        # Ignore third-party warnings from setup phase..
        warnings.simplefilter('ignore')
        # Initialize Flask server hosting api
        self.amb_api = amb_api.test_client()

    # Routes to the APIs that are being tested

    def _check_pos_regexps(self, req):
        return self.amb_api.post(
            '/check-pos-regexps',
            data=lib.API_INPUT_FORMAT.replace('{{requirement}}', req),
            follow_redirects=True)

    def _get_single_item_from_response(self, response, title):
        # Get JSON from response
        resp_json = json.loads(response.get_data())['1']['1']
        # Look for item in list of items
        item_l = [item for item in resp_json if item['title'] == title]
        if item_l:
            return random.choice(item_l)
        else:
            return None

    # Unit Tests

    def test_return_title(self):
        response = self._check_pos_regexps('The system will be tested.')
        # pprint(json.loads(response.get_data()))
        item = self._get_single_item_from_response(response, 'Passive Ambiguity')
        # Check if the indexes are correct
        self.assertEqual(item['title'], 'Passive Ambiguity')

    def test_return_description(self):
        response = self._check_pos_regexps('The system will be tested.')
        item = self._get_single_item_from_response(response, 'Passive Ambiguity')
        # Check if the indexes are correct
        self.assertEqual(item['description'], 'Authors should state requirements in active form, as passive conceals who is responsible for the action.')

    def test_return_text(self):
        response = self._check_pos_regexps('The system will be tested.')
        item = self._get_single_item_from_response(response, 'Passive Ambiguity')
        # Check if the indexes are correct
        self.assertEqual(item['text'], 'be tested')

    def test_return_indexes(self):
        response = self._check_pos_regexps('The system will be tested.')
        item = self._get_single_item_from_response(response, 'Passive Ambiguity')
        # Check if the indexes are correct
        self.assertEqual(item['index_start'], 16)
        self.assertEqual(item['index_end'], 25)


if __name__ == '__main__':
    unittest.main(verbosity=2)
