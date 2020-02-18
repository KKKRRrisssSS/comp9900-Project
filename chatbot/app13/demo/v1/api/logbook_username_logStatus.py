# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class LogbookUsernameLogstatus(Resource):

    def get(self, username, logStatus):
        if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
            cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        logbooks_ref = db.collection(u'logbooks')
        query = logbooks_ref.where(u'user_email', u'==', username).where(u'logStatus', u'==', logStatus).stream()
        docs = []
        for doc in query:
            docs.append((doc.id, doc.to_dict()))
        print(docs)
        if docs == []:
            respond = {'status': 1}
            print('no active')
            return respond, 404, None
        id = docs[0][0]
        print('is active')
        return {'status':0,'body':{'LogID':id}}, 200, None