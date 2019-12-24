from celery import Celery
import time

celery = Celery(
        "tasks",
        broker='amqp://admin:mypass321@rabbit:5672', backend='rpc://',
    )

@celery.task(name='create_workspace')
def create_workspace(workspaceId):
    return 0

@celery.task(name='add_team')
def add_team(workspaceId,team_name,team_path):
    return 0
@celery.task(name='config_plugin')
def config_plugin(pluginId):
    return 0
@celery.task(name='enable_plugin')
def enable_plugin(pluginId):
    return 0
@celery.task(name='disable_plugin')
def disable_plugin(pluginId):
    return 0

