from celery import Celery
import time
import logging
import subprocess

celery = Celery(
        "tasks",
        broker='amqp://admin:mypass321@localhost:5672', backend='rpc://',
    )
logging.basicConfig(filename='./output.log',level=logging.DEBUG)

@celery.task(name='create_workspace')
def create_workspace(workspaceId):
    logging.info('CREATE WORKSPACE')
    try:
        subprocess.Popen(["sh",
            "scripts/create_workspace.sh",
            str(workspaceId)
        ])
    except Exception:
        print("Something went wrong!")
    return 0

@celery.task(name='add_team')
def add_team(workspaceId,team_name,team_path):
    logging.info('ADD TEAM')
    try:
        subprocess.Popen(["sh",
            "scripts/add_team.sh",
            str(workspaceId),str(team_name),str(team_path)
        ])
    except Exception:
        print("Something went wrong!")
    return 0

@celery.task(name='config_plugin')
def config_plugin(pluginId):
    logging.info('CONFIG PLUGIN')
    try:
        subprocess.Popen(["sh",
            "scripts/config_plugin.sh",
            str(pluginId)
        ])
    except Exception:
        print("Something went wrong!")
    return 0

@celery.task(name='enable_plugin')
def enable_plugin(pluginId):
    logging.info('ENABLE PLUGIN')
    try:
        subprocess.Popen(["sh",
            "scripts/enable_plugin.sh",
            str(pluginId)
        ])
    except Exception:
        print("Something went wrong!")
    return 0

@celery.task(name='disable_plugin')
def disable_plugin(pluginId):
    logging.info('DISABLE PLUGIN')
    try:
        subprocess.Popen(["sh",
            "scripts/disable_plugin.sh",
            str(pluginId)
        ])
    except Exception:
        print("Something went wrong!")
    return 0
