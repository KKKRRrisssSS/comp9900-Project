from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from app import app, system

POST = 'POST'
GET = 'GET'

@app.route('/dashboard')
@login_required
def dashboard():
    dashboards = {
        "admin": dashboard_admin,
        "student": dashboard_student
        }
    return dashboards[current_user.role]()
        
def dashboard_admin():
    """ Shows list of active surveys, closed surveys and list of questions """
    supervisors = system.view_all_supervisors()
    print(supervisors)
    return render_template("dashboard_admin.html", supervisors=supervisors)

def dashboard_student():
    """ Shows active, completed and closed surveys
        Active: Enrolled, not completed, not closed
        Completed: Enrolled, completed, not closed
        Closed: Enrolled, closed
    """
    records =system.get_current_incomplete_records()
    token = system.get_verify_token()
    return render_template("dashboard_user.html", records=records, role="student", verify_token=token)

@app.route('/approve/<username>', methods=[GET, POST])
@login_required
def approve_supervisor(username):
    print(username)
    system.approve_supervisor(username)
    return redirect(url_for('dashboard'))

@app.route('/disapprove/<username>', methods=[GET, POST])
@login_required
def disapprove_supervisor(username):
    print(username)
    system.disapprove_supervisor(username)
    return redirect(url_for('dashboard'))