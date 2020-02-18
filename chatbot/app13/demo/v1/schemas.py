# -*- coding: utf-8 -*-

import six
from jsonschema import RefResolver
# TODO: datetime support

class RefNode(object):

    def __init__(self, data, ref):
        self.ref = ref
        self._data = data

    def __getitem__(self, key):
        return self._data.__getitem__(key)

    def __setitem__(self, key, value):
        return self._data.__setitem__(key, value)

    def __getattr__(self, key):
        return self._data.__getattribute__(key)

    def __iter__(self):
        return self._data.__iter__()

    def __repr__(self):
        return repr({'$ref': self.ref})

    def __eq__(self, other):
        if isinstance(other, RefNode):
            return self._data == other._data and self.ref == other.ref
        elif six.PY2:
            return object.__eq__(other)
        elif six.PY3:
            return object.__eq__(self, other)
        else:
            return False

    def __deepcopy__(self, memo):
        return RefNode(copy.deepcopy(self._data), self.ref)

    def copy(self):
        return RefNode(self._data, self.ref)

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###

base_path = '/v1'

definitions = {'definitions': {}, 'parameters': {}}

validators = {
    ('user', 'GET'): {'args': {'required': [], 'properties': {'username': {'type': 'string', 'required': False}, 'verify_token': {'type': 'string', 'required': False}, 'messenger_ID': {'type': 'integer', 'required': False}, 'name': {'type': 'string', 'required': False}}}},
    ('user', 'POST'): {'args': {'required': ['messenger_ID', 'field', 'value'], 'properties': {'messenger_ID': {'type': 'string'}, 'field': {'type': 'string'}, 'value': {'type': 'string'}}}},
    ('user_verify_token', 'POST'): {'args': {'required': ['messenger_ID'], 'properties': {'messenger_ID': {'type': 'integer'}}}},
    ('logbook', 'PUT'): {'args': {'required': ['username', 'program_uid', 'log_name'], 'properties': {'username': {'type': 'string'}, 'program_uid': {'type': 'integer'}, 'log_name': {'type': 'string'}}}},
    ('logbook_LogID', 'POST'): {'args': {'required': ['field', 'value'], 'properties': {'field': {'type': 'string'}, 'value': {'type': 'string'}}}},
    ('record', 'GET'): {'args': {'required': [], 'properties': {'username': {'type': 'string', 'required': False}, 'SupervisorID': {'type': 'string', 'required': False}, 'record_status': {'type': 'string', 'required': False}}}},
    ('record_RecordID', 'POST'): {'args': {'required': ['field', 'value'], 'properties': {'field': {'type': 'string'}, 'value': {'type': 'string'}}}},
    ('session_session_id', 'POST'): {'args': {'required': ['username'], 'properties': {'username': {'type': 'string'}}}},
}

filters = {
    ('user', 'GET'): {200: {'headers': None, 'schema': {'type': 'object', 'properties': {'status': {'type': 'integer'}, 'body': {'type': 'object', 'properties': {'username': {'type': 'string'}, 'about_me': {'type': 'string'}, 'current_certification': {'type': 'string'}, 'first_name': {'type': 'string'}, 'last_name': {'type': 'string'}, 'isSupervisor': {'type': 'integer'}, 'messenger_ID': {'type': 'integer'}, 'program_uid': {'type': 'string'}, 'specialist_level': {'type': 'string'}, 'verify_token': {'type': 'string'}}}}}}, 404: {'headers': None, 'schema': {'type': 'object', 'properties': {'status': {'type': 'integer'}}}}},
    ('user', 'POST'): {200: {'headers': None, 'schema': {'type': 'object', 'properties': {'status': {'type': 'integer'}, 'body': {'type': 'object', 'properties': {'username': {'type': 'string'}}}}}}},
    ('user_verify_token', 'POST'): {200: {'headers': None, 'schema': {'type': 'object', 'properties': {'status': {'type': 'integer'}, 'body': {'type': 'object', 'properties': {'username': {'type': 'string'}}}}}}},
    ('user_is_approved_value', 'GET'): {200: {'headers': None, 'schema': {'type': 'object', 'properties': {'status': {'type': 'integer'}, 'body': {'type': 'array', 'items': {'type': 'object', 'properties': {'log_name': {'type': 'string'}, 'record_index': {'type': 'string'}, 'user_email': {'type': 'string'}, 'upload_time': {'type': 'string'}}}}}}}},
    ('logbook_username_logStatus', 'GET'): {200: {'headers': None, 'schema': {'type': 'object', 'properties': {'status': {'type': 'integer'}, 'body': {'type': 'object', 'properties': {'LogID': {'type': 'string'}}}}}}, 404: {'headers': None, 'schema': {'type': 'object', 'properties': {'status': {'type': 'integer'}, 'LogID': {'type': 'string'}}}}},
    ('logbook', 'PUT'): {200: {'headers': None, 'schema': {'type': 'object', 'properties': {'status': {'type': 'integer'}}}}},
    ('logbook_LogID', 'POST'): {200: {'headers': None, 'schema': {'type': 'object', 'properties': {'status': {'type': 'integer'}, 'body': {'type': 'object', 'properties': {'LogID': {'type': 'string'}}}}}}},
    ('logbook_LogID', 'GET'): {200: {'headers': None, 'schema': {'type': 'object', 'properties': {'status': {'type': 'integer'}, 'body': {'type': 'object', 'properties': {'cardiac_count': {'type': 'integer'}, 'correlated_case_count': {'type': 'integer'}, 'gta_count': {'type': 'integer'}, 'library_case_count': {'type': 'integer'}, 'live_case_count': {'type': 'integer'}, 'live_case_course_count': {'type': 'integer'}, 'logStatus': {'type': 'string'}, 'log_name': {'type': 'string'}, 'native_coronary_count': {'type': 'integer'}, 'non_cardiac_count': {'type': 'integer'}, 'non_coronary_count': {'type': 'integer'}, 'total_case_count': {'type': 'integer'}, 'program_uid': {'type': 'string'}}}}}}},
    ('record', 'GET'): {200: {'headers': None, 'schema': {'type': 'array', 'items': {'type': 'object', 'properties': {'RecordID': {'type': 'string'}, 'record_name': {'type': 'string'}, 'log_name': {'type': 'string'}, 'user_email': {'type': 'string'}, 'upload_day': {'type': 'integer'}, 'upload_month': {'type': 'integer'}, 'upload_year': {'type': 'integer'}, 'upload_minute': {'type': 'integer'}, 'upload_hour': {'type': 'integer'}, 'upload_second': {'type': 'integer'}}}}}, 404: {'headers': None, 'schema': {'type': 'object', 'properties': {'status': {'type': 'integer'}}}}},
    ('record_RecordID', 'GET'): {200: {'headers': None, 'schema': {'type': 'object', 'properties': {'status': {'type': 'integer'}, 'body': {'type': 'object', 'properties': {'DLP': {'type': 'number'}, 'case_type': {'type': 'string'}, 'co_reporting_doctor': {'type': 'string'}, 'facility': {'type': 'boolean'}, 'is_cardiac': {'type': 'boolean'}, 'is_correlated': {'type': 'boolean'}, 'is_gta': {'type': 'boolean'}, 'is_native_coronary': {'type': 'boolean'}, 'is_non_cardiac': {'type': 'string'}, 'is_non_coronary': {'type': 'string'}, 'log_name': {'type': 'string'}, 'record_index': {'type': 'string'}, 'record_status': {'type': 'string'}, 'user_email': {'type': 'string'}, 'log_uid': {'type': 'integer'}, 'record_date': {'type': 'integer'}, 'record_name': {'type': 'integer'}, 'record_uid': {'type': 'integer'}, 'supervisor_uid': {'type': 'integer'}, 'upload_time': {'type': 'integer'}, 'patient_details': {'type': 'string'}}}}}}, 404: {'headers': None, 'schema': {'type': 'object', 'properties': {'status': {'type': 'integer'}}}}},
    ('record_RecordID', 'POST'): {200: {'headers': None, 'schema': {'type': 'object', 'properties': {'status': {'type': 'integer'}, 'body': {'type': 'object', 'properties': {'RecordID': {'type': 'string'}}}}}}},
    ('record_username_log_name_record_name', 'GET'): {200: {'headers': None, 'schema': {'type': 'object', 'properties': {'status': {'type': 'integer'}, 'body': {'type': 'object', 'properties': {'RecordID': {'type': 'string'}}}}}}, 404: {'headers': None, 'schema': {'type': 'object', 'properties': {'status': {'type': 'integer'}, 'body': {'type': 'object', 'properties': {'RecordID': {'type': 'string'}}}}}}},
    ('session_session_id', 'GET'): {200: {'headers': None, 'schema': {'type': 'object', 'properties': {'status': {'type': 'integer'}, 'body': {'type': 'object', 'properties': {'username': {'type': 'string'}}}}}}},
    ('session_session_id', 'POST'): {200: {'headers': None, 'schema': {'type': 'object', 'properties': {'status': {'type': 'integer'}}}}},
}

scopes = {
}

resolver = RefResolver.from_schema(definitions)

class Security(object):

    def __init__(self):
        super(Security, self).__init__()
        self._loader = lambda: []

    @property
    def scopes(self):
        return self._loader()

    def scopes_loader(self, func):
        self._loader = func
        return func

security = Security()


def merge_default(schema, value, get_first=True, resolver=None):
    # TODO: more types support
    type_defaults = {
        'integer': 9573,
        'string': 'something',
        'object': {},
        'array': [],
        'boolean': False
    }

    results = normalize(schema, value, type_defaults, resolver=resolver)
    if get_first:
        return results[0]
    return results


def normalize(schema, data, required_defaults=None, resolver=None):
    if required_defaults is None:
        required_defaults = {}
    errors = []

    class DataWrapper(object):

        def __init__(self, data):
            super(DataWrapper, self).__init__()
            self.data = data

        def get(self, key, default=None):
            if isinstance(self.data, dict):
                return self.data.get(key, default)
            return getattr(self.data, key, default)

        def has(self, key):
            if isinstance(self.data, dict):
                return key in self.data
            return hasattr(self.data, key)

        def keys(self):
            if isinstance(self.data, dict):
                return list(self.data.keys())
            return list(getattr(self.data, '__dict__', {}).keys())

        def get_check(self, key, default=None):
            if isinstance(self.data, dict):
                value = self.data.get(key, default)
                has_key = key in self.data
            else:
                try:
                    value = getattr(self.data, key)
                except AttributeError:
                    value = default
                    has_key = False
                else:
                    has_key = True
            return value, has_key

    def _merge_dict(src, dst):
        for k, v in six.iteritems(dst):
            if isinstance(src, dict):
                if isinstance(v, dict):
                    r = _merge_dict(src.get(k, {}), v)
                    src[k] = r
                else:
                    src[k] = v
            else:
                src = {k: v}
        return src

    def _normalize_dict(schema, data):
        result = {}
        if not isinstance(data, DataWrapper):
            data = DataWrapper(data)

        for _schema in schema.get('allOf', []):
            rs_component = _normalize(_schema, data)
            _merge_dict(result, rs_component)

        for key, _schema in six.iteritems(schema.get('properties', {})):
            # set default
            type_ = _schema.get('type', 'object')

            # get value
            value, has_key = data.get_check(key)
            if has_key or '$ref' in _schema:
                result[key] = _normalize(_schema, value)
            elif 'default' in _schema:
                result[key] = _schema['default']
            elif key in schema.get('required', []):
                if type_ in required_defaults:
                    result[key] = required_defaults[type_]
                else:
                    errors.append(dict(name='property_missing',
                                       message='`%s` is required' % key))

        additional_properties_schema = schema.get('additionalProperties', False)
        if additional_properties_schema is not False:
            aproperties_set = set(data.keys()) - set(result.keys())
            for pro in aproperties_set:
                result[pro] = _normalize(additional_properties_schema, data.get(pro))

        return result

    def _normalize_list(schema, data):
        result = []
        if hasattr(data, '__iter__') and not isinstance(data, (dict, RefNode)):
            for item in data:
                result.append(_normalize(schema.get('items'), item))
        elif 'default' in schema:
            result = schema['default']
        return result

    def _normalize_default(schema, data):
        if data is None:
            return schema.get('default')
        else:
            return data

    def _normalize_ref(schema, data):
        if resolver == None:
            raise TypeError("resolver must be provided")
        ref = schema.get(u"$ref")
        scope, resolved = resolver.resolve(ref)
        if resolved.get('nullable', False) and not data:
            return {}
        return _normalize(resolved, data)

    def _normalize(schema, data):
        if schema is True or schema == {}:
            return data
        if not schema:
            return None
        funcs = {
            'object': _normalize_dict,
            'array': _normalize_list,
            'default': _normalize_default,
            'ref': _normalize_ref
        }
        type_ = schema.get('type', 'object')
        if type_ not in funcs:
            type_ = 'default'
        if schema.get(u'$ref', None):
            type_ = 'ref'

        return funcs[type_](schema, data)

    return _normalize(schema, data), errors
