# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request, redirect
import os
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

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
		os.environ['apiserver'] = backendip
		os.environ['publicip'] = frontendip
		os.environ['apiproto'] = backendproto
		os.environ['apiport'] = backendport
		print(os.environ.get('apiserver'))
	return 'Petstore Web App Configured Successfully'

# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application
	# on the local development server.
	app.run()
