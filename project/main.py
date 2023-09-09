from flask import Blueprint, render_template, redirect, url_for, session, jsonify, request,flash
from . import db, backend_url
from flask_login import login_required, current_user
import requests
import json
from .models import Token, CartItems, Carts, Transactions, TransactionDetails
from . import logger


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
    profile_resp = requests.get(get_profile_url, verify=False)
    return render_template('profile.html', profile = json.loads(profile_resp.text))

@main.route('/pets')
@login_required
def pets():
    return render_template('pets.html')

@main.route('/allpets')
@login_required
def inventory():
    get_inventory_url = backend_url + "/store/inventory"
    logger.info("get_inventory_url is "+ get_inventory_url)
    headers = {"api_key":"",
               "Postman-Token":"6009e770-58ea-4081-8e7a-22ec012d8ed7"}
    resp = requests.get(get_inventory_url, headers=headers, verify=False)
    return_data = resp.text
    data = json.loads(return_data)
    logger.info(data)
    return render_template('store/inventory.html', data = data)

@main.route('/admin/pets')
def admin_pets():
    return render_template('pets_menu.html')

@main.route('/checkout')
@login_required
def getcheckoutpage():
    cartitems = CartItems.query.all()
    logger.info(cartitems)
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
    resp = requests.get(get_inventory_url, headers=headers, verify=False)
    return_data = resp.text
    data = json.loads(return_data)
    #print(data)
    return render_template('store/inventory.html', data = data)

@main.route('/shippinginfo', methods=['GET','POST'])
@login_required
def shippinginfo():
    headers = {"Content-Type": "application/json"}
    door_num = request.form.get('door')
    street = request.form.get('street')
    city = request.form.get('city')
    country = request.form.get('country')
    pincode = request.form.get('pincode')
    address = str(door_num) + ", " + str(street) + ", " + str(city) + ", " + str(country) + ", " + str(pincode)

    cart = Carts.query.filter_by(username = current_user.username).first()
    
    logger.info(cart)
    cart_id = cart.id
    logger.info(cart_id)
    cartitems = CartItems.query.filter_by(cart_id = cart_id).all()

    logger.info(cartitems)
    
    cartitems_dict = {}
    for i in range(len(cartitems)):
        cartitems_dict.update({
            cartitems[i].id : {
                "pet_id": cartitems[i].pet_id,
                "cart_id": cartitems[i].cart_id
            } 
        })
    
    #print(cartitems_dict)

    #check if transaction is active
    active_transactions = Transactions.query.filter_by(status = "active").all()
    if len(active_transactions) != 0:
        #Nothing added in cart
        return render_template('checkout.html')
    else:
        transaction = Transactions(username = current_user.username, cartid = cart_id, status = "active")
        TransactionDetails(address=address, transactions = transaction)
    
        db.session.add(transaction)
        db.session.commit()
        #order_details = 

        order = Transactions.query.filter_by(status = "active").all()
        order_num = order[0].id
        order_details = TransactionDetails.query.filter_by(transaction_id = order_num).all()
        #print(order_details)
        for i in range(len(order_details)):
            payload = {}
            for k,v in cartitems_dict.items():
                payload.update({
                "pet_id" : v["pet_id"],
                "transactionDetailsId" : order_details[i].id,
                "username" : current_user.username,
                "shipDate": "2017-07-21T17:32:28Z",
                "status" : "approved",
                "complete": True
                })
                
                order_place_url = backend_url+"/store/order"
                order_place_response = requests.post(order_place_url, headers=headers, data=json.dumps(payload),verify=False)
                
        
        #update the transaction to approved
        active_transactions = Transactions.query.filter_by(status = "active").all()
        
        for i in range(len(active_transactions)):
        
            active_transactions[i].status = "approved"
            db.session.commit()
        return render_template('orderdetails.html', payload = json.dumps(payload))

@main.route('/addtocart', methods=['GET'])
@login_required
def addtocart():
    username = current_user.username
    pet_id = request.args["pet_id"]
    cart = Carts.query.filter_by(username = current_user.username).first()
    cart_id = cart.id
    cart_items = CartItems.query.all()
    
    data=[]
    
    for i in range(len(cart_items)):
        #print(cart_items[i])
        data.append(cart_items[i].pet_id )
        #print(data)
    
    if int(pet_id) in data:
        pass
    else:
        #print(type(pet_id))
        #print("not in list")
        new_cart_item = CartItems(pet_id = pet_id, cart_id=cart_id)
        db.session.add(new_cart_item)
        db.session.commit()
    
    return redirect('/allpets')

@main.route('/removefromcart', methods=['GET'])
@login_required
def removefromcart():
    username = current_user.username
    pet_id = request.args["pet_id"]
    cart = Carts.query.filter_by(username = current_user.username).first()
    cart_id = cart.id
    cart_items = CartItems.query.filter_by(pet_id = int(pet_id)).first()

    
    if cart_items == None:
        return redirect('/allpets')
    else:
        db.session.delete(cart_items)
        db.session.commit()
        return redirect('/allpets')

@main.route('/viewcart', methods=['GET'])
@login_required
def viewcart():
    # Need to Fix this flow
    cart_items = CartItems.query.all()
    data=[]
    
    for i in range(len(cart_items)):
        data.append(cart_items[i].pet_id )
    logger.info(data)
    data_to_display = {}
    num_of_items = len(data)
    data_to_display.update({
        "total_items": num_of_items,
        "Items": data
    })
    
    return render_template('viewcart.html', data = data_to_display)


@main.route('/placeorder', methods=['GET', 'POST'])
@login_required
def orderdetails():
    return redirect('/shippinginfo')