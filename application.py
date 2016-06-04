from flask import Flask, request, redirect, url_for, render_template, flash, send_file, abort, Response, jsonify
import os 


###############################CONFIG#######################################
BUILTINPORT = 5000
TWISTEDPORT = 80
TWISTEDLOGFILE = "/var/log/app.log"
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
# Session seed, for per-session data
app.secret_key = os.urandom(24)



################################METHODS######################################
## Start up Stuff

# Start a twistd server
def twisted():
	print 'Twisted on port {port}...'.format(port=TWISTEDPORT)
	# Only import these if we need them
	from twisted.internet import reactor
	from twisted.web.server import Site
	from twisted.web.wsgi import WSGIResource
	from twisted.python import log as twisted_log
	twisted_log.startLogging(file=open(TWISTEDLOGFILE, "w"))
	resource = WSGIResource(reactor, reactor.getThreadPool(), app)
	site = Site(resource)

	reactor.listenTCP(TWISTEDPORT, site, interface="0.0.0.0")
	reactor.run()

# start a built in flask server
def builtin():
	print 'Built-in development server on port {port}...'.format(port=BUILTINPORT)
	app.run(host="0.0.0.0",port=BUILTINPORT,debug=True)

## END Start up Stuff


###############################VIEWS#######################################

##Health check 
@app.route("/status", methods=['GET'])
def status():
	ip = request.remote_addr #IP of visitor for logging
	return "{\"status\": \"OK\"}"

@app.route("/", methods=['GET'])
def index():
	head = "Hello World!"
	msg = "This is my flask template"
	company = "company name"
	return render_template("index.html",msg = msg, head = head, company = company)



################################ERROR VIEWS######################################
@app.errorhandler(400) 
def custom400(error):
	response = jsonify({'FAIL': error.description})
	return response


@app.errorhandler(403)
def error403(error):
	response = jsonify({'FAIL': error.description})
	return response

@app.errorhandler(404)
def error404(error):
	response = jsonify({'FAIL': error.description})
	return response


################################MAIN - RUN SETUP######################################
def startup():
	# find out if this is a twisted or builtin run 
	parser = optparse.OptionParser(usage="%prog [options]  or type %prog -h (--help)")
	parser.add_option('--twisted', help='Twisted event-driven web server', action="callback", callback=twisted, type="int");
	parser.add_option('--builtin', help='Built-in Flask web development server', action="callback", callback=builtin, type="int");
	(options, args) = parser.parse_args()
	parser.print_help()

if __name__ == "__main__":
	print("Starting")
	builtin() 