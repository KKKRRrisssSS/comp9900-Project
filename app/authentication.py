from flask import redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from app import login_manager, system
# from firebase import auth

@login_manager.user_loader 
def load_user(user_id):
    return system.get_user(user_id)

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')

# def createUserWithEmailAndPassword(email, password):
#     firebase.auth().createUserWithEmailAndPassword(email, password)