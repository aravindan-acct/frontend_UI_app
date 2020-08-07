from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
backend_url ="http://backend:8080/api/petstore/1.0.0"
headers = {"Content-Type":"application/json"}


