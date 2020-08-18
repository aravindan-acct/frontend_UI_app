import socket
import requests
import json
from http_basic_auth import generate_header, parse_header
import os

waf_ip = os.environ['WAFIP']
waf_password = os.environ['WAFPASSWORD']
headers = {"Content-Type": "application/json"}
login_url = "http://"+waf_ip+":8000/restapi/v3.1/login"
login_payload = {"username":"admin", "password":waf_password}
login_request = requests.post(login_url, headers=headers, data=json.dumps(login_payload))
token_output=login_request.text
token_split=token_output.split(":")
token_rstrip=token_split[1].rstrip("}")
token=token_rstrip.replace('"','')
auth_header=generate_header('',token)
api_headers = {"Content-Type":"application/json", "Authorization": auth_header}
#Creating the Service
hostname = socket.gethostname()

server = socket.gethostbyname(hostname)
#Create certificate
certificate_url = "http://"+waf_ip+":8000/restapi/v3.1/certificates/self-signed-certificate"
cert_payload = {
  "state": "CA",
  "key-size": "1024",
  "common-name": "training.petstore.com",
  "city": "San Francisco",
  "organizational-unit": "Training",
  "allow-private-key-export": "Yes",
  "name": "petstore",
  "country-code": "US",
  "key-type": "RSA",
  "elliptic-curve-name": "secp256r1",
  "organization-name": "Barracuda Networks"
}

cert_create_resp = requests.post(certificate_url, headers= api_headers, data=json.dumps(cert_payload))

print(cert_create_resp.text)


service_url = "http://"+waf_ip+":8000/restapi/v3.1/services"

svc_payload = {
    "address-version": "IPv4",
    "ip-address": waf_ip,
    "name": "frontend_svc",
    "port":443,
    "status": "On",
    "type": "HTTPS",
    "certificate": "petstore"}

create_svc = requests.post(service_url, data=json.dumps(svc_payload), headers = api_headers)
print(create_svc.text)
svr_url = "http://"+waf_ip+":8000/restapi/v3.1/services/frontend_svc/servers"
svr_payload = {
    "name": "frontendappserver",
    "port": 7979,
    "ip-address": server,
    "identifier": "IP Address",
    "address-version": "IPv4"
}
create_svr = requests.post(svr_url, headers = api_headers, data=json.dumps(svr_payload))
print(create_svr.text)
