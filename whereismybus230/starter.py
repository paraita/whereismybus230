#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_restplus import Resource
from flask_restplus import Api
from flask_restplus import fields
from flask_restplus import reqparse
import sophiabus230

app = Flask(__name__)
api = Api(app, version='1.0', title='Whereismybus230',
          description='Dude, where is my bus 230 ?!')

BusPassage = api.model('BusPassage', {
    'bus_time': fields.String(description='Time of passage in ISO8601 format',
                              required=True),
    'dest': fields.String(description='Terminus',
                          required=True),
    'is_real_time': fields.Boolean(description='Whether the time is an estimation or real time',
                                   required=True)
})


@api.route('/bus230')
class HelloWorld(Resource):

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('stop_id', required=True, type=int, help='Stop ID of the bus stop')

    @api.expect(get_parser)
    @api.response(200, 'Success', [BusPassage])
    def get(self):
        args = self.get_parser.parse_args()
        tt = sophiabus230.get_next_buses(stop_id=args['stop_id'])
        return [
            {
                'bus_time': bus['bus_time'].isoformat(),
                'dest': str(bus['dest']),
                'is_real_time': bus['is_real_time']
            }
            for bus in tt
        ]

if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=8080, debug=True)
    app.run()
