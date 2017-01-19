#!/usr/bin/env python

from flask import Flask
from flask_restplus import Resource, Api
import sophiabus230

app = Flask(__name__)
api = Api(app, version='1.0', title='Whereismybus230',
          description='Dude, where is my bus 230 ?!')


@api.route('/bus230')
class HelloWorld(Resource):

    def get(self):
        tt = sophiabus230.get_next_buses()
        return [
            {
                'bus_time': bus['bus_time'].isoformat(),
                'dest': str(bus['dest'], 'utf-8'),
                'is_real_time': bus['is_real_time']
            }
            for bus in tt
        ]

if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=8080, debug=True)
    app.run()