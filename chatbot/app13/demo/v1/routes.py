# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.user import User
from .api.user_verify_token import UserVerifyToken
from .api.user_is_approved_value import UserIsApprovedValue
from .api.logbook_username_logStatus import LogbookUsernameLogstatus
from .api.logbook import Logbook
from .api.logbook_LogID import LogbookLogid
from .api.record import Record
from .api.record_RecordID import RecordRecordid
from .api.record_username_log_name_record_name import RecordUsernameLogNameRecordName
from .api.session_session_id import SessionSessionId


routes = [
    dict(resource=User, urls=['/user'], endpoint='user'),
    dict(resource=UserVerifyToken, urls=['/user/<verify_token>'], endpoint='user_verify_token'),
    dict(resource=UserIsApprovedValue, urls=['/user/<is_approved>/<value>'], endpoint='user_is_approved_value'),
    dict(resource=LogbookUsernameLogstatus, urls=['/logbook/<username>/<logStatus>'], endpoint='logbook_username_logStatus'),
    dict(resource=Logbook, urls=['/logbook'], endpoint='logbook'),
    dict(resource=LogbookLogid, urls=['/logbook/<LogID>'], endpoint='logbook_LogID'),
    dict(resource=Record, urls=['/record'], endpoint='record'),
    dict(resource=RecordRecordid, urls=['/record/<RecordID>'], endpoint='record_RecordID'),
    dict(resource=RecordUsernameLogNameRecordName, urls=['/record/<username>/<log_name>/<record_name>'], endpoint='record_username_log_name_record_name'),
    dict(resource=SessionSessionId, urls=['/session/<session_id>'], endpoint='session_session_id'),
]