# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class User(Resource):

    def get(self):
        print(g.args)
        if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
            cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred)

        db = firestore.client()
        users_ref = db.collection(u'users')

        if 'username' in g.args.keys():
            query = users_ref.document(g.args['username'])
            data = query.get().to_dict()
            if data == None:
                respond = {'status': 1}
                return respond, 200, None
            print(data)
            body = {'username': query.id,
                    'current_certification': data['current_certification'], 'first_name': data['first_name'],
                    'last_name': data['last_name'], 'isSupervisor': data['supervisor_approved'],
                    'messenger_ID': data['messenger_uid'], 'program_uid': data['program_uid'],
                    'specialist_level': data['specialist_level'], 'verify_token': data['verify_token']}
            respond = {'status': 0, 'body': body}
            return respond, 200, None
        if 'verify_token' in g.args.keys():
            query = users_ref.where(u'verify_token', u'==', g.args['verify_token']).stream()
            docs = []
            for doc in query:
                docs.append((doc.id, doc.to_dict()))
            if docs == []:
                respond = {'status': 1}
                return respond, 404, None
            print(docs)
            id = docs[0][0]
            data = docs[0][1]
            body = {'username': id,
                    'current_certification': data['current_certification'], 'first_name': data['first_name'],
                    'last_name': data['last_name'], 'isSupervisor': data['supervisor_approved'],
                    'messenger_ID': data['messenger_uid'], 'program_uid': data['program_uid'],
                    'specialist_level': data['specialist_level'], 'verify_token': data['verify_token']}
            respond = {'status': 0, 'body': body}
            return respond, 200, None
        if 'messenger_ID' in g.args.keys():
            query = users_ref.where(u'messenger_uid', u'==', g.args['messenger_ID']).stream()
            docs = []
            for doc in query:
                docs.append((doc.id, doc.to_dict()))
            if docs == []:
                respond = {'status': 1}
                return respond, 404, None
            print(docs)
            id = docs[0][0]
            data = docs[0][1]
            body = {'username': id,
                    'current_certification': data['current_certification'], 'first_name': data['first_name'],
                    'last_name': data['last_name'], 'isSupervisor': data['supervisor_approved'],
                    'messenger_ID': data['messenger_uid'], 'program_uid': data['program_uid'],
                    'specialist_level': data['specialist_level'], 'verify_token': data['verify_token']}
            respond = {'status': 0, 'body': body}
            return respond, 200, None

        if 'name' in g.args.keys():
            try:
                first_name, last_name = g.args['name'].split('_')
            except ValueError:
                respond = {'status': 2}
                return respond, 200, None
            query = users_ref.where(u'first_name', u'==', first_name).where(u'last_name', u'==', last_name).stream()
            docs = []
            for doc in query:
                docs.append((doc.id, doc.to_dict()))
            if docs == []:
                respond = {'status': 1}
                return respond, 404, None
            print(docs)
            id = docs[0][0]
            data = docs[0][1]
            body = {'username': id,
                    'current_certification': data['current_certification'], 'first_name': data['first_name'],
                    'last_name': data['last_name'], 'isSupervisor': data['supervisor_approved'],
                    'messenger_ID': data['messenger_uid'], 'program_uid': data['program_uid'],
                    'specialist_level': data['specialist_level'], 'verify_token': data['verify_token']}
            respond = {'status': 0, 'body': body}
            return respond, 200, None


    def post(self):
        print(g.args)
        if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
            cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred)

        db = firestore.client()
        users_ref=db.collection(u'users')


        messenger_ID=int(g.args['messenger_ID'])
        field=g.args['field']
        if g.args['value']=='None':
            value=None
        else:
            value=g.args['value']
        query = users_ref.where(u'messenger_uid', u'==', messenger_ID).stream()
        docs = []
        for doc in query:
            docs.append((doc.id, doc.to_dict()))
        print('!!!!!!!',docs)
        if docs == []:
            respond = {'status': 1}
            return respond, 404, None
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(docs)
        id = docs[0][0]
        print(id,field,value)
        users_ref.document(id).update({field: value})

        return {'status':0,'body':{'username':id}}, 200, None