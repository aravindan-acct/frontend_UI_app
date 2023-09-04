# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request, redirect
import os
import logging
from input_validator import Validator
import json

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

logging.basicConfig(filename="/tmp/newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
# Creating an object
logger = logging.getLogger()
 
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/settings/starturl')
# ‘/settings/starturl’ URL is bound with provisioning() function.
def view_form():
    return render_template('starturl.html')

@app.route('/settings/target', methods=['GET','POST'])
def provisioning():
	if request.method == 'POST':
		frontendip = request.form.get('FrontendIP')
		if Validator.check_ip(str(frontendip)):
			pass
		elif Validator.check_string(str(frontendip)):
			pass
		else:
			return ('Invalid input for the Frontend',404)
		backendip = request.form.get('BackendIP')
		if Validator.check_ip(str(backendip)):
			pass
		elif Validator.check_string(str(frontendip)):
			pass
		else:
			return ('Invalid input for the Backend', 404)
		backendproto = request.form.get('BackendProto')
		if backendproto == "http" or backendproto == "https":
			pass
		else:
			return ('Invalid input for the Backend Protocol', 404)
		backendport = request.form.get('Backendport')
		backendport_num = int(backendport)
		if backendport_num == 8080 or backendport_num == 443:
			pass
		else:
			return ('Returning error. Please use 443 if proxying or specify the port as 8080', 404)
		os.environ["APISERVER"] = backendip
		os.environ["PUBLICIP"] = frontendip
		os.environ["APIPROTO"] = backendproto
		os.environ["APIPORT"] = backendport
		logger.debug(os.environ.get('APISERVER'))
		logger.debug(os.environ.get('PUBLICIP'))
		logger.debug(os.environ.get('APIPROTO'))
		logger.debug(os.environ.get('APIPORT'))
		params_dict = {
			"apiserver": backendip,
			"publicip" : frontendip,
			"apiproto" : backendproto,
			"apiport" : backendport
		}
		with open('/tmp/startup_params.json', 'w') as file:
			file.write(json.dumps(params_dict))
			file.close()
			
		try:
			logger.debug("Attempting to start the frontend app...")
			logger.info(os.system("sudo systemctl restart frontend"))
		except:
			pass
	return render_template('redirect.html', frontendip = frontendip)

@app.route('/settings/reset', methods=['POST'])

def reset():
	env_list = ['APISERVER', 'PUBLICIP', 'APIPROTO', 'APIPORT']
	for env_var in env_list:
		try:
			os.unsetenv(env_var)
		except:
			pass
	return ('Configuration Reset', 200)

# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application
	# on the local development server.
	app.run()
