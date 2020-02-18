from flask import render_template, request, jsonify, redirect, url_for, abort
from flask import safe_join, send_file
from flask_login import current_user, login_required
from app import app, system
import json


POST = 'POST'
GET = 'GET'

@app.route('/user', methods=[GET, POST])
@login_required
def user_profile():  
    if request.method == POST:
        print('Post method recognised')
        data = request.form
        system.update_user_profile(data)
        user_details = system.get_user_details()
        token = system.get_verify_token()
        return render_template("user.html", 
                            username=system.get_current_flask_user(),first_name=user_details['first_name'], last_name = user_details['last_name'], address_city = user_details['address_city'],
                            address = user_details['address'], address_state = user_details['address_state'], address_country = user_details['address_country'],
                            address_postcode = user_details['address_postcode'], current_cert_expiry_date = user_details['current_cert_expiry_date'], current_cert = user_details['current_certification'],
                            verify_token=token)

        
    user_details = system.get_user_details()
    token = system.get_verify_token()
    # user_data = system.get_json(user_details)
    #headers = {'content-type': 'application/json'}
    return render_template("user.html", 
                            username=system.get_current_flask_user(),first_name=user_details['first_name'], last_name = user_details['last_name'], address_city = user_details['address_city'],
                            address = user_details['address'], address_state = user_details['address_state'], address_country = user_details['address_country'],
                            address_postcode = user_details['address_postcode'], current_cert_expiry_date = user_details['current_cert_expiry_date'], current_cert = user_details['current_certification'],
                            verify_token=token)

@app.route('/file_upload', methods=[GET, POST])
@login_required
def file_upload():
    # if request.method == POST:
    #     print('Post method recognised')
    #     f = request.files['file']
    #     if f == None:
    #         print("file is none")
    #     print(f.filename)
    #     #data = request.form
    #     return render_template("not_found.html")
        #return redirect(url_for('language_processing'))
    user = system.get_current_flask_user()
    user_details =  system.get_user_details()
    record_name = ""
    active_log = system.get_current_active_logbook_id()
    record_size = system.get_current_active_logbook_record_size()
    record_name = active_log + '/record_' + str(record_size) 
    #record_name = active_log + '/record_7'
    print(user)
    print(record_name)
    token = system.get_verify_token()
    return render_template("file_list.html", user=user, record_name=record_name, verify_token=token)

@app.route('/file_test', methods=[GET,POST])
@login_required
def file_test():

    # if request.method == POST:
        # record_name = "record_1"
    record_name = ""
    active_log = system.get_current_active_logbook_id()
    record_size = system.get_current_active_logbook_record_size()
    record_name = active_log + '/record_' + str(record_size) 
    print('Post method recognised')
    print(record_name)
    f = request.files['file']
    if f == None:
        print("file is none")
    print(f.filename)
    record = system.language_processing(f, record_name)
    print(record)
    return redirect('http://127.0.0.1:7800/view_record/'+ record_name)
    # return render_template("not_found.html", record=record)


@app.route('/new_logbook', methods=[GET, POST])
@login_required
def new_logbook():
    if request.method == POST:
        data = request.form
        print(data)
        system.create_logbook(data)
        new_log_list = system.get_current_user_logbooks()
        print('new log_list')
        print(new_log_list)
        return render_template("new_logbook.html", logbooks=new_log_list)
    log_list = system.get_current_user_logbooks()
    print('log_list')
    print(log_list)
    token = system.get_verify_token()
    return render_template("new_logbook.html", logbooks=log_list, verify_token=token )

@app.route('/view_logbook/<logbook_name>', methods=[GET, POST])
@login_required
def view_logbook(logbook_name):
    print(logbook_name)
    if logbook_name =="none" or logbook_name == "":
        logbook_name = ""
        log_uid = system.get_current_active_logbook_id()
        print(log_uid)
   
    log_details = system.get_current_user_logbook_by_logname(logbook_name)
    if logbook_name != "":
        log_uid = system.get_logid_by_logname(logbook_name)
    print(log_uid)
    record_list = system.get_records_by_logbook_without_deleted(log_uid)
    print(log_details)
    print(record_list)
    incomplete_count = system.get_logbook_incomplete_count(log_uid)
    total_count = system.get_logbook_case_count(log_uid)
    print(str(incomplete_count) + "/" + str(total_count))
    token = system.get_verify_token()
    return render_template("record.html",log_details=log_details, records=record_list, logbook_name=logbook_name, 
                            incomplete_count=incomplete_count, total_count=total_count, verify_token=token)


@app.route('/delete_record/<log_id>/<record_index>', methods=[GET, POST])
@login_required
def delete_record(log_id, record_index):
    print('delete_rcord routing entered')
    record_name = log_id + "/" + record_index
    print(record_name)
    system.delete_record(record_name)
    return redirect(url_for('dashboard'))



@app.route('/view_record/<log_uid>/<record_index>', methods=[GET, POST])
@login_required
def view_record(log_uid, record_index):
    record_name = log_uid+'/'+record_index
    if request.method == POST:
        data = request.form
        print(data)
        system.update_record(data, record_name)
        record = system.get_record_list_by_name(record_name)
        print("------------------------RECORD DETAILs------------------------------")
        print(record)

        verify_token = system.get_verify_token()

        return render_template("view_record.html", dlp=record['DLP'], case_type=record['case_type'], doctor=record['co_reporting_doctor'], facility=record['facility'], 
                                is_cardiac=record['is_cardiac'], is_correlated=record['is_correlated'], is_gta=record['is_gta'], is_coronary=record['is_native_coronary'], 
                                patient=record['patient_details'], date=record['record_date'], status=record['record_status'], supervisor=record['supervisor_uid'], 
                                verify_token=verify_token)
    print(record_name)
    record= system.get_record_list_by_name(record_name)
    print("------------------------RECORD DETAILs------------------------------")
    print(record)
    verify_token = system.get_verify_token()

    return render_template("view_record.html", dlp=record['DLP'], case_type=record['case_type'], doctor=record['co_reporting_doctor'], facility=record['facility'], 
                                is_cardiac=record['is_cardiac'], is_correlated=record['is_correlated'], is_gta=record['is_gta'], is_coronary=record['is_native_coronary'], 
                                patient=record['patient_details'], date=record['record_date'], status=record['record_status'], supervisor=record['supervisor_uid'], 
                                verify_token=verify_token)



@app.route("/get-csv/<logbook_name>", methods=[GET, POST])
def get_csv(logbook_name):
    if logbook_name == "test":
        logbook_name = "test_logbooka2b"
    print(logbook_name)
    log_uid = system.get_logid_by_logname(logbook_name)
    print(log_uid)
    system.write_to_csv(log_uid)
    print('output.csv written')
    safe_path = safe_join(app.config["DATA_DIR"], "output.csv")
    
    try:
        render_template("file_downloaded.html")
        return send_file(safe_path, as_attachment=True, mimetype="text/csv")
    except FileNotFoundError:
        abort(404)            


@app.route("/supervisor", methods=[GET, POST])
def supervisor():
    username = system.get_current_flask_user()
    check = system.check_if_supervisor(username)
    print(check)
    if(check == True):
        records = system.get_completed_levelA_records()
        token = system.get_verify_token()
        return render_template("supervisor.html", records=records, verify_token=token)
    token = system.get_verify_token()
    return render_template("supervisor_error.html", verify_token=token)

@app.route('/approve_report/<log_id>/<record_index>', methods=[GET, POST])
@login_required
def approve_report(log_id, record_index):
    record_name = log_id + "/" + record_index
    print(record_name)
    system.approve_report(record_name)
    return redirect(url_for('supervisor'))

@app.route('/supervisor_view/<log_id>/<record_index>', methods=[GET, POST])
@login_required
def supervisor_view(log_id, record_index):
    record_name = log_id + "/" + record_index
    print(record_name)
    record = system.get_record_list_by_name(record_name)
    verify_token = system.get_verify_token()

    return render_template("supervisor_view.html", dlp=record['DLP'], case_type=record['case_type'], doctor=record['co_reporting_doctor'], facility=record['facility'], 
                        is_cardiac=record['is_cardiac'], is_correlated=record['is_correlated'], is_gta=record['is_gta'], is_coronary=record['is_native_coronary'], 
                        patient=record['patient_details'], date=record['record_date'], status=record['record_status'], supervisor=record['supervisor_uid'], 
                        verify_token=verify_token)
    

              
