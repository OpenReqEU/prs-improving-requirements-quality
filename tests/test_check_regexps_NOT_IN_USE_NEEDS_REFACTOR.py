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


class TestCheckRegexps(unittest.TestCase):

    def setUp(self):
        # Ignore third-party warnings from setup phase..
        warnings.simplefilter('ignore')
        # Initialize Flask server hosting api
        self.amb_api = amb_api.test_client()

    # Routes to the APIs that are being tested

    def _check_regexps(self, req):
        return self.amb_api.post(
            '/check-regexps',
            data=lib.API_INPUT_FORMAT.replace('{{requirement}}', req),
            follow_redirects=True)

    def _get_single_item_from_response(self, response, title):
        # Get JSON from response
        resp_json = json.loads(response.get_data())['1']['1']
        item_l = [item for item in resp_json if item['title'] == title]
        if item_l:
            return random.choice(item_l)
        else:
            return None

    # Unit Tests

    def test_return_title(self):
        response = self._check_regexps('The system shall read HTML and PDF or DOC files.')
        item = self._get_single_item_from_response(response, 'Unclear Associativity')
        # Check if the indexes are correct
        self.assertEqual(item['title'], 'Unclear Associativity')

    def test_return_description(self):
        response = self._check_regexps('The system shall read HTML and PDF or DOC files.')
        item = self._get_single_item_from_response(response, 'Unclear Associativity')
        # Check if the indexes are correct
        self.assertEqual(item['description'], 'The combination of \'and\' and \'or\' leads to unclear associativity.')

    def test_return_text(self):
        response = self._check_regexps('The system shall read HTML and PDF or DOC files.')
        item = self._get_single_item_from_response(response, 'Unclear Associativity')
        # Check if the indexes are correct
        self.assertEqual(item['text'], 'and PDF or')

    def test_return_indexes(self):
        response = self._check_regexps('The system shall read HTML and PDF or DOC files.')
        item = self._get_single_item_from_response(response, 'Unclear Associativity')
        # Check if the indexes are correct
        self.assertEqual(item['index_start'], 27)
        self.assertEqual(item['index_end'], 37)


if __name__ == '__main__':
    unittest.main(verbosity=2)
