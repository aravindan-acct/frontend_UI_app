from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import logging

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('/tmp/accesslogs.log', mode='a')
logger.addHandler(file_handler)

db = SQLAlchemy()


# Picking the details of the environment


backend_app_svc = os.environ['APISERVER']
backend_app_port = os.environ['APIPORT']
backend_app_proto = os.environ['APIPROTO']
callback_ip = os.environ['PUBLICIP']



backend_url = backend_app_proto+"://"+backend_app_svc+":"+backend_app_port+"/api/petstore/1.0.0"
headers = {"Content-Type":"application/json"}


