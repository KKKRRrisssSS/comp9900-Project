# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

class Record(Resource):

    def get(self):
        if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
            cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        records_ref = db.collection(u'records')

        print(g.args)
        if 'SupervisorID' in g.args.keys():
            query = records_ref.where(u'supervisor_uid', u'==', g.args['SupervisorID']).where(u'record_status', u'==', g.args['record_status']).stream()
            docs = []
            print('AAAAAAA')
            for doc in query:
                docs.append((doc.id, doc.to_dict()))
            if docs == []:
                respond = {'status': 1}
                return respond, 404, None
            print(docs)
            body=[]
            for doc in docs:
                body.append({'RecordID':doc[1],'record_name':doc[1]['record_name'],'log_name':doc[1]['log_name'],'user_email':doc[1]['user_email']})
            respond=body
            print(respond)
            return respond,200,None
        if 'userID' in g.args.keys():
            query = records_ref.where(u'user_email', u'==', g.args['userID']).where(u'record_status', u'==', g.args['record_status']).stream()
            docs = []
            for doc in query:
                docs.append((doc.id, doc.to_dict()))
            if docs == []:
                respond = {'status': 1}
                return respond, 404, None
            body=[]
            for doc in docs:
                body.append({'RecordID':doc[0],'record_name':doc[1]['record_name'],'log_name':doc[1]['log_name'],'user_email':doc[1]['user_email']})
            return {'status':0,'body':body},200,None
