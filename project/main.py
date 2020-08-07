from flask import Blueprint, render_template, redirect, url_for, session, jsonify, request,flash
from . import db, backend_url
from flask_login import login_required, current_user
import requests
import json
from .models import Token

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/contactus')
def contactus():
    return render_template('contactus.html')

@main.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name = current_user.username)

@main.route('/pets')
@login_required
def pets():
    return render_template('pets.html')

@main.route('/allpets')
@login_required
def inventory():
    get_inventory_url = backend_url + "/store/inventory"
    #token = db.session.query(Token).order_by(Token.id.desc()).first()
    #headers = {"Authorization": token.tokenstring}
    headers = {"api_key":"",
               "Postman-Token":"6009e770-58ea-4081-8e7a-22ec012d8ed7"}
    resp = requests.get(get_inventory_url, headers=headers)
    return_data = resp.text
    data = json.loads(return_data)
    print(data)
    return render_template('store/inventory.html', data = data)

@main.route('/admin/pets')
def admin_pets():
    return render_template('pets_menu.html')



