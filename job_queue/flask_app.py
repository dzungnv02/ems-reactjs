from flask import Flask
from flask import jsonify, request
from flask_cors import CORS, cross_origin
import json
import time
from celery import Celery
from flask_restful import Resource, Api, reqparse
import sys
import os
from tasks_docker import create_workspace, add_team, config_plugin, enable_plugin, disable_plugin

app = Flask(__name__)
CORS(app, allow_headers=['Content-Type', 'Access-Control-Allow-Origin',
                         'Access-Control-Allow-Headers', 'Access-Control-Allow-Methods'])

api = Api(app)



@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS,POST,PUT"
    response.headers["Access-Control-Allow-Headers"] = \
        "Access-Control-Allow-Headers,  Access-Control-Allow-Origin, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
    return response


# These are just some health/server is up checks

@app.route('/', methods=['GET'])
def enter():
    return jsonify({'status': 'ok'})


@app.route('/health', methods=['POST'])
@cross_origin(origin='*')
def health():
    try:
        data = json.loads(request.data.decode('utf-8'))
        return jsonify(data)
    except Exception as e:
        return jsonify({'status': 'ok'})


class CreateWorkspace(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('workspaceId', type=str, required=True)
        args = parser.parse_args()
        create_workspace.delay(args.workspaceId)
        return {'context': {'request': args, 'path': '/create_workspace'}, 'sent': 1}

class AddTeam(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('workspaceId', type=str, required=True)
        parser.add_argument('team_name', type=str, required=True)
        parser.add_argument('team_path', type=str, required=True)
        args = parser.parse_args()
        add_team.delay(args.workspaceId, args.team_name, args.team_path)
        return {'context': {'request': args, 'path': '/add_team'}, 'sent': 1}

class ConfigPlugin(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('pluginId', type=str, required=True)
        args = parser.parse_args()
        config_plugin.delay(args.pluginId)
        return {'context': {'request': args, 'path': '/config_plugin'}, 'sent': 1}

class DisablePlugin(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('pluginId', type=str, required=True)
        args = parser.parse_args()
        disable_plugin.delay(args.pluginId)
        return {'context': {'request': args, 'path': '/disable_plugin'}, 'sent': 1}

class EnablePlugin(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('pluginId', type=str, required=True)
        args = parser.parse_args()
        enable_plugin.delay(args.pluginId)
        return {'context': {'request': args, 'path': '/enable_plugin'}, 'sent': 1}

api.add_resource(CreateWorkspace, '/create_workspace')
api.add_resource(AddTeam, '/add_team')
api.add_resource(ConfigPlugin, '/config_plugin')
api.add_resource(EnablePlugin, '/enable_plugin')
api.add_resource(DisablePlugin, '/disable_plugin')
