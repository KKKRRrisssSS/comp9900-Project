# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import datetime


class RecordRecordid(Resource):

    def get(self, RecordID):
        if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
            cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred)

        db = firestore.client()
        records_ref=db.collection(u'records')
        query = records_ref.document(RecordID)
        data = query.get().to_dict()
        if data == None:
            respond = {'status': 1}
            return respond, 200, None
        body=dict()
        for item in data.items():
            body[item[0]]=item[1]
        #if body['record_status'] in ['Level A Certification','Level B Certification']:
            #body.pop('is_native_coronary')
            #body.pop('is_graft_thoracic_aorta')
        #else:
            #body.pop('is_non_cardiac')
            #body.pop('is_non_coronary_cardiac')
        cred = credentials.Certificate("serviceAccountKey.json")
        app = firebase_admin.initialize_app(cred, {
            'storageBucket': 'cs9900-3f87f.appspot.com',
        }, name='storage')

        bucket = storage.bucket(app=app)
        blob = bucket.blob(f"{body['user_email']}/{body['log_uid']}/{body['record_index']}")
        body['user_email']=blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')

        firebase_admin.delete_app(app)

        response={'status':0,'body':body}

        return response, 200, None

    def post(self, RecordID):
        if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
            cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred)
        print(g.args)
        field=g.args['field']
        value=g.args['value']
        print(field)
        if value in ['True','true',True]:
            value=True
        if value in ['False','false',False]:
            value=False
        #if field not in ['DLP','case_day','case_month','case_type','case_year','co_reporting_doctor','facility_name','is_correlated','is_graft_thoracic_aorta','is_native_coronary','is_non_cardiac','is_non_coronary_cardiac','patient_details']:
        #    return {'status':2}
        db = firestore.client()
        records_ref=db.collection(u'records')
        query = records_ref.document(RecordID)
        data = query.get().to_dict()
        if data == None:
            respond = {'status': 1}
            return respond, 200, None
        records_ref.document(RecordID).update({field: value})

        records_query = records_ref.document(RecordID)
        records_data = records_query.get().to_dict()
        flag_complete=1
        fields = {'0': 'DLP', '1': 'record_date', '2': 'facility', '3': 'co_reporting_doctor',
                  '4': 'patient_details',
                  '5': 'case_type', '6': 'is_correlated', '7': 'is_gta', '8': 'is_non_coronary',
                  '9': 'is_native_coronary', '10': 'is_cardiac', '11': 'is_non_cardiac'}
        for field in fields.values():
            if data[field]==None:
                flag_complete=0
                break
        if flag_complete==1:
            records_ref.document(RecordID).update({'record_status': 'Completed'})
        return {'status':0}
