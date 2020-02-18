import json
import os, config
import string
import random
import csv

from .Pools import UserPool
from app import db, db1
from firebase_admin import *
from datetime import date, datetime
from .language_processing import *
from flask_login import current_user
from collections import defaultdict
from flask import jsonify
import time



class System:
    def __init__(self):
        self._user_pool = UserPool()
        self.c_user = ' '

    def set_current_user(self, user_id):
        self.c_user = user_id
        return 

    def get_current_user(self):
        return self.c_user

    def get_current_flask_user(self):
        return current_user.id

    def add_user(self, user_data):
        self._user_pool.add_user(user_data)
        pass

    def get_user(self, user_id):
        return self._user_pool.get(user_id)

    def get_all_users(self, roles=[]):
        if roles:
            return self._user_pool.get_users_by_roles(roles)
        return self._user_pool.get_all()

    def id_generator(self):
        size=10
        chars=string.ascii_uppercase + string.digits
        string_random = ''.join(random.choice(chars) for _ in range(size))
        print(string_random)
        return string_random

    def create_admin_documents(self, user_id):
        users_ref = db1.collection(u'users').document(user_id)
        users_ref.set({
            u'user_email': user_id,
            u'messenger_uid':None, 
            u'verify_token':self.id_generator(),
            u'first_name': "",
            u'last_name': "",
            u'is_supervisor': True,
            u'specialist_level': "",
            u'address_city': "",
            u'address_country': "",
            u'address': "",
            u'address_state': "",
            u'address_postcode': "",
            u'current_certification': "",
            u'current_cert_expiry_date': "",
            u'program_uid': "",
            u'supervisor_approved':True
        })
        self.create_default_logbook(user_id)
    
    def create_user_documents(self, user_data):
        user_id=user_data['email_id']
        self.set_current_user(user_id)
        users_ref = db1.collection(u'users').document(user_id)
        username = self.get_current_user()
        users_ref.set({
            u'user_email': username,
            u'messenger_uid':None,
            u'verify_token':self.id_generator(),
            u'first_name': "",
            u'last_name': "",
            u'is_supervisor':False,
            u'specialist_level': "",
            u'address_city': "",
            u'address_country': "",
            u'address': "",
            u'address_state': "",
            u'address_postcode': "",
            u'current_certification': "",
            u'current_cert_expiry_date': "",
            u'program_uid': "",
            u'supervisor_approved':False
        })
        self.create_default_logbook(username)

    def check_password(self, user_id, password):
        self.set_current_user(user_id)
        return self._user_pool.check_password(user_id, password)


# ----------------------------------------------------------------------------------------------------
# User functions
# ----------------------------------------------------------------------------------------------------
    def check_user_details(self, user_data):
        keys = [] 
        keys = user_data.keys()

        if 'first_name' not in keys :
            user_data['first_name'] = None
        if 'last_name' not in keys :
            user_data['last_name'] = None
        if 'address' not in keys :
            user_data['address'] = None
        if 'address_city' not in keys :
            user_data['address_city'] = None
        if 'address_state' not in keys :
            user_data['address_state'] = None
        if 'address_postcode' not in keys :
            user_data['address_postcode'] = None
        if 'current_cert_expiry_date' not in keys :
            user_data[current_cert_expiry_date] = None
        if 'current_cert' not in keys :
            user_data[current_cert] = None

        return user_data
        

    def update_user_profile(self, user_data):
        print('_user_profile_function entered')
        print(self.get_current_flask_user())

        # user_data = self.check_user_details(user_details)
        print(user_data)
        print(user_data['first_name'])
        first_name = user_data['first_name']
        last_name =  user_data['last_name']
        address_city = user_data['address_city']
        address_country = user_data['address_country']
        address_state = user_data['address_state']
        address = user_data['address']
        address_postcode = user_data['address_postcode']
        current_cert_expiry_date = user_data['current_cert_expiry_date']
        current_cert = user_data['current_cert']

        if first_name == "" or last_name == "" or current_cert_expiry_date=="" or current_cert == "empty":
            return
        if address_city == "" or address == ""or address_country == "" or address_state == "" or address_postcode == "":
            return

        if current_cert == 'Level B':
            is_supervisor = True
            specialist_level = 'level_b'
        elif current_cert == 'Level A':
            specialist_level = 'level_a'
            is_supervisor = False
        else :
            specialist_level = 'Student'
            is_supervisor = False

        # print(first_name[0] + ',' + last_name [0])
        # print(address[0] + ',' + address_city[0]+','+address_country[0] +','+address_postcode[0])
        users_ref = db1.collection(u'users').document(self.get_current_flask_user())
        users_ref.update({
            u'first_name': first_name,
            u'last_name': last_name,
            u'is_supervisor': is_supervisor,
            u'specialist_level': specialist_level,
            u'address_city': address_city,
            u'address_country': address_country,
            u'address_state':address_state,
            u'address': address,
            u'address_postcode': address_postcode,
            u'current_certification': current_cert,
            u'current_cert_expiry_date': current_cert_expiry_date,
            u'program_uid': None
        })


    def get_user_details(self):
        curr_user = self.get_current_flask_user()
        print(curr_user)
        doc_ref = db1.collection(u'users').document(curr_user)
        doc = doc_ref.get()
        print('USER DETAILS !!!!!!!!!!!!!')
        print(u'Document data: {}'.format(doc.to_dict()))
        return doc.to_dict()

    def get_verify_token(self):
        curr_user = self.get_current_flask_user()
        doc_ref = db1.collection(u'users').document(curr_user)
        doc = doc_ref.get()
        tmp = doc.to_dict()
        print(tmp)
        return tmp['verify_token']


# ----------------------------------------------------------------------------------------------------
# Logbook functions
# ----------------------------------------------------------------------------------------------------
    def test_logbook_new(self):
        self.add_logbook()

    def close_other_logbooks(self):
        curr_user = self.get_current_flask_user()
        query_ref = db1.collection(u'logbooks').where('user_email', '==', curr_user)
        docs = query_ref.get()
        for doc in docs:
            doc_tmp = {}
            doc_tmp = doc.to_dict()
            log_status = doc_tmp['logStatus']
            if log_status == 'activated' :
                doc_ref = db1.collection(u'logbooks').document(doc_tmp['log_uid'])
                doc_ref.update({
                    'logStatus' : "expired"
                })

    def check_unique_logbook(self, check_name):
        curr_user = self.get_current_flask_user()
        query_ref = db1.collection(u'logbooks').where('user_email', '==', curr_user)
        docs = query_ref.get()
        for doc in docs:
            doc_tmp = {}
            doc_tmp = doc.to_dict()
            log_name = doc_tmp['log_name']
            if log_name == check_name :
                print ('check_unique_logbook failed: -------------' + check_name)
                return True
        print ('check_unique_logbook passed-----------' + check_name)
        return False

    def create_default_logbook(self, username):
        log_name = "Default"
        upload_datetime = datetime.now()
        logbooks_ref = db1.collection(u'logbooks').document()
        logbooks_ref.set({
            'user_email': username,
            'total_case_count':0,
            'program_uid': None,
            'non_coronary_count':0 ,
            'non_cardiac_count': 0,
            'cardiac_count': 0,
            'gta_count': 0,
            'native_coronary_count': 0,
            'logStatus' : "activated", 
            'live_case_course_count' : 0, 
            'live_case_count' :0, 
            'library_case_count':0,
            'log_uid' : logbooks_ref.id, 
            'created_time' : upload_datetime,
            'log_name' : log_name,
            'correlated_case_count' :0
        })


    def create_logbook(self, log_data):
        log_name = log_data['log_name']
        program_tmp = log_data['current_cert']
        if log_name == "" or program_tmp == "empty":
            return
        if self.check_unique_logbook(log_name) == True:
            return
        self.close_other_logbooks()
        logbooks_ref = db1.collection(u'logbooks').document()
        upload_datetime = datetime.now()
        
        program_uid = "no_program"
        if program_tmp == "Level A Certification":
            program_uid = "level_a_certification"
        elif program_tmp == "Level B Certification":
            program_uid = "level_b_certification"
        elif program_tmp == "Level A Recertification":
            program_uid = "level_a_recertification"
        elif program_tmp == "Level B Recertification":
            program_uid = "level_b_recertification"
        elif program_tmp == "Conversion from A to B":
            program_uid = "level_a_to_b_conversion"
        
        logbooks_ref.set({
            'user_email': self.get_current_flask_user(),
            'total_case_count':0,
            'program_uid': program_uid,
            'non_coronary_count':0 ,
            'non_cardiac_count': 0,
            'cardiac_count': 0,
            'gta_count': 0,
            'native_coronary_count': 0,
            'logStatus' : "activated", 
            'live_case_course_count' : 0, 
            'live_case_count' :0, 
            'library_case_count':0,
            'log_uid' : logbooks_ref.id, 
            'created_time' : upload_datetime,
            'log_name' : log_name,
            'correlated_case_count' :0
        })

# ----------------------------------------------------------------------------------------------------
# Querying Logbooks
# ----------------------------------------------------------------------------------------------------
    def get_logbook_case_count(self, log_uid):
        if log_uid == "" or log_uid ==  None:
            log_uid =  self.get_current_active_logbook_id()
        records= self.get_records_by_logbook_without_deleted(log_uid)
        return len(records)
    
    def get_logbook_incomplete_count(self, log_uid):
        query_ref = db1.collection(u'records').where('log_uid', '==', log_uid).where('record_status', '==', 'incomplete')
        docs = query_ref.get()
        count = 0
        for doc in docs:
            count =  count +1 
        return count

    
    def get_current_user_logbooks(self):
        curr_user = self.get_current_flask_user()
        query_ref = db1.collection(u'logbooks').where('user_email', '==', curr_user)
        docs = query_ref.get()
        log_list = []
        for doc in docs:
            tmp = {}
            # print(u'current user logbooks : {}'.format(doc.to_dict()))
            tmp = doc.to_dict()
            log_name = tmp['log_name']
            log_status = tmp['logStatus']
            log_string = log_name + "+" + log_status
            log_list.append(log_string)
        return log_list

    def get_current_active_logbook_record_size(self):
        log_id = self.get_current_active_logbook_id()
        records=[]
        if log_id!=None :
            print(log_id)
            records = self.get_records_by_logbook(log_id)
            print('________________________' + str(len(records)+1))
            return len(records)+ 1
        return 0

    def get_current_active_logbook(self):
        curr_user = self.get_current_flask_user()
        query_ref = db1.collection(u'logbooks').where('user_email', '==', curr_user).where('logStatus', '==', 'activated')
        docs = query_ref.get()
        for doc in docs:
            return doc.to_dict()
        return None

    def get_current_active_logbook_id(self):
        curr_user = self.get_current_flask_user()
        query_ref = db1.collection(u'logbooks').where('user_email', '==', curr_user).where('logStatus', '==', 'activated')
        docs = query_ref.get()
        for doc in docs:
            log=doc.to_dict()
            if(log['logStatus'] == "activated"):
                return log['log_uid']
        return None

    def get_current_active_logbook_name(self):
        curr_user = self.get_current_flask_user()
        query_ref = db1.collection(u'logbooks').where('user_email', '==', curr_user).where('logStatus', '==', 'activated')
        docs = query_ref.get()
        for doc in docs:
            log=doc.to_dict()
            if(log['logStatus'] == "activated"):
                return log['log_name']
        return None

    def get_logid_by_logname(self, log_name):
        curr_user = self.get_current_flask_user()
        query_ref = db1.collection(u'logbooks').where('user_email', '==', curr_user)
        docs = query_ref.get()
        log_details = []
        for doc in docs:
            tmp = {}
            # print(u'current user logbooks : {}'.format(doc.to_dict()))
            tmp = doc.to_dict()
            tmp_name = tmp['log_name']
            if(log_name == tmp_name): 
                return tmp['log_uid']
        return None


    def get_current_user_logbook_by_logname(self, log_name):
        if log_name == "":
            log = self.get_current_active_logbook()
            log_name =  log['log_name']
        curr_user = self.get_current_flask_user()
        query_ref = db1.collection(u'logbooks').where('user_email', '==', curr_user).where('log_name', '==', log_name)
        docs = query_ref.get()
        log_details = []
        for doc in docs:
            tmp = {}
            # print(u'current user logbooks : {}'.format(doc.to_dict()))
            tmp = doc.to_dict()
            tmp_name = tmp['log_name']
            if(log_name == tmp_name): 
                log_details.append("log_name+" + log_name)
                log_details.append("log_uid+" + tmp['log_uid'])
                log_details.append("total_case_count+" + str(tmp['total_case_count']))
                log_details.append("native_coronary_count+" + str(tmp['native_coronary_count']))
                log_details.append("non_coronary_count+" + str(tmp['non_coronary_count']))
                log_details.append("non_cardiac_count+" + str(tmp['non_cardiac_count']))
                log_details.append("cardiac_count+" + str(tmp['cardiac_count']))
                log_details.append("gta_count+" + str(tmp['gta_count']))
                log_details.append("log_status+" + tmp['logStatus'])
                log_details.append("live_case_course_count+" + str(tmp['live_case_course_count']))
                log_details.append("live_case_count+" + str(tmp['live_case_count']))
                log_details.append("library_case_count" + str(tmp['library_case_count']))
                log_details.append("created_time+" + str(tmp['created_time']))
                log_details.append("correlated_case_count+" + str(tmp['correlated_case_count']))
                return log_details
        return None

# ----------------------------------------------------------------------------------------------------
# Updating Logbooks
# ----------------------------------------------------------------------------------------------------

    
    def update_logbook_counts(self, record_data):
        correlated_case = 0
        case_type = record_data['case_type']
        live_case = 0
        library_case = 0
        live_course_case = 0
        non_coronary = 0
        native_coronary = 0
        cardiac = 0
        non_cardiac = 0
        gta = 0


        print('case_type')
        if case_type == 'Live':
            live_case = True
        elif case_type == 'Library':
            library_case = True
        else:
            live_course_case = True
        
        print('case_count')
        if(record_data['is_case_correlated']== "Yes"):
            correlated_case = 1
        if(record_data['is_case_coronary']== "Yes"):
            non_coronary = 1
        # if(record_data['is_native_coronary']== "Yes"):
        #     native_coronary = 1
        if(record_data['is_case_gta']== "Yes"):
            gta = 1
        if(record_data['is_case_cardiac']== "Yes"):
            cardiac = 1
        else :
            non_cardiac = 1

        print('update')

        log_ref = db1.collection('logbooks').document(self.get_current_active_logbook_id())
        log = log_ref.get()
        log_dict = log.to_dict()
        current_correlated = log_dict['correlated_case_count']
        current_live = log_dict['live_case_count']
        current_library = log_dict['library_case_count']
        current_course = log_dict['live_case_course_count']
        current_native_coronary= log_dict['native_coronary_count']
        current_non_cardiac = log_dict['non_cardiac_count']
        current_non_coronary= log_dict['non_coronary_count']
        current_cardiac = log_dict['cardiac_count']
        current_gta = log_dict['gta_count']
        current_total = log_dict['total_case_count']

        print('log_ref.update')

        log_ref.update({
            u'correlated_case_count': current_correlated + correlated_case,
            u'live_case_count': current_live + live_case,
            u'library_case_count': current_library + library_case,
            u'live_case_course_count': current_course + live_course_case,
            u'native_coronary_count': current_native_coronary + native_coronary,
            u'non_cardiac_count': current_non_cardiac + non_cardiac,
            u'non_coronary_count': current_non_coronary + non_coronary,
            u'cardiac_count' : current_cardiac + cardiac,
            u'gta_count' : current_gta + gta,
            u'total_case_count': current_total + 1
        })
# ----------------------------------------------------------------------------------------------------
# Record functions
# ----------------------------------------------------------------------------------------------------
    def add_record(self, record_data, record_name):
        
        records_ref = db1.collection(u'records').document()
        DLP_list = record_data.get("DLP")
        Date_list = record_data.get("Date")
        Facility_list = record_data.get("Facility")
        Doctor_list = record_data.get("Co-reporting Doctor")
        UID_list = record_data.get("Unique Episode Number")
        non_coronary = record_data.get("Non_coronary_cardiac_findings")
        non_cardiac = record_data.get("Non_cardiac_findings")
        is_coronary = "Yes"
        is_cardiac = "Yes"
        is_non_coronary = "No"
        is_non_cardiac = "No"

        print(str(non_coronary[0])+ "AND" + str(non_cardiac[0]))


        if(non_coronary[0] == 1 or non_coronary[0] == "1"):
            print("enteref if non coronary")
            is_coronary = "No"
            is_non_coronary = "Yes"
        if(non_cardiac[0] == 1 or non_cardiac[0] == "1"):
            print("enteref if non cardiac")
            is_cardiac = "No"
            is_non_cardiac = "Yes"

        print("exit if")

        upload_datetime = datetime.now()
        log_uid = self.get_current_active_logbook_id()
        #print(upload_datetime)

        Doctor_string = ""
        for doctor in Doctor_list:
            Doctor_string = Doctor_string + doctor + " ,"

        record_name_list = record_name.split("/")
        record_index = record_name_list[1]
        log_name = self.get_current_active_logbook_name()


        records_ref.set({
            'user_email': self.get_current_flask_user(),
            'DLP': DLP_list[0],
            'record_date': Date_list[0],
            'facility':Facility_list[0] ,
            'co_reporting_doctor': Doctor_string,
            'patient_details': UID_list[0],
            'case_type' : None, 
            'is_correlated' : None, 
            'is_gta' :None, 
            'is_native_coronary':is_coronary, 
            'is_cardiac':is_cardiac,
            'is_non_coronary':is_non_coronary, 
            'is_non_cardiac':is_non_cardiac,
            'log_uid' : log_uid, 
            'log_name':log_name,
            'record_name':record_name,
            'record_status' : "incomplete", 
            'supervisor_uid': None, 
            'upload_time' : upload_datetime,
            'record_uid': records_ref.id,
            'record_index':record_index,
            'is_approved':False,
            'supervisor_that_approved' :None

        })
        
        doc = records_ref.get()
        return doc.to_dict()


    def update_record(self, record_data, record_name):

        records_ref = db1.collection(u'records').document(self.get_record_id_by_name(record_name))
        doc = self.get_record_dict_by_name(record_name)
        if doc['log_uid'] != self.get_current_active_logbook_id():
            return "Not Active Logbook"

        record_details = {}

        DLP = record_data["dlp"]
        Date = record_data["date"]
        Facility = record_data["facility"]
        Doctors = record_data["doctor"]
        UID = record_data["uid"]

        current_correlated = record_data['is_case_correlated']
        case_type = record_data['case_type']
        current_native_coronary= record_data['is_case_coronary']
        current_cardiac = record_data['is_case_cardiac']
        current_gta = record_data['is_case_gta']
        current_supervisor = record_data['supervisor']
        current_status = record_data['record_status']
        current_live = ""
        current_library = ""
        current_course = ""
        
        if DLP == "":
            DLP = doc["DLP"]
        if Date == "":
            Date = doc["record_date"]
        if Facility == "":
            Date = doc["facility"]
        if Doctors == "":
            Doctors = doc['co_reporting_doctor']
        if UID == "":
            UID = doc['patient_details']
        if current_correlated == "empty":
            current_correlated = doc['is_correlated']
        if case_type == "empty":
            case_type= doc['case_type']
        if current_native_coronary == "empty":
            current_native_coronary= doc['is_native_coronary']
        if current_cardiac == "empty":
            current_cardiac= doc['is_cardiac']
        if current_gta == "empty":
            current_gta= doc['is_gta'] 
        if current_supervisor == "":
            current_supervisor = doc['supervisor_uid']
        if current_supervisor == "":
            current_supervisor = doc['record_status']

        if case_type == "Live" :
            current_live = "Yes"
        elif case_type == "Library":
            current_library = "Yes"
        elif case_type == "Course":
            current_course = "Yes"

        current_non_cardiac = "Yes"
        current_non_coronary= "Yes"

        if current_cardiac == "Yes":
            current_non_cardiac = "No"
        if current_native_coronary == "Yes":
            current_non_cardiac = "No"

        record_details["case_type"] = case_type
        record_details['is_case_correlated'] = current_correlated
        record_details["is_case_coronary"] = current_native_coronary
        record_details["is_case_cardiac"] = current_cardiac
        record_details["is_case_gta"] = current_gta


        records_ref.update({
            'DLP': DLP,
            'record_date': Date,
            'facility':Facility ,
            'co_reporting_doctor': Doctors,
            'patient_details': UID,
            'case_type' :case_type, 
            'is_correlated' : current_correlated, 
            'is_gta' :current_gta,
            'is_native_coronary':current_native_coronary, 
            'is_cardiac':current_cardiac,
            'is_non_coronary':current_non_coronary, 
            'is_non_cardiac':current_non_cardiac, 
            'record_name':record_name,
            'record_status' : current_status, 
            'supervisor_uid': current_supervisor, 
        })

        self.update_logbook_counts(record_details)
        doc = records_ref.get()
        return doc.to_dict()



# ----------------------------------------------------------------------------------------------------
# Querying Records
# ----------------------------------------------------------------------------------------------------
    def get_records_by_logbook(self, log_id):
        query_ref = db1.collection(u'records').where('log_uid', '==', log_id)
        docs = query_ref.get()
        dicts_list = []
        for doc in docs:
            print(u'Get Records By Logbook data: {}'.format(doc.to_dict()))
            tmp = {}
            tmp = doc.to_dict()
            record_name = tmp['record_name']
            record_date = tmp['upload_time']
            dicts_list.append(record_name + '+' + str(record_date))
        return dicts_list

    def get_records_by_logbook_without_deleted(self, log_id):
        query_ref = db1.collection(u'records').where('log_uid', '==', log_id)
        docs = query_ref.get()
        dicts_list = []
        for doc in docs:
            print(u'Get Records By Logbook data: {}'.format(doc.to_dict()))
            tmp = {}
            tmp = doc.to_dict()
            if(tmp['record_status'] != 'deleted'):
                record_name = tmp['record_name']
                record_date = tmp['upload_time']
                dicts_list.append(record_name + '+' + str(record_date))
        return dicts_list

    def get_current_user_records_all(self):
        curr_user = self.get_current_flask_user()
        query_ref = db1.collection(u'records').where('user_email', '==', curr_user)
        docs = query_ref.get()
        dicts_list = []
        for doc in docs:
            print(u'Document data: {}'.format(doc.to_dict()))
            dicts_list.append(doc.to_dict)
        return dicts_list

    def get_current_incomplete_records(self):
        curr_user = self.get_current_flask_user()
        active_logbook = self.get_current_active_logbook_id()
        # print(active_logbook)
        query_ref = db1.collection(u'records').where('user_email', '==', curr_user).where('log_uid', '==', active_logbook).where('record_status', '==', "incomplete")
        docs = query_ref.get()
        dicts_list = []
        for doc in docs:
            tmp = doc.to_dict()
            # print(u'Document data: {}'.format(doc.to_dict()))
            dicts_list.append(str(tmp['record_name']) + '+' + str(tmp['upload_time']))
        return dicts_list

    def get_record(self, record_id):
        doc_ref = db1.collection(u'records').document(record_id)
        doc = doc_ref.get()
        print(u'Document data: {}'.format(doc.to_dict()))
        return doc.to_dict()

    def get_record_by_name(self, record_name):
        doc_ref = db1.collection(u'records').where('record_name','==',record_name)
        docs = doc_ref.get()
        for doc in docs:
            print(u'Document data: {}'.format(doc.to_dict()))
            record_deet = []
            tmps = doc.to_dict()
            for tmp in tmps:
                tmp_string = str(tmp) + "+" + str(tmps[tmp])
                record_deet.append(tmp_string)
            return record_deet

    def get_record_dict_by_name(self, record_name):
        doc_ref = db1.collection(u'records').where('record_name','==',record_name)
        tmps = doc_ref.get()
        # print(u'Document data: {}'.format(doc.to_dict()))
        for tmp in tmps:
            docs = tmp.to_dict()
            return docs


    def get_record_list_by_name(self, record_name):
        doc_ref = db1.collection(u'records').where('record_name','==',record_name)
        tmps = doc_ref.get()
        # print(u'Document data: {}'.format(doc.to_dict()))
        # record_deet = []
        for tmp in tmps:
            doc = tmp.to_dict()
            return doc
            # for key in sorted(docs.keys()):
            #     record_deet.append(str(key) + "+" + str(docs[key])) 
        return None

    def get_record_id_by_name(self, record_name):
        doc_ref = db1.collection(u'records').where('record_name','==',record_name)
        tmps = doc_ref.get()
        for tmp in tmps:
            doc = tmp.to_dict()
            return doc['record_uid']

    def delete_record(self, record_name):
        print(record_name)
        record_uid = self.get_record_id_by_name(record_name)
        doc_ref = db1.collection(u'records').document(record_uid)
        doc_ref.update({
            u'record_status': 'deleted'
        })


# ----------------------------------------------------------------------------------------------------
# Language Processing
# ----------------------------------------------------------------------------------------------------

    def test_language_processing(self):
        Conclustion_Dictionary = defaultdict(list)
        report = os.path.join(config.DATA_DIR, '25.pdf')
        fp = open(report, 'rb')
        tempary_sentence = language_processing.pdf_to_txt(fp) 
        language_processing.decect_DLP(tempary_sentence,Conclustion_Dictionary)
        language_processing.decect_date(tempary_sentence,Conclustion_Dictionary)
        language_processing.Decect_Unique_Number(tempary_sentence,Conclustion_Dictionary)
        language_processing.Decect_location(tempary_sentence,Conclustion_Dictionary)
        language_processing.Decect_Coreporting_Doctor(tempary_sentence,Conclustion_Dictionary)
        language_processing.Decect_cardiac_findings(tempary_sentence,Conclustion_Dictionary)
        language_processing.Decect_coronary_cardiac_findings(tempary_sentence,Conclustion_Dictionary)
        Conclustion_Dictionary['Correlated'].append("None")
        print(Conclustion_Dictionary)
        self.add_record(Conclustion_Dictionary, "log_test/record_test")

    def language_processing(self,file_sent, record_name):
        Conclustion_Dictionary = defaultdict(list)
        report = file_sent
        tempary_sentence = language_processing.pdf_to_txt(report) 
        language_processing.decect_DLP(tempary_sentence,Conclustion_Dictionary)
        language_processing.decect_date(tempary_sentence,Conclustion_Dictionary)
        language_processing.Decect_Unique_Number(tempary_sentence,Conclustion_Dictionary)
        language_processing.Decect_location(tempary_sentence,Conclustion_Dictionary)
        language_processing.Decect_Coreporting_Doctor(tempary_sentence,Conclustion_Dictionary)
        language_processing.Decect_cardiac_findings(tempary_sentence,Conclustion_Dictionary)
        language_processing.Decect_coronary_cardiac_findings(tempary_sentence,Conclustion_Dictionary)
        Conclustion_Dictionary['Correlated'].append("None")
        #print(Conclustion_Dictionary)
        record = self.add_record(Conclustion_Dictionary, record_name)
        return record

    def get_json(self, dictionary):
        return jsonify(dictionary)


        
        
    def write_to_csv(self, log_id):
        # log_id = self.get_current_active_logbook_id()
        query_ref = db1.collection(u'records').where('log_uid', '==', log_id)
        docs = query_ref.get() 
        file_dict = {}
        log_details = self.get_current_active_logbook()
        file_dict['logbook_details'] = log_details
        count = 0
        for doc in docs:
            tmps = doc.to_dict()
            tmp_dict = {}
            for key in sorted(tmps.keys()):
                tmp_dict[key] = tmps[key]
            file_dict["record " + str(count)] = tmp_dict
            count = count +1
        
        # df = pandas.DataFrame(file_dict)
        # df.to_csv("output.csv")
        w = csv.writer(open(os.path.join(config.DATA_DIR, "output.csv"), "w"))
        for key, val in file_dict.items():
            w.writerow([key, val])




    # ----------------------------------------------------------------------------------------------------
# Admin Functions
# ----------------------------------------------------------------------------------------------------
    
    def view_all_supervisors(self):
        users_ref = db1.collection(u'users')
        docs = users_ref.get()
        supervisors = []
        for doc in docs:
            tmp = doc.to_dict()
            if tmp['is_supervisor'] == True or tmp['is_supervisor'] == "True":
                username = tmp['user_email']
                approved = tmp['supervisor_approved']
                current_cert =  tmp['current_certification']
                current_cert_expiry = tmp['current_cert_expiry_date']
                supervisors.append(str(username)+ "+" + str(approved) + "+" + str(current_cert)+ "+" +str(current_cert_expiry))
        return supervisors

    def approve_supervisor(self, username):
        user_ref = db1.collection(u'users').document(username)
        user_ref.update({
            u'supervisor_approved': True
        })
        print('approve_completed')

    def disapprove_supervisor(self, username):
        user_ref = db1.collection(u'users').document(username)
        user_ref.update({
            u'supervisor_approved': False
        })
        print('disapprove_completed')

    def check_if_supervisor(self, username):
        user_ref = db1.collection('users').document(username)
        doc=user_ref.get()
        tmp = doc.to_dict()
        print(tmp['supervisor_approved'] )
        if tmp['supervisor_approved'] == True :
            return True
        else :
            return False
        return False


# ----------------------------------------------------------------------------------------------------
# Supervisor Functions
# ----------------------------------------------------------------------------------------------------
    def get_completed_levelA_records(self):
        records_ref = db1.collection('records').where('is_approved', '==', False)
        records = records_ref.get()
        record_list = []

        for record in records:
            tmp = record.to_dict()
            if tmp['user_email'] != self.get_current_flask_user():
                if tmp['record_status']=='Completed' or tmp['record_status']=='complete' :
                    record_list.append(str(tmp['user_email']) + "+" + str(tmp['record_name']) + '+' + str(tmp['upload_time']))
        
        return record_list

    def approve_report (self, record_name):
        supervisor_uid = self.get_current_flask_user()
        record_id = self.get_record_id_by_name(record_name)
        record_ref = db1.collection('records').document(record_id)
        record_ref.update({
            u'supervisor_that_approved' :supervisor_uid,
            u'is_approved' : True
        })





        


    ########################################################################
