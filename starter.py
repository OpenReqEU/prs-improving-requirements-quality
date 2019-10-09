# -*- coding: utf-8 -*-
import json
from flask import (
    Flask, request, abort, jsonify, render_template
)
from flask_cors import CORS

from app.requirement_improver import RequirementChecker

amb_api = Flask(__name__, template_folder='./demos/iframe/static', static_folder='./demos/iframe/static')

CORS(amb_api)  # So we can run and test locally. May be production necessary as well.

with open('./config.json') as config_file:
    CONFIG = json.load(config_file)


class Requirement:

    def __init__(self, *, id, text):
        # These attributes are a part of the OpenReq JSON Standard: <Link to OpenReq JSON Standard>

        ## Required by this API ##
        # The unique identifier of a Requirement. Not a null value or an empty string.
        self.id = id
        # The textual description or content of a Requirement.
        self.text = text


def check_json_conformance():
    json_data = {}
    try:
        # Check that the request can be read
        json_data = request.get_json(force=True)
    except:
        abort(400, 'Unable to load data. Please refer to documentation on how to send JSON data in a POST request')

    # Transform data into appropriate format, checking conformance along the way
    try:
        # Extract requirements from JSON
        reqs = json_data['requirements']
        # Check each requirement for conformance
        [Requirement(id=req['id'], text=req['text']) for req in reqs]
    except KeyError:
        abort(400, """Improper body sent. Body should resemble the following example input:
            {
                "requirements": [{
                    "id": 1,
                    "text": "This is actually a good requirement."
                },{
                    "id": 2,
                    "text": "The system shall read HTML and PDF or DOC files."
                }]
            }""")
    return json_data


def get_reqs(json_data):
    reqs = json_data['requirements']
    reqs = [Requirement(id=req['id'], text=req['text']) for req in reqs]
    return reqs


def get_config(json_data):
    # Check if the user has passed a config
    try:
        return json_data['config']
    except KeyError:
        # The config is optional, so we simply return None if it is not found
        return None


# These initial routes are to enable the demo to function properly.
# You can remove these these routes if you do not need the demo.
# IMPORTANT NOTE: This route is no longer functional. Please use provided demos.
# @amb_api.route('/')
# @amb_api.route('/<requirement>')
# @amb_api.route('/index/<requirement>')
# def index(requirement=None):
#     # Render page with ambiguities labelled
#     return render_template('index.html')


# This is the main route for checking requirement(s) quality
@amb_api.route("/check-quality", methods=['POST'])
def check_quality():
    json_data = check_json_conformance()
    reqs = get_reqs(json_data)
    config = get_config(json_data)
    return jsonify(RequirementChecker(reqs, config).check_quality())


if __name__ == "__main__":
    amb_api.run(debug=True, host=CONFIG['HOST'], port=CONFIG['PORT'])
