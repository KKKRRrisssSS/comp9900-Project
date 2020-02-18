# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import string
import random
import datetime
import datetime

class Logbook(Resource):

    def put(self):
        print(g.args)
        if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
            cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred)

        db = firestore.client()
        logbook_ref = db.collection(u'logbooks')

        programs = {1: 'level_a_certification', 2: 'level_a_recertification', 3: 'level_b_certification',
                    4: 'level_b_recertification', 5: 'level_a_to_b_conversion'}
        username=g.args['username']
        program_uid = programs[g.args['program_uid']]
        log_name=g.args['log_name']
        allchar = string.ascii_uppercase+ string.digits
        Log_ID = ''.join(random.choice(allchar) for _ in range(20))
        today = datetime.date.today()
        create_time=datetime.datetime.now()
        doc_ref = logbook_ref.document(Log_ID)
        doc_ref.set({
            u'graft_thoracic_aorta_count': 0,
            u'library_case_count': 0,
            u'live_case_count': 0,
            u'live_case_course_count': 0,
            u'logStatus': 'activated',
            u'native_coronary_count': 0,
            u'non_cardiac_count': 0,
            u'non_coronary_cardiac_count': 0,
            u'program_uid': program_uid,
            u'user_email': username,
            u'create_time': create_time,
            u'log_uid':Log_ID,
            u'log_name':log_name})

        return {'status':1}, 200, None