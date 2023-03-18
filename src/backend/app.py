from flask import Flask, request, jsonify
from flask.json import JSONEncoder
from datetime import datetime
import os
import logging

from routes import events
from routes import webhooks

class CalendarJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime("%Y-%m-%dT%H:%M")
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

app = Flask(__name__)
app.json_encoder = CalendarJSONEncoder

@app.after_request
def after_request_func(response):
    response.headers.add('Access-Control-Allow-Origin', "*")
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    response.headers.add('Accept-Ranges', 'bytes')
    return response

def main():
    logging.getLogger().setLevel(logging.INFO)

    app.register_blueprint(events.app_events)
    # app.register_blueprint(webhooks.app_webhooks)

    app.run(
        host="0.0.0.0", 
        port=5000, 
        debug=True)


if __name__ == '__main__':
    main()
