import requests
import json
from flask import Blueprint, render_template
from . import db
from flask_login import login_required, current_user

def process_pets():
    return "doing magic"