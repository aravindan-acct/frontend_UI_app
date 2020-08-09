from flask import Blueprint, render_template, redirect, url_for, session, jsonify, request,flash
from . import db, backend_url
from flask_login import login_required, current_user
import requests
import json
from .models import Token, CartItems, Carts

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
    username = current_user.username
    get_profile_url = backend_url + "/user/" +username
    profile_resp = requests.get(get_profile_url)
    print(profile_resp.text)
    return render_template('profile.html', profile = json.loads(profile_resp.text))

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

@main.route('/checkout')
@login_required
def getcheckoutpage():
    cartitems = CartItems.query.all()
    print(cartitems)
    print(type(cartitems))
    if len(cartitems) == 0:
        return redirect(url_for('main.pets'))
    else:
        return render_template('checkout.html')

@main.route('/checkout', methods=['POST'])
@login_required
def checkout_for_order():
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

@main.route('/shippinginfo', methods=['POST'])
@login_required
def shippinginfo():
    

    return render_template('pets.html')

@main.route('/addtocart', methods=['GET'])
@login_required
def addtocart():
    username = current_user.username
    pet_id = request.args["pet_id"]
    cart = Carts.query.filter_by(username = current_user.username).first()
    cart_id = cart.id
    new_cart_item = CartItems(pet_id = pet_id, cart_id=cart_id)
    db.session.add(new_cart_item)
    db.session.commit()
    
    return render_template('pets.html')

