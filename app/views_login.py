from flask import render_template, request, url_for, redirect
from flask_login import login_user, login_required, logout_user
from app import app, db1, system, views_dashboard, views_userprofile
import re 

# Make a regular expression 
# for validating an Email 
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

def check(email):  
    if(re.search(regex,email)):  
        return True 
          
    else:  
        return False


POST = 'POST'
GET = 'GET'

@app.route('/', methods=[GET])
def index():
    """ Splash page, does nothing much """
    return render_template('index.html')

@app.route('/login',methods=["GET","POST"]) 
def login():
    if request.method == "POST":
        """ User submits login details
            Redirect to dashboard if successful
            Return to login page if failed, display login failed
        """
        user_id = request.form["zID"]
        password = request.form["password"]
        if system.check_password(user_id, password):
            user = system.get_user(user_id)
            login_user(user)
            return redirect(request.args.get('next') or url_for('dashboard'))
        return render_template("login.html", login_failed=True)
    
    """ Login page, user can submit form with id and password """
    return render_template("login.html")

@app.route('/language')
@login_required
def language_processing():
    """ Logouts user, redirects to index """
    system.test_language_processing()
    return render_template("test.html")

@app.route('/register',methods=["GET","POST"]) 
def register():
    if request.method == POST:
        print('Post method recognised')
        data = request.form
        username = data['email_id']
        if(check(username) == False):
            return render_template('register.html')
        user = system.get_user(username)
        if (user is not None) :
            return render_template('register.html')
        system.add_user(data)
        system.create_user_documents(data)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """ Logouts user, redirects to index """
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html'), 404