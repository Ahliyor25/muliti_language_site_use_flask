"""
    Module handlers.py
    for handle all error and response in json not in html
"""


from flask.json import jsonify
from app import app


@app.errorhandler(405)
def method_not_allowed(error):
    """
        Route for handling errors with 405 status code
    """
    #pylint: disable=unused-argument
    return jsonify(msg="Method Not Allowed Maybe You Pereputal Get And Post"), 405


@app.errorhandler(500)
def something_went_wrong(error):
    """
        Route for handling errors with 500 status code
    """
    #pylint: disable=unused-argument