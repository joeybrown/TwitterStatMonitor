from flask import Flask
from json import dumps as jsonify
from Variables import STAT_SERVER_PORT


class StatServer:
    """
    Http server with an endpoint of '/getStats' that returns a json object with statistics about the tweets
    """

    def __init__(self, stat_manager):
        self.flask_app = Flask(__name__)

        @self.flask_app.route("/getStats")
        def get_stats():
            return jsonify(stat_manager.get())

    def start(self):
        self.flask_app.run(port=STAT_SERVER_PORT)
