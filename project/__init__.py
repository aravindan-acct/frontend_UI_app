from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os




    
db = SQLAlchemy()
# Picking the IP of the WAF service protecting the API
if os.path.exists('/tmp/withwaf.txt'):
    backend_app_svc = os.environ['WAFIP']
    callback_ip = os.environ['WAFPublicIP']
else:
    backend_app_svc = os.environ['apiserver']
    callback_ip = os.environ['publicip']

backend_url = "http://"+backend_app_svc+":8080/api/petstore/1.0.0"
headers = {"Content-Type":"application/json"}


