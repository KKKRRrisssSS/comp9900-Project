# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class RecordUsernameLogNameRecordName(Resource):

    def get(self, username, log_name, record_name):
        if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
            cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred)
        print('SSSSSsS')
        db = firestore.client()
        records_ref = db.collection(u'records')
        query = records_ref.where(u'user_email', u'==', username).where(u'log_name', u'==',log_name).where(u'record_index', u'==',record_name).stream()
        docs = []
        for doc in query:
            docs.append((doc.id, doc.to_dict()))
        print(2222222222,docs)
        if docs == []:
            respond = {'status': 1}
            print(respond)
            return respond, 404, None
        body={'RecordID':docs[0][0]}
        return {'status': 0,'body':body}, 200, None