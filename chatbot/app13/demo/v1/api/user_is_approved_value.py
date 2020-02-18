# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class UserIsApprovedValue(Resource):

    def get(self, is_approved, value):
        if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
            cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred)
        username = value
        db = firestore.client()
        records_ref = db.collection(u'records')
        query = records_ref.where(u'is_approved', u'==', False).where(u'record_status', u'==', 'Completed').stream()
        #username=value
        docs=[]
        for doc in query:
            docs.append((doc.id,doc.to_dict()))
        print(docs)
        body = []
        for doc in docs:
            if doc[1]['user_email']!=username:
                body.append({'upload_time': doc[1]['upload_time'], 'record_index': doc[1]['record_name'], 'log_name': doc[1]['log_name'],
                         'user_email': doc[1]['user_email']})
        print('!!!!!!!!!',body)
        print(username)
        if body == []:
            respond = {'status': 1,'body':body}
            print(respond)
            return respond, 404, None
        print(body)
        return {'status': 0,'body':body}, 200, None
