# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class SessionSessionId(Resource):

    def get(self, session_id):
        if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
            cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        sessions_ref = db.collection(u'sessions')
        query = sessions_ref.document(session_id)
        data = query.get().to_dict()
        if data == None:
            respond = {'status': 1}
            return respond, 200, None
        print(data)
        body={'username':data['username']}
        respond = {'status': 0, 'body': body}
        return respond, 200, None

    def post(self, session_id):
        print(g.args)
        if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
            cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred)
        username=g.args['username']
        db = firestore.client()
        sessions_ref = db.collection(u'sessions')
        doc_ref = sessions_ref.document(session_id)
        doc_ref.set({u'username':username})

        return {'status':1}, 200, None