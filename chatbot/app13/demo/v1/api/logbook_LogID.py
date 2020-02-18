# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore



class LogbookLogid(Resource):

    def get(self, LogID):
        if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
            cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        logs_ref = db.collection(u'logbooks')
        query = logs_ref.document(LogID)
        data = query.get().to_dict()
        if data == None:
            respond = {'status': 1}
            return respond, 200, None
        return {'status': 0,'body':data}, 200, None

    def post(self, LogID):
        if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
            cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred)
        print(g.args)
        field=g.args['field']
        value=g.args['value']
        db = firestore.client()
        logs_ref = db.collection(u'logbooks')
        logs_ref.document(LogID).update({field: value})
        return {'status':0}, 200, None