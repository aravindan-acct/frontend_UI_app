# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request, redirect
import os
import logging
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
# ‘/starturl’ URL is bound with provisioning() function.
def view_form():
    return render_template('starturl.html')

@app.route('/settings/target', methods=['GET','POST'])
def provisioning():
	if request.method == 'POST':
		frontendip = request.form.get('FrontendIP')
		backendip = request.form.get('BackendIP')
		backendproto = request.form.get('BackendProto')
		backendport = request.form.get('Backendport')
		os.environ["APISERVER"] = backendip
		os.environ["PUBLICIP"] = frontendip
		os.environ["APIPROTO"] = backendproto
		os.environ["APIPORT"] = backendport
		print(os.environ.get('APISERVER'))
		try:
			os.chdir("/etc/startup/frontend_UI_app")
			os.system("nohup python3 -m project &")
		except:
			pass
	return 'Petstore Web App Configured Successfully'

# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application
	# on the local development server.
	app.run()
