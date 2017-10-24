""" Flask server Entry Script
"""

from flask import (Flask)
from flask_cors import CORS


APP = Flask(__name__)
APP.config['SECRET_KEY'] = 'Trukish'

CORS(APP)

if __name__ == "__main__":
    APP.run(
        '0.0.0.0',
        5000,
        debug=False,
        threaded=True
    )
