from flask import Flask,render_template, request,jsonify,Response

# Router calls objetc
app = Flask(__name__)

#Add a single endpoint - testing
@app.route('/', methods = ['GET'])
def home():
    return render_template('log.html')

#When run from command line, start the server
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3333, debug=True)