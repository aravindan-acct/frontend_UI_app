from flask import Blueprint, render_template, redirect, url_for, session, jsonify, request,flash
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
import requests
import json
from .models import Token
from . import db, backend_url
import os
from . import logger

admin = Blueprint('admin', __name__)


# Landing URL for admin login
@admin.route('/admin')
def administrator():
    with open('/tmp/startup_params.json', 'r') as file:
        contents = file.read()
        contents_dict = json.loads(contents)
        file.close()

    try:
        callback_ip = os.environ['PUBLICIP']
    except:
        callback_ip = contents_dict["publicip"]
    
    # Assuming that frontend is always deployed with HTTPS Protocol
    # Deployment on Azure is also tuned to deploy NGINX proxy listening on https/443
    callback_proto = "https"
    callback_port = "443"
    return render_template('admin.html', callback_ip = callback_ip, callback_proto = callback_proto, 
                            callback_port = callback_port)

@admin.route('/home')
def callback():
    
    return render_template('home.html')



@admin.route('/callback_backend', methods=['GET'])
def callback_backend():
    url_fragment = request.query_string
    query = str(url_fragment)
    query_list = query.split("=")
    access_token_element = query_list[1]
    access_token_list = access_token_element.split("&")
    access_token = access_token_list[0]
    auth_header_value = f"Bearer "+access_token
    new_token = Token(tokenstring = auth_header_value)
    db.session.add(new_token)
    db.session.commit()
    
    return redirect('/admin/all_pets')

# URL to add an item
@admin.route('/admin/addpet')
def addpet_get():
    return render_template('petupload.html')

# URL to edit an item. This route gets the item details with existing values.
# Useful to know what's existing and if that has to be changed.
@admin.route('/admin/petsedit', methods=['GET'])
def pets_edit():
    token = db.session.query(Token).order_by(Token.id.desc()).first()
    headers = {"Authorization": token.tokenstring}
    petid_string = request.args["petid"]
    petid_list = petid_string.split('y')
    get_pet_url = backend_url+"/pet/"+petid_list[1]
    get_pet_resp = requests.get(get_pet_url, headers=headers, verify=False)
    resp = json.loads(get_pet_resp.text)
    return render_template('/editpet.html', data = resp)

# URL to edit an item. This route uses the PUT method to edit the item values.
@admin.route('/admin/petsedit', methods=['POST'])
def pets_edit_put():
    token = db.session.query(Token).order_by(Token.id.desc()).first()
    headers = {"Authorization": token.tokenstring,
               'Content-Type': 'application/x-www-form-urlencoded'}
    tags = list()
    photoUrls=list()
    data = {}
    data.update({"id": request.form.get('id')})
    # Input validation for updated values
    if request.form.get('name'):
        name = request.form.get('name')
        data.update({"name": name})
    if request.form.get('tags_1'):
        tags_1 = request.form.get('tags_1')
        tags.append(tags_1)
    if request.form.get('tags_2'):
        tags_2 = request.form.get('tags_2')
        tags.append(tags_2)
        
    if request.form.get('photoUrls_1'):
        photoUrls_1 = request.form.get('photoUrls_1')
        photoUrls.append(photoUrls_1)
    if request.form.get('photoUrls_2'):
        photoUrls_2 = request.form.get('photoUrls_2')
        photoUrls.append(photoUrls_2)
    if request.form.get('status'):
        status = request.form.get('status')
        data.update({"status": status})
    if len(tags) == 0:
        pass
    else:
        data.update({"tags": tags})
    if len(photoUrls) == 0:
        pass
    else:
        data.update({"photoUrls": photoUrls})
    edit_url = backend_url+"/pet"
    edit_resp = requests.put(edit_url, headers=headers, data=urlencode(data), verify=False)
    if edit_resp.status_code == 200:
        print("Successfully edited")
        return redirect('/admin/all_pets')
    else:
        print("There is a problem with editing the Pet")
        return redirect('/admin/all_pets')

# This route fetches the list of items and renders it on the HTML
@admin.route('/admin/pets')
def admin_pets():
    return render_template('pets_menu.html')

# This route is used to delete an item from the inventory
@admin.route('/admin/petsdelete')
def pets_delete():
    token = db.session.query(Token).order_by(Token.id.desc()).first()
    headers = {"Authorization": token.tokenstring}
    petid_string = request.args["petid"]
    petid_list = petid_string.split('y')
    delete_url = backend_url+"/pet/"+petid_list[1]
    delete_resp = requests.delete(delete_url, headers=headers, verify=False)
    if delete_resp.status_code == 200:
        return redirect('/admin/all_pets')
    else:
        return redirect('/admin/all_pets')


@admin.route('/admin/all_pets')
def pets_menu():
    token = db.session.query(Token).order_by(Token.id.desc()).first()
    headers = {"Authorization": token.tokenstring}
    available_status_url = backend_url+"/pet/findByStatus?status=available&status1=pending&status2=sold"
    available_status_response = requests.get(available_status_url, headers=headers, verify=False)
    resp = dict()
    resp = json.loads(available_status_response.text)
    return render_template('pets_menu.html', display_json=resp)

# Provides a starter pack of items so that the portal can be trialed.
@admin.route('/admin/uploadsampledata')
def uploadsampledata():
    token = db.session.query(Token).order_by(Token.id.desc()).first()
    
    available_status_url = backend_url+"/pet/findByStatus?status=available&status=pending"
    logger.info(available_status_url)
    headers = {"Authorization": token.tokenstring}
    logger.info(headers)

    available_status_response = requests.get(available_status_url, headers=headers, verify=False)

    resp = dict()
    resp = json.loads(available_status_response.text)
    logger.info(resp)

    if len(resp) >= 1:
        logger.info("data exists")
        return redirect('/admin/all_pets')
    else:
        logger.info("Current working directory is ")
        logger.info(os.getcwd())
        directory = os.getcwd()
        with open(f"{directory}"+"/project/pets_data.json") as sample_file:
            file_content=sample_file.read()
            logger.info(file_content)
            data=json.loads(file_content)
        for keys,val in data.items():
            
            pet_url = backend_url+"/pet"
            
            headers = {"Authorization": token.tokenstring,
                       "Content-Type": "application/x-www-form-urlencoded"}
            print("val is {}".format(val))
            tags = list()
            tags.append(val["tag_1"])
            tags.append(val["tag_2"])
            photoUrls=list()
            photoUrls.append(val["photo_1"])
            photoUrls.append(val["photo_2"])
            payload = {
                "name": val["name"],
                "tags": tags,
                "photoUrls": photoUrls,
                "status": val["status"]
            }
            response = requests.post(pet_url, headers=headers, data=urlencode(payload), verify=False)
        
        return redirect('/admin/all_pets')

# This route is used for adding a new item to the existing list    
@admin.route('/admin/addpet', methods=['POST'])
def addpet():
    token = db.session.query(Token).order_by(Token.id.desc()).first()
    headers = {"Authorization": token.tokenstring,
    'Content-Type': 'application/x-www-form-urlencoded'}
    url = backend_url+"/pet"
    name = request.form.get('name')
    
    tags_1 = request.form.get('tags_1')
    tags_2 = request.form.get('tags_2')
    
    tags = list()
    tags.append(tags_1)
    tags.append(tags_2)
    photoUrls_1 = request.form.get('photoUrls_1')
    photoUrls_2 = request.form.get('photoUrls_2')
    photoUrls=list()
    photoUrls.append(photoUrls_1)
    photoUrls.append(photoUrls_2)
    status = request.form.get('status')
    
    payload = {
        "name": name,
        "tags": tags,
        "photoUrls": photoUrls,
        "status": status
    }
    response = requests.post(url, headers=headers, data=urlencode(payload), verify=False)
    if response.status_code == 200:
        resp = json.loads(response.text)
        return redirect('/admin/all_pets')
    else:
        return render_template('/editpet.html')



