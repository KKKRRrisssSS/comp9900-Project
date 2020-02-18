from flask import render_template, request, jsonify, redirect, url_for
from flask_login import current_user, login_required
from app import app, system

POST = 'POST'
GET = 'GET'

@app.route('/logbooks/new', methods=[GET, POST])
@login_required
def new_logbook():
    if current_user.role != "admin":
        return redirect(url_for('/dashboard'))

    if request.method == POST:
        data = request.form
        return render_template('completed.html')
    
    log = system.get_current_active_logbook
    records = system.get_records_by_logbook(log['log_uid'])
    return render_template('new_logbook.html', log=log, records=records)

@app.route('/complete/<record_id>', methods=[GET, POST])
@login_required
def complete_record(record_id):
    # check if current user can access
    record = system.get_record(record_id)
    if current_user.role != "student":
        return render_template("<h1>No Access</h1>")

    # check if exists or is expired and then process data
    if request.method == POST:
        data = request.form
        return render_template('completed.html')
    
    return render_template('display_completed_record.html', record=record)

@app.route('/view_logbook/<logbook_id>', methods=[GET])
@login_required
def view_logbook(logbook_id):
    log = system.get_logbook_by_id(logbook_id)
    if log == None:
        return render_template("<h1>No such logbook exists</h1>")
    return render_template('display_completed_logbook.html', log=log)