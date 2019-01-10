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


class TestCheckCompound(unittest.TestCase):

    def setUp(self):
        # Ignore third-party warnings from setup phase..
        warnings.simplefilter('ignore')
        # Initialize Flask server hosting api
        self.amb_api = amb_api.test_client()

    # Routes to the APIs that are being tested

    def _check_compound(self, req):
        return self.amb_api.post(
            '/check-compound',
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
        response = self._check_compound('Deleting company documents requires permission.')
        # pprint(json.loads(response.get_data()))
        item = self._get_single_item_from_response(response, 'Ambiguous Compound Nouns')
        # Check if the indexes are correct
        self.assertEqual(item['title'], 'Ambiguous Compound Nouns')

    def test_return_description(self):
        response = self._check_compound('Deleting company documents requires permission.')
        item = self._get_single_item_from_response(response, 'Ambiguous Compound Nouns')
        # Check if the indexes are correct
        self.assertEqual(item['description'], 'A sequence of more than two consecutive nouns may have more than one interpretation depending on the possible associations between the words.')

    def test_return_text(self):
        response = self._check_compound('Deleting company documents requires permission.')
        item = self._get_single_item_from_response(response, 'Ambiguous Compound Nouns')
        # Check if the indexes are correct
        self.assertEqual(item['text'], 'Deleting company documents')

    def test_return_indexes(self):
        response = self._check_compound('Deleting company documents requires permission.')
        item = self._get_single_item_from_response(response, 'Ambiguous Compound Nouns')
        # Check if the indexes are correct
        self.assertEqual(item['index_start'], 0)
        self.assertEqual(item['index_end'], 26)


if __name__ == '__main__':
    unittest.main(verbosity=2)
