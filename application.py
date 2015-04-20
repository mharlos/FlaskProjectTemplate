from flask import Flask, request, redirect, url_for, render_template, flash, send_file, abort, Response, jsonify



###############################CONFIG#######################################
#Flask Config
#http://flask.pocoo.org/
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
SERVERPORT = 5000

################################METHODS######################################
## Start up Stuff

# This gets the port to run on
def getPort(value):
	return (SERVERPORT, value)[value > 0]

# Start a twistd server
def twisted(option, opt_str, value, parser):
	print 'Twisted on port {port}...'.format(port=getPort(value))
	# Only import these if we need them
	from twisted.internet import reactor
	from twisted.web.server import Site
	from twisted.web.wsgi import WSGIResource

	resource = WSGIResource(reactor, reactor.getThreadPool(), app)
	site = Site(resource)

	reactor.listenTCP(getPort(value), site, interface="0.0.0.0")
	reactor.run()

# start a built in flask server
def builtin(option, opt_str, value, parser):
	print 'Built-in development server on port {port}...'.format(port=getPort(value))
	app.run(host="0.0.0.0",port=getPort(value),debug=True)

## END Start up Stuff


###############################VIEWS#######################################

##Health check 
@app.route("/status", methods=['GET'])
def status():
	ip = request.remote_addr #IP of visitor for logging
	return "{\"status\": \"OK\"}"

@app.route("/", methods=['GET'])
def index():
	return render_template("index.html")



################################ERROR VIEWS######################################
@app.errorhandler(400) 
def custom400(error):
    response = jsonify({'FAIL': error.description})
    return response


@app.errorhandler(403)
def error403(e):
	dmsg = ""
	return '403'

@app.errorhandler(404)
def error404(e):
	dmsg = ""
	return "404"


################################MAIN - RUN SETUP######################################
def startup():
	# find out if this is a twisted or builtin run 
	parser = optparse.OptionParser(usage="%prog [options]  or type %prog -h (--help)")
	parser.add_option('--twisted', help='Twisted event-driven web server', action="callback", callback=twisted, type="int");
	parser.add_option('--builtin', help='Built-in Flask web development server', action="callback", callback=builtin, type="int");
	(options, args) = parser.parse_args()
	parser.print_help()

if __name__ == "__main__":
	startup() 