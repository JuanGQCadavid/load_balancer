from flask import Flask,render_template, request,jsonify,Response,redirect,url_for
from database import Database
import sys
# Router calls objetc
app = Flask(__name__)
db = None


#Add a single endpoint - testing
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if valid_login(username,password):
            return redirect(url_for('home'))
        return render_template('index.html')

    return render_template('index.html')

@app.route('/home', methods = ['GET'])
def home():
    return render_template('home.html')

@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        correo = request.form['correo']
        password = request.form['password']

        register_user(username,password,correo)

        return redirect(url_for('index'))
    return render_template('register.html')

def valid_login(username,password):
    print('LOG IN ->' , username, password)
    result = db.validUser(username,password)
    if result:
        return True
    else:
        return False

def register_user(username,password,email):
    print('REGISTER USER ->',username,password,email)
    result = db.registerUser(username,password,email)
    print(result)
    pass

#When run from command line, start the server
if __name__ == '__main__':
    global Database
    db = Database()
    try:
        debug=True
        if len(sys.argv) > 1:
            if sys.argv[1] == '-Dev':
                debug=False
        
        app.run(host = '0.0.0.0', port = 3333, debug=debug)
    except KeyboardInterrupt:
        print('Clossing server...')
        db.close_connection()
