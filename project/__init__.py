from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import json
import logging

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('/tmp/accesslogs.log', mode='a')
logger.addHandler(file_handler)


db = SQLAlchemy()


# Picking the details of the environment

try:
    backend_app_svc = os.environ['APISERVER']
    backend_app_port = os.environ['APIPORT']
    backend_app_proto = os.environ['APIPROTO']
    callback_ip = os.environ['PUBLICIP']
    backend_url = backend_app_proto+"://"+backend_app_svc+":"+backend_app_port+"/api/petstore/1.0.0"
except:
    with open('/tmp/startup_params.json', 'r') as file:
        contents = file.read()
        contents_dict = json.loads(contents)
        backend_url = contents_dict["apiproto"]+"://"+contents_dict["apiserver"]+":"+contents_dict["apiport"]+"/api/petstore/1.0.0"
headers = {"Content-Type":"application/json"}


