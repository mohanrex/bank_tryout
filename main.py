""" Flask server Entry Script
"""

# Default flask imports with CORS to allow cross origin request
from flask import (Flask)
from flask_cors import CORS

# Controllers for this application
from controllers import (account_controller)

# Flask Configuration
APP = Flask(__name__)
APP.config['SECRET_KEY'] = 'Trukish'
CORS(APP)

# Register accounts controller
APP.register_blueprint(account_controller.ACCOUNT_V1)

if __name__ == "__main__":
    """ Flask App Initialization
    """
    APP.run(
        '0.0.0.0',
        5000,
        debug=True,
        threaded=True
    )
