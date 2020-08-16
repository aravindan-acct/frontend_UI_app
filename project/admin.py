from flask import Blueprint, render_template, redirect, url_for, session, jsonify, request,flash
from .pets import process_pets
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
import requests
import json
from .models import Token
from . import db, backend_url
import os

admin = Blueprint('admin', __name__)



@admin.route('/admin')
def administrator():
    callback_ip = os.environ['WAFPublicIP']
    return render_template('admin.html', callback_ip = callback_ip)


'''
@admin.route('/admin', methods=['POST'])
def administrator_login():

    return render_template('Callback.html')
'''
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

    '''
    url = "http://54.193.108.132:8080/api/petstore/1.0.0/pet"

    payload = 'name=testing28&id=19&tags=%5B%22tag1%22%2C%22%20tag2%22%5D&photoUrls=%5B%22photo1%22%2C%20%22photo2%22%5D&status=available'
    headers = {
        'Authorization': auth_header_value,
        'Content-Type': 'application/x-www-form-urlencoded'
        }

    response = requests.request("POST", url, headers=headers, data = payload)
    print(response.status_code)
    '''
    
    return redirect('/admin/all_pets')

'''
@admin.route('/adminhome.html')
def adminhome():
    
    token = db.session.query(Token).order_by(Token.id.desc()).first()
    headers = {"Authorization": token.tokenstring}
    url = "http://54.193.108.132:8080/api/petstore/1.0.0/pet/findByStatus?status=available"
    response = requests.get(url, headers=headers)

    return render_template('adminhome.html', display_json =  response.text)
'''

@admin.route('/admin/addpet')
def addpet_get():
    return render_template('petupload.html')

@admin.route('/admin/petsedit', methods=['GET'])
def pets_edit():
    token = db.session.query(Token).order_by(Token.id.desc()).first()
    headers = {"Authorization": token.tokenstring}
    print(headers)
    petid_string = request.args["petid"]
    petid_list = petid_string.split('y')
    get_pet_url = backend_url+"/pet/"+petid_list[1]
    print(get_pet_url)
    get_pet_resp = requests.get(get_pet_url, headers=headers)
    resp = json.loads(get_pet_resp.text)
    print(type(resp))
    return render_template('/editpet.html', data = resp)

@admin.route('/admin/petsedit', methods=['POST'])
def pets_edit_put():
    token = db.session.query(Token).order_by(Token.id.desc()).first()
    headers = {"Authorization": token.tokenstring,
               'Content-Type': 'application/x-www-form-urlencoded'}
    tags = list()
    photoUrls=list()
    data = {}
    data.update({"id": request.form.get('id')})
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
    print("Tags count is {}".format(len(tags)))
    print("Photos count is {}".format(len(photoUrls)))
    print(data)
    edit_url = backend_url+"/pet"
    edit_resp = requests.put(edit_url, headers=headers, data=urlencode(data))
    if edit_resp.status_code == 200:
        print("Successfully edited")
        return redirect('/admin/all_pets')
    else:
        print("There is a problem with editing the Pet")
        return redirect('/admin/all_pets')


@admin.route('/admin/petsdelete')
def pets_delete():
    token = db.session.query(Token).order_by(Token.id.desc()).first()
    headers = {"Authorization": token.tokenstring}
    petid_string = request.args["petid"]
    petid_list = petid_string.split('y')

    delete_url = backend_url+"/pet/"+petid_list[1]
    print(delete_url)
    delete_resp = requests.delete(delete_url, headers=headers)
    if delete_resp.status_code == 200:
        return redirect('/admin/all_pets')
    else:
        return redirect('/admin/all_pets')


@admin.route('/admin/all_pets')
def pets_menu():
    token = db.session.query(Token).order_by(Token.id.desc()).first()
    headers = {"Authorization": token.tokenstring}
    available_status_url = backend_url+"/pet/findByStatus?status=available&status=pending"
    available_status_response = requests.get(available_status_url, headers=headers)
    resp = dict()
    resp = json.loads(available_status_response.text)

    print(type(resp))
    print(len(resp))
    print(resp)
    return render_template('pets_menu.html', display_json=resp)

@admin.route('/admin/uploadsampledata')
def uploadsampledata():
    try:
        with open("static/pets_data.json") as sample_file:
            file_content=sample_file.read()
            data=json.loads(file_content)
        for keys,val in data.items():
            print(keys)
            print(val)
            pet_url = backend_url+"/pet"
            headers = {
                'Authorization': auth_header_value,
                'Content-Type': 'application/x-www-form-urlencoded'
                    }
        
            response = requests.request("POST", pet_url, headers=headers, data = urlencode(val))
        
        return redirect('/admin/all_pets')
    except:
        print("error loading sample data")
        return redirect('/admin/all_pets')

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
    print(tags)
    photoUrls_1 = request.form.get('photoUrls_1')
    photoUrls_2 = request.form.get('photoUrls_2')
    photoUrls=list()
    photoUrls.append(photoUrls_1)
    photoUrls.append(photoUrls_2)
    print(photoUrls)
    status = request.form.get('status')
    
    payload = {
        "name": name,
        "tags": tags,
        "photoUrls": photoUrls,
        "status": status
    }

    print(payload)
    
    
    response = requests.post(url, headers=headers, data=urlencode(payload))
    if response.status_code == 200:
        resp = json.loads(response.text)
        return redirect('/admin/all_pets')
    else:
        return render_template('/editpet.html')



