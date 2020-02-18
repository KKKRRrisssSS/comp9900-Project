# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class UserVerifyToken(Resource):

    def post(self, verify_token):
        print(g.args)
        if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
            cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred)

        db = firestore.client()
        users_ref=db.collection(u'users')

        query = users_ref.where(u'verify_token', u'==', verify_token).stream()
        docs = []
        for doc in query:
            docs.append((doc.id, doc.to_dict()))
        print(docs)
        if docs == []:
            respond = {'status': 1}
            return respond, 404, None
        print(docs)
        id = docs[0][0]
        print(type(g.args['messenger_ID']))
        doc_ref=users_ref.document(id).update({'messenger_uid': g.args['messenger_ID']})
        '''doc_ref.set({
            u'first_name': 'Hanyi',
            u'last_name': 'Lin',
            u'about_me': 'about_me',
            u'isSupervisor': False,
            u'specialist_level': 'level A',
            u'medical_specialisation': 'specialty',
            u'address_country': 'AU',
            u'address_unit': 'bb',
            u'address_first_line': 'aa',
            u'address_second_line': 'cc',
            u'address_postcode': 11,
            u'current_certification': 'level A',
            u'current_cert_expiry_day': 22,
            u'current_cert_expiry_month': 12,
            u'current_cert_expiry_year': 22,
            u'program_uid': 'hanyi@email.com',
            u'verify_token': 'abcde',
            u'messenger_ID': None,
            u'user_email': 'hanyi@email.com'
        })'''


        return {'status':0,'body':{'username':id}}, 200, None