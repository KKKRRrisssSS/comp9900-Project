import json
import os, config

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

    def create_admin_documents(self, user_id):
        users_ref = db1.collection(u'users').document(user_id)
        users_ref.set({
            u'user_email': user_id
        })
    
    def create_user_documents(self, user_data):
        user_id=user_data['email_id']
        self.set_current_user(user_id)
        users_ref = db1.collection(u'users').document(user_id)
        users_ref.set({
            u'user_email': self.get_current_user()
        })

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
        print('add_user_profile_function entered')
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
        users_ref.set({
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


    def add_user_profile(self, user_data):
        print('add_user_profile_function entered')
        print(self.get_current_flask_user())
        print(user_data)
        first_name = user_data['first_name'],
        last_name =  user_data['last_name'],
        address_city = user_data['address_city'],
        address_country = user_data['address_country'],
        address = user_data['address'],
        address_postcode = user_data['address_postcode'],

        print(first_name[0] + ',' + last_name [0])
        print(address[0] + ',' + address_city[0]+','+address_country[0] +','+address_postcode[0])
        users_ref = db1.collection(u'users').document(self.get_current_flask_user())
        users_ref.set({
            u'first_name': first_name[0],
            u'last_name': last_name[0],
            u'is_supervisor': None,
            u'specialist_level': None,
            u'address_city': address_city[0],
            u'address_country': address_country[0],
            u'address': address[0],
            u'address_postcode': address_postcode[0],
            u'current_certification': None,
            u'current_cert_expiry_day': None,
            u'current_cert_expiry_month': None,
            u'current_cert_expiry_year': None,
            u'program_uid': None
        })

    def test_language_processing(self):
        Conclustion_Dictionary = defaultdict(list)
        report = os.path.join(config.DATA_DIR, '25.pdf')
        tempary_sentence = language_processing.pdf_to_txt(report) 
        language_processing.decect_DLP(tempary_sentence,Conclustion_Dictionary)
        language_processing.decect_date(tempary_sentence,Conclustion_Dictionary)
        language_processing.Decect_Unique_Number(tempary_sentence,Conclustion_Dictionary)
        language_processing.Decect_location(tempary_sentence,Conclustion_Dictionary)
        language_processing.Decect_Coreporting_Doctor(tempary_sentence,Conclustion_Dictionary)
        Conclustion_Dictionary['Correlated'].append("None")
        print(Conclustion_Dictionary)
        self.add_record(Conclustion_Dictionary)

    def language_processing(self,file_sent):
        Conclustion_Dictionary = defaultdict(list)
        report = file_sent
        tempary_sentence = language_processing.pdf_to_txt(report) 
        language_processing.decect_DLP(tempary_sentence,Conclustion_Dictionary)
        language_processing.decect_date(tempary_sentence,Conclustion_Dictionary)
        language_processing.Decect_Unique_Number(tempary_sentence,Conclustion_Dictionary)
        language_processing.Decect_location(tempary_sentence,Conclustion_Dictionary)
        language_processing.Decect_Coreporting_Doctor(tempary_sentence,Conclustion_Dictionary)
        Conclustion_Dictionary['Correlated'].append("None")
        #print(Conclustion_Dictionary)
        record = self.add_record(Conclustion_Dictionary)
        return record
    
    def test_logbook_new(self):
        self.add_logbook()

    def add_record(self, record_data):
        records_ref = db1.collection(u'records').document()
        DLP_list = record_data.get("DLP")
        Date_list = record_data.get("Date")
        Facility_list = record_data.get("Facility")
        Doctor_list = record_data.get("Co-reporting Doctor")
        UID_list = record_data.get("Unique Episode Number")
        upload_datetime = datetime.now()
        log_uid = self.get_current_active_logbook_id()
        #print(upload_datetime)

        Doctor_string = ""
        for doctor in Doctor_list:
            Doctor_string = Doctor_string + doctor + " ,"

        records_ref.set({
            'user_email': self.get_current_flask_user(),
            'DLP': DLP_list[0],
            'record_date': Date_list[0],
            'facility':Facility_list[0] ,
            'co_reporting_doctor': Doctor_string,
            'patient_details': UID_list[0],
            'case_type' : None, 
            'is_correlated' : None, 
            'is_graft_thoracic_aorta' :None, 
            'log_uid' : log_uid, 
            'program_uid' : None,
            'record_status' : None, 
            'supervisor_uid': None, 
            'upload_time' : upload_datetime,
            'current_certification' :None,
            'record_uid': records_ref.id
        })
        doc = records_ref.get()
        return doc.to_dict()

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


    def get_json(self, dictionary):
        return jsonify(dictionary)


    def get_user_details(self):
        curr_user = self.get_current_flask_user()
        doc_ref = db1.collection(u'users').document(curr_user)
        doc = doc_ref.get()
        print(u'Document data: {}'.format(doc.to_dict()))
        return doc.to_dict()

    def get_records_by_logbook(self, log_id):
        query_ref = db1.collection(u'records').where('log_uid', '==', log_id)
        docs = query_ref.get()
        dicts_list = []
        for doc in docs:
            print(u'Document data: {}'.format(doc.to_dict()))
            dicts_list.append(doc.to_dict)
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
        doc = query_ref.get()
        return doc.to_dict()

    def get_current_active_logbook_id(self):
        curr_user = self.get_current_flask_user()
        query_ref = db1.collection(u'logbooks').where('user_email', '==', curr_user).where('logStatus', '==', 'activated')
        docs = query_ref.get()
        for doc in docs:
            log=doc.to_dict()
            if(log['logStatus'] == "activated"):
                return log['log_uid']
        return None

    def get_current_user_incomplete_records(self):
        curr_user = self.get_current_flask_user()
        active_logbook = self.get_current_active_logbook_id()
        query_ref = db1.collection(u'records').where('user_email', '==', curr_user).where('log_uid', '==', active_logbook).where('is_correlated', '==', None)
        docs = query_ref.get()
        dicts_list = []
        for doc in docs:
            print(u'Document data: {}'.format(doc.to_dict()))
            dicts_list.append(doc.to_dict)
        return dicts_list

    def get_record(self, record_id):
        doc_ref = db1.collection(u'records').document(record_id)
        doc = doc_ref.get()
        print(u'Document data: {}'.format(doc.to_dict()))
        return doc.to_dict()
        
    def check_password(self, user_id, password):
        self.set_current_user(user_id)
        return self._user_pool.check_password(user_id, password)

    ########################################################################
