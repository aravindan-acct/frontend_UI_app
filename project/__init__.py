from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


db = SQLAlchemy()
# Picking the IP of the WAF service protecting the API
backend_app_svc = os.environ['WAFIP']
backend_url = "http://"+backend_app_svc+":8080/api/petstore/1.0.0"
callback_ip = os.environ['WAFPublicIP']
headers = {"Content-Type":"application/json"}


