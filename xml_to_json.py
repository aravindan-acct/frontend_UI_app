# Program to convert an xml 
# file to json file 

# import json module and xmltodict 
# module provided by python 
import json 
import xmltodict
import base64
import os

# open the input xml file and read 
# data in form of python dictionary 
# using xmltodict module 
with open("ovf-env.xml") as xml_file: 
	
	data_dict = xmltodict.parse(xml_file.read()) 
	xml_file.close() 
	
	# generate the object using json.dumps() 
	# corresponding to json data 
	
	json_data = json.dumps(data_dict) 
	
	# Write the json data to output 
	# json file 
	with open("data.json", "w") as json_file: 
		json_file.write(json_data) 
		json_file.close()

with open("data.json") as json_file:
    json_val = json.loads(json_file.read())
    json_file.close()

b64_data = json_val["ns0:Environment"]["ns1:ProvisioningSection"]["ns1:LinuxProvisioningConfigurationSet"]["ns1:CustomData"]
b64_decoded = base64.b64decode(b64_data)

decoded_json = json.loads(b64_decoded)

with open("waf_json", "w") as waf_json:
    waf_json.write(json.dumps(decoded_json))
    os.system(f'export WAFIP={decoded_json["waf_ip"]}')
    waf_json.close()
