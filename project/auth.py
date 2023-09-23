from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Carts, CartItems
from . import db, backend_url, headers
from flask_login import login_user, logout_user, login_required, current_user
import requests
import json
from .input_validator import Validator
from . import logger

auth = Blueprint('auth', __name__)



@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    try:
        activeuser = current_user.username
        cart = Carts.query.filter_by(username = activeuser).first()
        cart_id = cart.id
        delete_cart_items = CartItems.query.filter_by(cart_id = cart_id).all()
        for i in range(len(delete_cart_items)):
            print("deleting cart items {} for this cart".format(delete_cart_items[i]))
            db.session.delete(delete_cart_items[i])
            db.session.commit()
        delete_cart = Carts.query.filter_by(username = current_user.username).all()
        logger.info(delete_cart)
        logger.info(type(delete_cart))
        for i in range(len(delete_cart)):
            print("deleting cart {} for the user".format(delete_cart[i]))

            db.session.delete(delete_cart[i])
            db.session.commit()
        logout_user()
    except:
        logout_user()
    return redirect(url_for('main.index'))

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    username = request.form.get('username')
    if Validator.check_string(str(username)):
        pass
    else:
        return ('Invalid input', 404)
    password = request.form.get('password')
    if Validator.check_passwd(str(password)):
        pass
    else:
        return('Invalid input', 404)
    firstName = request.form.get('firstName')
    if Validator.check_string(str(firstName)):
        pass
    else:
        return ('Invalid input', 404)
    lastName = request.form.get('lastName')
    if Validator.check_string(str(lastName)):
        pass
    else:
        return ('Invalid input', 404)
    phone = request.form.get('phone')

    #user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    user_get_url = backend_url + "/user/" + username
    user_get = requests.get(user_get_url, verify=False)
    if user_get.status_code == 200:
    #if user: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    '''
    new_user = User(email=email, username=username, firstName=firstName, lastName=lastName, 
    phone=phone, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    '''
    payload = {
        "email": email,
        "username": username,
        "password": password,
        "firstName": firstName,
        "lastName": lastName,
        "phone": phone
    }
    new_user_url = backend_url + "/user"
    new_user = requests.post(new_user_url, headers=headers, data=json.dumps(payload), verify=False)
    if new_user.status_code == 200:
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('auth.signup'))

@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    #user = User.query.filter_by(email=email).first()
    user_login_url = backend_url + "/user/login?username=" + username + "&password=" + password
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    user_get = requests.get(user_login_url, verify=False)
    logger.info(user_login_url)
    logger.info(user_get.status_code)
    logger.info(user_get.text)
    if user_get.status_code != 200:
    #if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    else:
        logger.info("Proceeding with the user flow")
        user_get_info = backend_url + "/user/" + username
        user_info_resp = requests.get(user_get_info, verify=False)
        user_info_text = user_info_resp.text
        user_info = json.loads(user_info_text)
        logger.info(type(user_info))
        logger.info(user_info)
        class user:
            is_active=user_info["is_active"]
            is_authenticated=user_info["is_authenticated"]
            def get_id():
                return user_info["get_id"]
        new_user = User(username=user_info["username"])
        new_cart = Carts(username = username, activestate = "active")
        # add the new user to the database
        db.session.add(new_user)
        
        db.session.commit()
        db.session.add(new_cart)
        db.session.commit()
        user = User.query.filter_by(username = user_info["username"]).first()
        login_user(user, remember=remember)
        logger.info("redirecting the user to /allpets")
    return redirect('/allpets')

