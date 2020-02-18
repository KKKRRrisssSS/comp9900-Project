import dialogflow
import flask

from flask import Flask, request, make_response, jsonify

import requests

# initialize the flask app
app = Flask(__name__)

# default route
@app.route('/')
def index():
    return 'Hello World!'


# function for responses
def results():
    def check_user_by_token(user_token):
        '''http GET to USER database, requests for user binding check by user token,
           token exsists and user not binded -> return {'status':'success','username':'userxxx'},
           token not exsists -> return {'status':'token not found'},
           token exsists but user binded {'status':'user already binded','username':'userxxx'}
           '''
        print(user_token)
        response = requests.get(
            'http://127.0.0.1:7000/v1/user',
            params={'verify_token': user_token},
        ).json()
        if response['status']==1:
            return {'status':'token not found'}
        if response['status']==0 and response['body']['messenger_ID']==None:
            return {'status':'success','body':response['body']}
        if response['status']==0 and response['body']['messenger_ID']!=None:
            return {'status': 'user already binded', 'body': response['body']}


        return {'status':'success','username':'userxxx'}

    def check_user_by_sender_id(facebook_sender_id):
        '''http GET to USER database, requests for user binding check by sender id,
           user unbind -> return {'status':'sender id not found'},
           user binded -> return {'status':'success','username':'userxxx'}'''
        response = requests.get(
            'http://127.0.0.1:7000/v1/user',
            params={'messenger_ID': facebook_sender_id}).json()
        print(response)
        return response

    def bind_account(facebook_sender_id,user_token):
        '''http POST to USER database, bind facebook_sender_id with username related with user_token,
           binding successful -> return {'status':'success','username':'userxxx'}'''
        response = requests.post(
            f'http://127.0.0.1:7000/v1/user/{user_token}',
            params={'messenger_ID': facebook_sender_id},
        ).json()
        print(response)

        return {'status':'success','username':response['body']['username']}

    def cancel_account(facebook_sender_id):
        '''http POST to USER database, unbind facebook_sender_id with related username,
           binding successful -> return {'status':'success','username':'userxxx'}'''
        response = requests.post(
            f'http://127.0.0.1:7000/v1/user',
            params={'messenger_ID': facebook_sender_id,'field':'messenger_uid','value':'None'},
        ).json()
        print(response)

        return {'status': 'success', 'username': response['body']['username']}

    def check_active_logbook(username):
        '''http GET to Logbook database, check whether the given username have active logbook,
           have active logbook -> return {'status':'have active logbook,'logbook':'logbookID'},
           no active logbook -> return {'status':'no active logbook'}'''
        print('!!!!!!!!!!')
        response = requests.get(
            f'http://127.0.0.1:7000/v1/logbook/{username}/activated').json()
        print(response)
        if response['status']==1:
            return {'status':'no active logbook'}
        if response['status']==0:
            return {'status':'have active logbook','LogID':response['body']['LogID']}

    def create_new_logbook(username,program_uid,log_name):
        '''http PUT to logbook database, create a new logbook of given level,
           create successful -> return {'status':'success','logbook':'logbookID'}'''
        response = requests.put(
            f'http://127.0.0.1:7000/v1/logbook',
            params={'username': username, 'program_uid': program_uid,'log_name':log_name },
        ).json()
        print('12242',response)
        return {'status':'success','program_uid':program_uid}

    def delete_logbook(LogID):
        '''http DELETE to logbook database, delete a new logbook of given level,
           create successful -> return {'status':'success'}'''
        response = requests.post(
            f'http://127.0.0.1:7000/v1/logbook/{LogID}',
            params={'field': 'logStatus', 'value': 'deleted'},
        ).json()
        print(response)
        return {'status':'success'}

    def download_logbook(username):
        '''http GET to logbook database, get the url of excel version logbook,
           download successful -> return {'status':'success','url':'comp9900/user/logbook...'}'''
        return {'status': 'success', 'url': 'comp9900/user/logbook...'}

    def view_logbook_statistics(LogID):
        '''http GET to logbook database, get the statics of logbook,
           download successful -> return {'status':'success','casecount':'50','url':'comp9900/user/logbook...'}'''
        response = requests.get(f'http://127.0.0.1:7000/v1/logbook/{LogID}').json()
        return response

    def check_user_authority(username):
        '''http GET to user database, get check whether user is supervisor
            is supervisor -> return {'isSupervisor':True}
            is supervisor -> return {'isSupervisor':False}'''
        print('check!')
        response = requests.get(
            'http://127.0.0.1:7000/v1/user',
            params={'username': username}).json()
        if response['body']['isSupervisor']==True:
            print('aaaa')
            return {'isSupervisor': True}
        elif response['body']['isSupervisor']==False:
            print('bbbb')
            return {'isSupervisor': False}

    def check_record_to_be_confirmed(username):
        '''http GET to record database, get the list of case to be confirmed
            '''
        print(username)
        response = requests.get(
            f'http://127.0.0.1:7000/v1/user/a/{username}').json()
        print(response)
        return response


    def change_record_paramater(username,log_name,record_name,field,value):
        '''http POST to change record value of paramater
            success -> return {'status'='success'}'''
        if field not in ['DLP','record_date','facility','co_reporting_doctor','patient_details','case_type','is_correlated','is_gta','is_non_coronary','is_native_coronary','is_non_cardiac','is_cardiac','supervisor_uid',]:
            return {'status':2}

        response = requests.get(f'http://127.0.0.1:7000/v1/record/{username}/{log_name}/{record_name}').json()
        if response['status'] == 1:
            return {'status': 'record not found'}
        recordID = response['body']['RecordID']
        response = requests.post(
            f'http://127.0.0.1:7000/v1/record/{recordID}',
            params={'field': field, 'value': value},
        ).json()
        print(response)

        return  response

    def change_record_paramater_supervisor(username,log_name,record_name,field,value):
        '''http POST to change record value of paramater
            success -> return {'status'='success'}'''
        response = requests.get(f'http://127.0.0.1:7000/v1/record/{username}/{log_name}/{record_name}').json()
        if response['status'] == 1:
            return {'status': 1}
        recordID = response['body']['RecordID']
        response = requests.post(
            f'http://127.0.0.1:7000/v1/record/{recordID}',
            params={'field': field, 'value': value},
        ).json()
        print(response)

        return  response

    def check_record_parameter(parameter,username,log_name,record_name):
        '''http POST to change record value of paramater
            success -> return {'status'='success'}'''
        response = requests.get(f'http://127.0.0.1:7000/v1/record/{username}/{log_name}/{record_name}').json()
        print(111111111, response)
        if response['status'] == 1:
            print(1)
            return {'status': 1}
        recordID = response['body']['RecordID']
        response = requests.get(
            f'http://127.0.0.1:7000/v1/record/{recordID}').json()
        print(response)
        if response['status'] == 0:
            return {'status': 0, 'data': {parameter:response['body'][parameter]}}
        if response['status'] == 1:
            return {'status': 1}

    def check_record_all(username,log_name,record_name):
        response=requests.get(f'http://127.0.0.1:7000/v1/record/{username}/{log_name}/{record_name}').json()
        print(111111111,response)
        if response['status']==1:
            print(1)
            return {'status': 'record not found'}
        recordID=response['body']['RecordID']
        print(recordID)
        print(2)
        response = requests.get(
            f'http://127.0.0.1:7000/v1/record/{recordID}').json()
        print(3)
        print(response)
        if response['status']==0:
            return {'status': 'success', 'data': response['body']}
        if response['status']==1:
            return {'status': 'record not found'}

    def check_user_by_session_id(session_id):
        response = requests.get(
            f'http://127.0.0.1:7000/v1/session/{session_id}').json()
        print(response)
        return response



    def bind_user_by_session_id(session_id,username):
        response = requests.post(
            f'http://127.0.0.1:7000/v1/session/{session_id}',
            params={'username': username}).json()
        return response

    def check_user_by_token_web_demo(user_token):
        '''http GET to USER database, requests for user binding check by user token,
           token exsists and user not binded -> return {'status':'success','username':'userxxx'},
           token not exsists -> return {'status':'token not found'},
           token exsists but user binded {'status':'user already binded','username':'userxxx'}
           '''
        print(user_token)
        response = requests.get(
            'http://127.0.0.1:7000/v1/user',
            params={'verify_token': user_token},
        ).json()
        if response['status']==1:
            return {'status':'token not found'}
        if response['status']==0:
            return {'status':'success','body':response['body']}






    # build a request object
    req = request.get_json(force=True)
    print(req)
    print(req['queryResult']['intent'])
    #print(req['queryResult']['originalDetectIntentRequest'])
    try:
        a=req['originalDetectIntentRequest']['source']
        flag=1
    except KeyError:
        flag=0

    if flag==1:
        intent=req['queryResult']['intent']['displayName']
        for i in range(len(req['queryResult']['outputContexts'])):
            try:
                facebook_sender_id = int(req['queryResult']['outputContexts'][i]['parameters']['facebook_sender_id'])
            except:
                continue
            index=i
            break

        '''try:
            facebook_sender_id = int(req['queryResult']['outputContexts'][0]['parameters']['facebook_sender_id'])
        except KeyError:
            facebook_sender_id = int(req['queryResult']['outputContexts'][1]['parameters']['facebook_sender_id'])'''
        if intent=='Default Welcome Intent':
            print(facebook_sender_id)
            rsp_check_user_by_sender_id = check_user_by_sender_id(facebook_sender_id)
            if rsp_check_user_by_sender_id['status']==1:
                return {'fulfillmentText': f"Welcome, new user!\n I am CTCA Logbook Assistant, which can help you manage your CTCA Logbook!\n You haven\'t bind your account with me yet.\n For further operation, please bind your account with me first by sending 'bind messenger chatbot'"}
            if rsp_check_user_by_sender_id['status']==0:
                return {'fulfillmentText':f'Welcome back {rsp_check_user_by_sender_id["body"]["first_name"]} {rsp_check_user_by_sender_id["body"]["last_name"]}'}
        if intent=='BindAccount':
            rsp_check_user_by_sender_id=check_user_by_sender_id(facebook_sender_id)
            if rsp_check_user_by_sender_id['status']==0:
                print(11111111)
                return {'fulfillmentText': f'Sorry, I am already binded with account {rsp_check_user_by_sender_id["body"]["username"]}.\n If you want to bind another account, please cancel first by sending "Cancel Binding"'}
            user_token=req['queryResult']['parameters']['user_token']
            rsp_check_user_by_token=check_user_by_token(user_token)
            print(22222)
            if rsp_check_user_by_token['status']=='token not found':
                return {'fulfillmentText': f'Sorry, the token you sent is invalid, please try again.'}
            if rsp_check_user_by_token['status']=='user already binded':
                return {'fulfillmentText': f'Sorry, the account {rsp_check_user_by_token["body"]["username"]} is already binded with other bots, please unbind the account first.'}
            if rsp_check_user_by_token['status']=='success':
                return {'fulfillmentText': f'You want to bind account {rsp_check_user_by_token["body"]["username"]} with me, are you sure?'}

        if intent=='BindAccount - yes':
            user_token = req['queryResult']['outputContexts'][index]['parameters']['user_token']
            rsp_check_user_by_token=check_user_by_token(user_token)
            rsp_bind_account=bind_account(facebook_sender_id, user_token)
            return {'fulfillmentText': f'Great! Your account {rsp_bind_account["username"]} is binded with me now'}
        if intent=='BindAccount - no':
            return {'fulfillmentText': f'Well, I am still not bind with any account'}

        rsp_check_user_by_sender_id=check_user_by_sender_id(facebook_sender_id)
        if rsp_check_user_by_sender_id['status']==1:
            return {'fulfillmentText': 'Sorry, You haven\'t bind your account with me yet.\n For further operation, please bind your account with me first by sending "bind messenger chatbot".'}

        username=rsp_check_user_by_sender_id['body']['username']
        print('USERNAME!!!!!!!!',username)
        if intent=='CancelBinding':
            return {'fulfillmentText': f'You want to unbind your account {username}, are you sure?'}
        if intent=='cancel_binding - yes':
            rsp_cancel_account = cancel_account(facebook_sender_id)
            return {'fulfillmentText': f'Done, your account {username} is unbind with me now'}
        if intent=='cancel_binding - no':
            return {'fulfillmentText': f'Well, your account {username} is still binding with me now'}

        if intent=='CreateLogbook':
            rsp_check_active_logbook=check_active_logbook(username)
            print(rsp_check_active_logbook)
            if rsp_check_active_logbook['status']=='have active logbook':
                return {'fulfillmentText': f'Oops,You already have an active logbook, new logbook cannot be created.'}
            if rsp_check_active_logbook['status']=='no active logbook':
                return {'fulfillmentText': f'You are going to create a new logbook, are you sure?'}
        if intent=='CreateLogbook - no':
            return {'fulfillmentText': f"Well, I didn\'t create new logbook for you"}
        if intent == 'CreateLogbook - yes':
            #certificationLevel = req['queryResult']['outputContexts'][index]['parameters']['CertificationLevel']
            program_uid=req['queryResult']['outputContexts'][index]['parameters']['Program']
            log_name = req['queryResult']['outputContexts'][index]['parameters']['log_name']
            rsp_create_new_logbook=create_new_logbook(username,program_uid,log_name)
            return {'fulfillmentText': f"Great, I have created a new {program_uid} logbook for you!"}

        if intent=='DeleteLogbook':
            rsp_check_active_logbook = check_active_logbook(username)
            print(rsp_check_active_logbook)
            if rsp_check_active_logbook['status'] == 'have active logbook':
                return {'fulfillmentText': f'You have a logbook , are you sure you want to delete it?'}
            if rsp_check_active_logbook['status'] == 'no active logbook':
                return {'fulfillmentText': f'Oops, you don\'t have any active logbook, so you cannot delete'}
        if intent=='DeleteLogbook - yes':
            LogID=check_active_logbook(username)['LogID']
            rsp_delete_logbook=delete_logbook(LogID)
            return {'fulfillmentText': f"Great, I have deleted the active logbook for you!"}
        if intent=='DeleteLogbook - no':
            return {'fulfillmentText': f"Well, I didn\'t delete logbook for you"}

        if intent=='DownloadLogbook':
            rsp_check_active_logbook = check_active_logbook(username)
            if rsp_check_active_logbook['status'] == 'have active logbook':
                LogID=rsp_check_active_logbook['LogID']
                rsp_download_logbook=download_logbook(username)
                return {'fulfillmentText':f"You can download your logbook in the following link:\n{rsp_download_logbook['url']}"}
            if rsp_check_active_logbook['status'] == 'no active logbook':
                return {'fulfillmentText':f'Sorry you currently don\'t have any active logbook, so you can not download anything.'}

        if intent == 'ViewLogbookStatics':
            rsp_check_active_logbook = check_active_logbook(username)
            if rsp_check_active_logbook['status'] == 'no active logbook':
                return {
                    'fulfillmentText': f'Sorry you currently don\'t have any active logbook, so you can not view anything.'}
            if rsp_check_active_logbook['status'] == 'have active logbook':
                LogID = check_active_logbook(username)['LogID']
                rsp_view_logbook_statistics = view_logbook_statistics(LogID)
                print(rsp_view_logbook_statistics)
                return {'fulfillmentText': f"[Logbook Name]:{rsp_view_logbook_statistics['body']['log_name']}\n[Total Case Count]:{rsp_view_logbook_statistics['body']['total_case_count']}\n[Live Case Count]:{rsp_view_logbook_statistics['body']['live_case_count']}\n[Library Case Count]:{rsp_view_logbook_statistics['body']['library_case_count']}\n[Live Course Case Count]:{rsp_view_logbook_statistics['body']['live_case_course_count']}\n[correlated_case_count]:{rsp_view_logbook_statistics['body']['correlated_case_count']}\n[GTA Count]:{rsp_view_logbook_statistics['body']['gta_count']}\n[Native Coronary Count]:{rsp_view_logbook_statistics['body']['native_coronary_count']}\n[Non Cardiac Count]:{rsp_view_logbook_statistics['body']['non_cardiac_count']}\n[Non Coronary Count]:{rsp_view_logbook_statistics['body']['non_coronary_count']}"}

        if intent=='SupervisorRecordsToBeConfirmed':
            rsp_check_user_authority=check_user_authority(username)
            print(rsp_check_user_authority['isSupervisor']==False)
            print('s')
            if rsp_check_user_authority['isSupervisor']==False:
                return {'fulfillmentText':f'Sorry you are not certificated Supervisor'}
            rsp_check_record_to_be_confirmed=check_record_to_be_confirmed(username)
            print(rsp_check_record_to_be_confirmed)
            if rsp_check_record_to_be_confirmed['status']==1:
                return {'fulfillmentText':f'No cases to be confirmed'}
            returnString=''
            for i in rsp_check_record_to_be_confirmed['body']:
                rec_string=f"[User]:{i['user_email']}\n[Log Name]:{i['log_name']}\n[Record Name]:{i['record_index']}\n[Upload Time]:{i['upload_time']}\n===================\n"
                returnString+=rec_string
            return {'fulfillmentText':f"{returnString}"}


        if intent == 'SupervisorCheckRecord':
            student_email = req['queryResult']['outputContexts'][i]['parameters']['student_email']
            record_name = req['queryResult']['outputContexts'][i]['parameters']['record_name']
            log_name = req['queryResult']['outputContexts'][i]['parameters']['log_name']
            rsp_check_user_authority = check_user_authority(username)
            if rsp_check_user_authority['isSupervisor']== False:
                return {'fulfillmentText': f'Sorry you are not certificated Supervisor'}
            rsp_check_record_parameter=check_record_parameter('supervisor_uid',student_email,log_name,record_name)
            print(rsp_check_record_parameter)
            if rsp_check_record_parameter['status']==1:
                return {'fulfillmentText': f'No such record ID, please try again.'}
            rsp_check_record_all=check_record_all(username,log_name,record_name)
            return {'fulfillmentText': f"[Log_name]:{rsp_check_record_all['data']['log_name']}\n[Record Name]:{rsp_check_record_all['data']['record_name']}\n[DLP]:{rsp_check_record_all['data']['DLP']}\n[Case Type]:{rsp_check_record_all['data']['case_type']}\n[Co-reporting Doctor]:{rsp_check_record_all['data']['co_reporting_doctor']}\n[Facility]:{rsp_check_record_all['data']['facility']}\n[Patient Detail]:{rsp_check_record_all['data']['patient_details']}\n[Is Cardiac]:{rsp_check_record_all['data']['is_cardiac']}\n[Is Correlated]:{rsp_check_record_all['data']['is_correlated']}\n[Is GTA]:{rsp_check_record_all['data']['is_gta']}\n[Is Native Coronary]:{rsp_check_record_all['data']['is_native_coronary']}\n[is_non_cardiac]:{rsp_check_record_all['data']['is_non_cardiac']}\n[Is Non Coronary]:{rsp_check_record_all['data']['is_non_coronary']}\n[URL]:{rsp_check_record_all['data']['user_email']}\nAre you sure you want to approve?"}
        if intent == 'SupervisorCheckRecord - cancel':
            return {'fulfillmentText': 'you didn\'t do anything'}
        if intent == 'SupervisorCheckRecord - refuse':
            student_email = req['queryResult']['outputContexts'][i]['parameters']['student_email']
            record_name = req['queryResult']['outputContexts'][i]['parameters']['record_name']
            log_name = req['queryResult']['outputContexts'][i]['parameters']['log_name']
            rsp_change_record_status=change_record_paramater_supervisor(student_email,log_name,record_name,'is_approved','rejected')
            return {'fulfillmentText':'rejected'}
        if intent == 'SupervisorCheckRecord - approve':
            student_email = req['queryResult']['outputContexts'][i]['parameters']['student_email']
            record_name = req['queryResult']['outputContexts'][i]['parameters']['record_name']
            log_name = req['queryResult']['outputContexts'][i]['parameters']['log_name']
            rsp_change_record_status=change_record_paramater_supervisor(student_email,log_name,record_name,'is_approved',True)
            return {'fulfillmentText':'confirmed'}

        if intent== 'UploadRecord':
            rsp_check_active_logbook = check_active_logbook(username)
            if rsp_check_active_logbook['status'] == 'no active logbook':
                return {'fulfillmentText': f'Oops, you don\'t have any active logbook, so you cannot upload case'}
            LogID = rsp_check_active_logbook['LogID']
            return {'fulfillmentText': f"http://127.0.0.1:7800/file_upload , please go to this url to upload your case. After uploaded, please memorize your RecordID, then send 'Upload finished + [RecordID]'to me."}
        if intent == 'UploadRecord - uploaded':
            record_name=req['queryResult']['outputContexts'][index]['parameters']['record_name']
            log_name = req['queryResult']['outputContexts'][index]['parameters']['log_name']
            print('****************')
            #print(recordID)
            print(username)


            rsp_check_record_all=check_record_all(username,log_name,record_name)
            rsp_check_active_logbook=check_active_logbook(username)
            LogID=rsp_check_active_logbook['LogID']

            if rsp_check_record_all['status']=='record not found':
                return {'fulfillmentText':'Record Not Found'}
            #####if logid doesn't match recordid

            if rsp_check_record_all['status']=='success' and rsp_check_record_all['data']['log_uid']!=LogID:
                return {'fulfillmentText':f"this record is not in your current active logbook"}


            if rsp_check_record_all['status']=='success' and rsp_check_record_all['data']['log_uid']==LogID:
                print(rsp_check_record_all)
                return {'fulfillmentText': f"[Log_name]:{rsp_check_record_all['data']['log_name']}\n[Record Name]:{rsp_check_record_all['data']['record_name']}\n[DLP]:{rsp_check_record_all['data']['DLP']}\n[Case Type]:{rsp_check_record_all['data']['case_type']}\n[Co-reporting Doctor]:{rsp_check_record_all['data']['co_reporting_doctor']}\n[Facility]:{rsp_check_record_all['data']['facility']}\n[Patient Detail]:{rsp_check_record_all['data']['patient_details']}\n[Is Cardiac]:{rsp_check_record_all['data']['is_cardiac']}\n[Is Correlated]:{rsp_check_record_all['data']['is_correlated']}\n[Is GTA]:{rsp_check_record_all['data']['is_gta']}\n[Is Native Coronary]:{rsp_check_record_all['data']['is_native_coronary']}\n[is_non_cardiac]:{rsp_check_record_all['data']['is_non_cardiac']}\n[Is Non Coronary]:{rsp_check_record_all['data']['is_non_coronary']}\n[URL]:{rsp_check_record_all['data']['user_email']}"}



        if intent== 'UpdateRecord':
            fields = {'0': 'DLP', '1': 'record_date', '2': 'facility', '3': 'co_reporting_doctor',
                      '4': 'patient_details',
                      '5': 'case_type', '6': 'is_correlated', '7': 'is_gta', '8': 'is_non_coronary',
                      '9': 'is_native_coronary', '10': 'is_cardiac', '11': 'is_non_cardiac'}


            rsp_check_active_logbook = check_active_logbook(username)
            record_name = req['queryResult']['outputContexts'][index]['parameters']['record_name']
            log_name = req['queryResult']['outputContexts'][index]['parameters']['log_name']
            field = req['queryResult']['outputContexts'][index]['parameters']['field']

            if field not in fields.keys():
                return {'fulfillmentText': f"No such field called {field}"}
            if rsp_check_active_logbook['status'] == 'no active logbook':
                return {'fulfillmentText': f'Sorry you currently don\'t have any active logbook, so you can not view anything.'}
            if rsp_check_active_logbook['status'] == 'have active logbook':
                rsp_check_record_all=check_record_all(username,log_name,record_name)
                if rsp_check_record_all['status'] == 'record not found':
                    return {'fulfillmentText': 'Record Not Found'}
                if rsp_check_record_all['status'] == 'success' and rsp_check_record_all['data']['record_status'] in ['rejected','confirmed']:
                    return {'fulfillmentText': f"This record is already {rsp_check_record_all['data']['record_status']}, you cannot change it's value now"}
                else:
                    return {'fulfillmentText': f"[Log_name]:{rsp_check_record_all['data']['log_name']}\n[Record Name]:{rsp_check_record_all['data']['record_name']}\n[DLP]:{rsp_check_record_all['data']['DLP']}\n[Case Type]:{rsp_check_record_all['data']['case_type']}\n[Co-reporting Doctor]:{rsp_check_record_all['data']['co_reporting_doctor']}\n[Facility]:{rsp_check_record_all['data']['facility']}\n[Patient Detail]:{rsp_check_record_all['data']['patient_details']}\n[Is Cardiac]:{rsp_check_record_all['data']['is_cardiac']}\n[Is Correlated]:{rsp_check_record_all['data']['is_correlated']}\n[Is GTA]:{rsp_check_record_all['data']['is_gta']}\n[Is Native Coronary]:{rsp_check_record_all['data']['is_native_coronary']}\n[is_non_cardiac]:{rsp_check_record_all['data']['is_non_cardiac']}\n[Is Non Coronary]:{rsp_check_record_all['data']['is_non_coronary']}\n[URL]:{rsp_check_record_all['data']['user_email']}\n,are you sure you want to update?"}

        if intent== 'UpdateRecord - yes':
            fields = {'0': 'DLP', '1': 'record_date', '2': 'facility', '3': 'co_reporting_doctor', '4': 'patient_details',
                      '5': 'case_type', '6': 'is_correlated', '7': 'is_gta', '8': 'is_non_coronary',
                      '9': 'is_native_coronary', '10': 'is_cardiac', '11': 'is_non_cardiac'}
            record_name = req['queryResult']['outputContexts'][index]['parameters']['record_name']
            log_name = req['queryResult']['outputContexts'][index]['parameters']['log_name']
            field = fields[req['queryResult']['outputContexts'][index]['parameters']['field']]
            value = req['queryResult']['outputContexts'][index]['parameters']['value']
            rsp_change_record_paramater=change_record_paramater(username,log_name,record_name,field,value)
            print(rsp_change_record_paramater)
            if rsp_change_record_paramater['status']==0:
                return {'fulfillmentText': f"{field} has been updated as {value}"}
            if rsp_change_record_paramater['status']==2:
                return {'fulfillmentText': f"No such field called {field}"}
        if intent == 'UpdateRecord - no':
            return {'fulfillmentText': f"I didn't change value for you"}

        if intent== 'viewRecord':
            record_name = req['queryResult']['outputContexts'][0]['parameters']['record_name']
            log_name = req['queryResult']['outputContexts'][0]['parameters']['log_name']
            rsp_check_record_all = check_record_all(username, log_name, record_name)
            if rsp_check_record_all['status'] == 'record not found':
                return {'fulfillmentText': 'Record Not Found'}
            else:
                return {'fulfillmentText': f"[Log_name]:{rsp_check_record_all['data']['log_name']}\n[Record Name]:{rsp_check_record_all['data']['record_name']}\n[DLP]:{rsp_check_record_all['data']['DLP']}\n[Case Type]:{rsp_check_record_all['data']['case_type']}\n[Co-reporting Doctor]:{rsp_check_record_all['data']['co_reporting_doctor']}\n[Facility]:{rsp_check_record_all['data']['facility']}\n[Patient Detail]:{rsp_check_record_all['data']['patient_details']}\n[Is Cardiac]:{rsp_check_record_all['data']['is_cardiac']}\n[Is Correlated]:{rsp_check_record_all['data']['is_correlated']}\n[Is GTA]:{rsp_check_record_all['data']['is_gta']}\n[Is Native Coronary]:{rsp_check_record_all['data']['is_native_coronary']}\n[is_non_cardiac]:{rsp_check_record_all['data']['is_non_cardiac']}\n[Is Non Coronary]:{rsp_check_record_all['data']['is_non_coronary']}\n[URL]:{rsp_check_record_all['data']['user_email']}"}


    if flag==0:
        session_id=req['session'].split('/')[-1]
        print('================SESSION==============')
        print(session_id)
        #return {'fulfillmentText': f"Hello you are using our chatbot from website, please send bind from web to tell me who you are"}
        intent = req['queryResult']['intent']['displayName']
        print('intent',intent)
        if intent == 'Default Welcome Intent':
            #print(facebook_sender_id)
            rsp_check_user_by_session_id=check_user_by_session_id(session_id)

            if rsp_check_user_by_session_id['status'] == 1:
                return {
                    'fulfillmentText': f"Welcome!\n I am CTCA Logbook Assistant, which can help you manage your CTCA Logbook!\n For further operation, please bind your account with me first by sending 'bind webpage chatbot'"}
            if rsp_check_user_by_session_id['status'] == 0:
                return {'fulfillmentText': f'Welcome back {rsp_check_user_by_session_id["body"]["username"]} '}
        if intent=='bind_webpage':
            rsp_check_user_by_session_id = check_user_by_session_id(session_id)
            print(rsp_check_user_by_session_id)
            if rsp_check_user_by_session_id['status'] == 0:
                return {'fulfillmentText': f'Sorry I\'m alreary binded with {rsp_check_user_by_session_id["body"]["username"]} '}
            if rsp_check_user_by_session_id['status'] == 1:
                verify_token=req['queryResult']['parameters']['verify_token']
                rsp_check_user_by_token_web_demo = check_user_by_token_web_demo(verify_token)
                print(verify_token)
                print(rsp_check_user_by_token_web_demo)
                if rsp_check_user_by_token_web_demo['status'] == 'token not found':
                    return {'fulfillmentText': f'Sorry, the token you sent is invalid, please try again.'}
                username = rsp_check_user_by_token_web_demo['body']['username']
                if rsp_check_user_by_token_web_demo['status'] == 'success':
                    verify_token = req['queryResult']['outputContexts'][0]['parameters']['verify_token']
                    rsp_check_user_by_token_web_demo = check_user_by_token_web_demo(verify_token)
                    username = rsp_check_user_by_token_web_demo['body']['username']
                    bind_user_by_session_id = bind_user_by_session_id(session_id, username)
                    return {'fulfillmentText': f'Great! Your account {username} is binded with me now'}
                    #return {'fulfillmentText': f'You want to bind account {username} with me, are you sure?'}
        '''if intent=='bind_webpage - yes':
            print('yes')
            verify_token = req['queryResult']['outputContexts'][0]['parameters']['verify_token']
            rsp_check_user_by_token_web_demo=check_user_by_token_web_demo(verify_token)
            username=rsp_check_user_by_token_web_demo['body']['username']
            bind_user_by_session_id=bind_user_by_session_id(session_id, username)
            return {'fulfillmentText': f'Great! Your account {username} is binded with me now'}
        if intent=='bind_webpage - no':
            print('no')
            return {'fulfillmentText': f'Well, I am still not bind with any account'}'''
        rsp_check_user_by_session_id = check_user_by_session_id(session_id)
        if rsp_check_user_by_session_id['status'] == 1:
            return {'fulfillmentText': f"You didn't binded with any of Account,For further operation, please bind your account with me first by sending 'bind webpage chatbot'"}
        username = rsp_check_user_by_session_id['body']['username']
        if intent=='CreateLogbook':
            rsp_check_active_logbook=check_active_logbook(username)
            print(rsp_check_active_logbook)
            if rsp_check_active_logbook['status']=='have active logbook':
                return {'fulfillmentText': f'Oops,You already have an active logbook, new logbook cannot be created.'}
            if rsp_check_active_logbook['status']=='no active logbook':
                return {'fulfillmentText': f'You are going to create a new logbook, are you sure?'}
        if intent=='CreateLogbook - no':
            return {'fulfillmentText': f"Well, I didn\'t create new logbook for you"}
        if intent == 'CreateLogbook - yes':
            #certificationLevel = req['queryResult']['outputContexts'][index]['parameters']['CertificationLevel']
            program_uid=req['queryResult']['outputContexts'][0]['parameters']['Program']
            log_name = req['queryResult']['outputContexts'][0]['parameters']['log_name']
            rsp_create_new_logbook=create_new_logbook(username,program_uid,log_name)
            return {'fulfillmentText': f"Great, I have created a new {program_uid} logbook for you!"}

        if intent=='DeleteLogbook':
            rsp_check_active_logbook = check_active_logbook(username)
            print(rsp_check_active_logbook)
            if rsp_check_active_logbook['status'] == 'have active logbook':
                return {'fulfillmentText': f'You have a logbook , are you sure you want to delete it?'}
            if rsp_check_active_logbook['status'] == 'no active logbook':
                return {'fulfillmentText': f'Oops, you don\'t have any active logbook, so you cannot delete'}
        if intent=='DeleteLogbook - yes':
            LogID=check_active_logbook(username)['LogID']
            rsp_delete_logbook=delete_logbook(LogID)
            return {'fulfillmentText': f"Great, I have deleted the active logbook for you!"}
        if intent=='DeleteLogbook - no':
            return {'fulfillmentText': f"Well, I didn\'t delete logbook for you"}

        if intent=='DownloadLogbook':
            rsp_check_active_logbook = check_active_logbook(username)
            if rsp_check_active_logbook['status'] == 'have active logbook':
                LogID=rsp_check_active_logbook['LogID']
                rsp_download_logbook=download_logbook(username)
                return {'fulfillmentText':f"You can download your logbook in the following link:\n{rsp_download_logbook['url']}"}
            if rsp_check_active_logbook['status'] == 'no active logbook':
                return {'fulfillmentText':f'Sorry you currently don\'t have any active logbook, so you can not download anything.'}

        if intent=='ViewLogbookStatics':
            rsp_check_active_logbook = check_active_logbook(username)
            if rsp_check_active_logbook['status'] == 'no active logbook':
                return {'fulfillmentText':f'Sorry you currently don\'t have any active logbook, so you can not view anything.'}
            if rsp_check_active_logbook['status'] == 'have active logbook':
                LogID = check_active_logbook(username)['LogID']
                rsp_view_logbook_statistics=view_logbook_statistics(LogID)
                print(rsp_view_logbook_statistics)
                return {'fulfillmentText': f"[Logbook Name]:{rsp_view_logbook_statistics['body']['log_name']}\n[Total Case Count]:{rsp_view_logbook_statistics['body']['total_case_count']}\n[Live Case Count]:{rsp_view_logbook_statistics['body']['live_case_count']}\n[Library Case Count]:{rsp_view_logbook_statistics['body']['library_case_count']}\n[Live Course Case Count]:{rsp_view_logbook_statistics['body']['live_case_course_count']}\n[correlated_case_count]:{rsp_view_logbook_statistics['body']['correlated_case_count']}\n[GTA Count]:{rsp_view_logbook_statistics['body']['gta_count']}\n[Native Coronary Count]:{rsp_view_logbook_statistics['body']['native_coronary_count']}\n[Non Cardiac Count]:{rsp_view_logbook_statistics['body']['non_cardiac_count']}\n[Non Coronary Count]:{rsp_view_logbook_statistics['body']['non_coronary_count']}\n"}

        if intent == 'SupervisorRecordsToBeConfirmed':
            rsp_check_user_authority = check_user_authority(username)
            print(rsp_check_user_authority['isSupervisor'] == False)
            print('s')
            if rsp_check_user_authority['isSupervisor'] == False:
                return {'fulfillmentText': f'Sorry you are not certificated Supervisor'}
            rsp_check_record_to_be_confirmed = check_record_to_be_confirmed(username)
            print(rsp_check_record_to_be_confirmed)
            if rsp_check_record_to_be_confirmed['status'] == 1:
                return {'fulfillmentText': f'No cases to be confirmed'}
            returnString = ''
            for i in rsp_check_record_to_be_confirmed['body']:
                rec_string = f"[User]:{i['user_email']}\n[Log Name]:{i['log_name']}\n[Record Name]:{i['record_index']}\n[Upload Time]:{i['upload_time']}\n===================\n"
                returnString += rec_string
            return {'fulfillmentText': f"{returnString}"}

        if intent == 'SupervisorCheckRecord':
            student_email = req['queryResult']['outputContexts'][0]['parameters']['student_email']
            record_name = req['queryResult']['outputContexts'][0]['parameters']['record_name']
            log_name = req['queryResult']['outputContexts'][0]['parameters']['log_name']
            rsp_check_user_authority = check_user_authority(username)
            if rsp_check_user_authority['isSupervisor'] == False:
                return {'fulfillmentText': f'Sorry you are not certificated Supervisor'}
            rsp_check_record_parameter = check_record_parameter('supervisor_uid', student_email, log_name, record_name)
            print(rsp_check_record_parameter)
            if rsp_check_record_parameter['status'] == 1:
                return {'fulfillmentText': f'No such record ID, please try again.'}
            rsp_check_record_all = check_record_all(username, log_name, record_name)
            return {'fulfillmentText': f"[Log_name]:{rsp_check_record_all['data']['log_name']}\n[Record Name]:{rsp_check_record_all['data']['record_name']}\n[DLP]:{rsp_check_record_all['data']['DLP']}\n[Case Type]:{rsp_check_record_all['data']['case_type']}\n[Co-reporting Doctor]:{rsp_check_record_all['data']['co_reporting_doctor']}\n[Facility]:{rsp_check_record_all['data']['facility']}\n[Patient Detail]:{rsp_check_record_all['data']['patient_details']}\n[Is Cardiac]:{rsp_check_record_all['data']['is_cardiac']}\n[Is Correlated]:{rsp_check_record_all['data']['is_correlated']}\n[Is GTA]:{rsp_check_record_all['data']['is_gta']}\n[Is Native Coronary]:{rsp_check_record_all['data']['is_native_coronary']}\n[is_non_cardiac]:{rsp_check_record_all['data']['is_non_cardiac']}\n[Is Non Coronary]:{rsp_check_record_all['data']['is_non_coronary']}\n[URL]:{rsp_check_record_all['data']['user_email']}\nAre you sure you want to approve?"}
        if intent == 'SupervisorCheckRecord - cancel':
            return {'fulfillmentText': 'you didn\'t do anything'}
        if intent == 'SupervisorCheckRecord - refuse':
            student_email = req['queryResult']['outputContexts'][0]['parameters']['student_email']
            record_name = req['queryResult']['outputContexts'][0]['parameters']['record_name']
            log_name = req['queryResult']['outputContexts'][0]['parameters']['log_name']
            rsp_change_record_status = change_record_paramater_supervisor(student_email, log_name, record_name,
                                                                          'is_approved', 'rejected')
            return {'fulfillmentText': 'rejected'}
        if intent == 'SupervisorCheckRecord - approve':
            student_email = req['queryResult']['outputContexts'][0]['parameters']['student_email']
            record_name = req['queryResult']['outputContexts'][0]['parameters']['record_name']
            log_name = req['queryResult']['outputContexts'][0]['parameters']['log_name']
            rsp_change_record_status = change_record_paramater_supervisor(student_email, log_name, record_name,
                                                                          'is_approved', True)
            return {'fulfillmentText': 'confirmed'}

        if intent== 'UploadRecord':
            rsp_check_active_logbook = check_active_logbook(username)
            if rsp_check_active_logbook['status'] == 'no active logbook':
                return {'fulfillmentText': f'Oops, you don\'t have any active logbook, so you cannot upload case'}
            LogID = rsp_check_active_logbook['LogID']
            return {'fulfillmentText': f"http://127.0.0.1:7800/file_upload , please go to this url to upload your case. After uploaded, please memorize your RecordID, then send 'Upload finished + [RecordID]'to me."}
        if intent == 'UploadRecord - uploaded':
            record_name=req['queryResult']['outputContexts'][0]['parameters']['record_name']
            log_name = req['queryResult']['outputContexts'][0]['parameters']['log_name']
            print('****************')
            #print(recordID)
            print(username)
            rsp_check_record_all=check_record_all(username,log_name,record_name)
            rsp_check_active_logbook=check_active_logbook(username)
            LogID=rsp_check_active_logbook['LogID']

            if rsp_check_record_all['status']=='record not found':
                return {'fulfillmentText':'Record Not Found'}
            #####if logid doesn't match recordid

            if rsp_check_record_all['status']=='success' and rsp_check_record_all['data']['log_uid']!=LogID:
                return {'fulfillmentText':f"this record is not in your current active logbook"}


            if rsp_check_record_all['status']=='success' and rsp_check_record_all['data']['log_uid']==LogID:
                print(rsp_check_record_all)
                return {'fulfillmentText': f"[Log_name]:{rsp_check_record_all['data']['log_name']}\n[Record Name]:{rsp_check_record_all['data']['record_name']}\n[DLP]:{rsp_check_record_all['data']['DLP']}\n[Case Type]:{rsp_check_record_all['data']['case_type']}\n[Co-reporting Doctor]:{rsp_check_record_all['data']['co_reporting_doctor']}\n[Facility]:{rsp_check_record_all['data']['facility']}\n[Patient Detail]:{rsp_check_record_all['data']['patient_details']}\n[Is Cardiac]:{rsp_check_record_all['data']['is_cardiac']}\n[Is Correlated]:{rsp_check_record_all['data']['is_correlated']}\n[Is GTA]:{rsp_check_record_all['data']['is_gta']}\n[Is Native Coronary]:{rsp_check_record_all['data']['is_native_coronary']}\n[is_non_cardiac]:{rsp_check_record_all['data']['is_non_cardiac']}\n[Is Non Coronary]:{rsp_check_record_all['data']['is_non_coronary']}\n[URL]:{rsp_check_record_all['data']['user_email']}"}

        if intent== 'UpdateRecord':
            fields = {'0': 'DLP', '1': 'record_date', '2': 'facility', '3': 'co_reporting_doctor',
                      '4': 'patient_details',
                      '5': 'case_type', '6': 'is_correlated', '7': 'is_gta', '8': 'is_non_coronary',
                      '9': 'is_native_coronary', '10': 'is_cardiac', '11': 'is_non_cardiac'}


            rsp_check_active_logbook = check_active_logbook(username)
            record_name = req['queryResult']['outputContexts'][0]['parameters']['record_name']
            log_name = req['queryResult']['outputContexts'][0]['parameters']['log_name']
            field = req['queryResult']['outputContexts'][0]['parameters']['field']

            if field not in fields.keys():
                return {'fulfillmentText': f"No such field called {field}"}
            if rsp_check_active_logbook['status'] == 'no active logbook':
                return {'fulfillmentText': f'Sorry you currently don\'t have any active logbook, so you can not view anything.'}
            if rsp_check_active_logbook['status'] == 'have active logbook':
                rsp_check_record_all=check_record_all(username,log_name,record_name)
                if rsp_check_record_all['status'] == 'record not found':
                    return {'fulfillmentText': 'Record Not Found'}
                if rsp_check_record_all['status'] == 'success' and rsp_check_record_all['data']['record_status'] in ['rejected','confirmed']:
                    return {'fulfillmentText': f"This record is already {rsp_check_record_all['data']['record_status']}, you cannot change it's value now"}
                else:
                    return {'fulfillmentText':f"[Log_name]:{rsp_check_record_all['data']['log_name']}\n[Record Name]:{rsp_check_record_all['data']['record_name']}\n[DLP]:{rsp_check_record_all['data']['DLP']}\n[Case Type]:{rsp_check_record_all['data']['case_type']}\n[Co-reporting Doctor]:{rsp_check_record_all['data']['co_reporting_doctor']}\n[Facility]:{rsp_check_record_all['data']['facility']}\n[Patient Detail]:{rsp_check_record_all['data']['patient_details']}\n[Is Cardiac]:{rsp_check_record_all['data']['is_cardiac']}\n[Is Correlated]:{rsp_check_record_all['data']['is_correlated']}\n[Is GTA]:{rsp_check_record_all['data']['is_gta']}\n[Is Native Coronary]:{rsp_check_record_all['data']['is_native_coronary']}\n[is_non_cardiac]:{rsp_check_record_all['data']['is_non_cardiac']}\n[Is Non Coronary]:{rsp_check_record_all['data']['is_non_coronary']}\n[URL]:{rsp_check_record_all['data']['user_email']}\n,are you sure you want to update?"}
        if intent== 'UpdateRecord - yes':
            fields = {'0': 'DLP', '1': 'record_date', '2': 'facility', '3': 'co_reporting_doctor',
                      '4': 'patient_details',
                      '5': 'case_type', '6': 'is_correlated', '7': 'is_gta', '8': 'is_non_coronary',
                      '9': 'is_native_coronary', '10': 'is_cardiac', '11': 'is_non_cardiac'}


            record_name = req['queryResult']['outputContexts'][0]['parameters']['record_name']
            log_name = req['queryResult']['outputContexts'][0]['parameters']['log_name']
            field = fields[req['queryResult']['outputContexts'][0]['parameters']['field']]
            value = req['queryResult']['outputContexts'][0]['parameters']['value']
            rsp_change_record_paramater=change_record_paramater(username,log_name,record_name,field,value)
            print(rsp_change_record_paramater)
            if rsp_change_record_paramater['status']==0:
                return {'fulfillmentText': f"{field} has been updated as {value}"}
            if rsp_change_record_paramater['status']==2:
                return {'fulfillmentText': f"No such field called {field}"}
        if intent == 'UpdateRecord - no':
            return {'fulfillmentText': f"I didn't change value for you"}

        if intent== 'viewRecord':
            record_name = req['queryResult']['parameters']['record_name']
            log_name = req['queryResult']['parameters']['log_name']
            print(record_name)
            print(log_name)
            rsp_check_record_all = check_record_all(username, log_name, record_name)
            if rsp_check_record_all['status'] == 'record not found':
                return {'fulfillmentText': 'Record Not Found'}
            else:
                print(rsp_check_record_all['data'])
                return {'fulfillmentText': f"[Log_name]:{rsp_check_record_all['data']['log_name']}\n[Record Name]:{rsp_check_record_all['data']['record_name']}\n[DLP]:{rsp_check_record_all['data']['DLP']}\n[Case Type]:{rsp_check_record_all['data']['case_type']}\n[Co-reporting Doctor]:{rsp_check_record_all['data']['co_reporting_doctor']}\n[Facility]:{rsp_check_record_all['data']['facility']}\n[Patient Detail]:{rsp_check_record_all['data']['patient_details']}\n[Is Cardiac]:{rsp_check_record_all['data']['is_cardiac']}\n[Is Correlated]:{rsp_check_record_all['data']['is_correlated']}\n[Is GTA]:{rsp_check_record_all['data']['is_gta']}\n[Is Native Coronary]:{rsp_check_record_all['data']['is_native_coronary']}\n[is_non_cardiac]:{rsp_check_record_all['data']['is_non_cardiac']}\n[Is Non Coronary]:{rsp_check_record_all['data']['is_non_coronary']}\n[URL]:{rsp_check_record_all['data']['user_email']}"}




    # fetch action from json
    action = req.get('queryResult').get('action')

    # return a fulfillment response
    return {'fulfillmentText': 'This is a response from webhook.'}

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
   app.run()
