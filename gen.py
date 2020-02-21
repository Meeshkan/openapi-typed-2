import openapi_typed_2
from collections.abc import Sequence, Mapping

_TO_DICT_SUBS = {'_license': 'license', '_format': 'format', '_in': 'in', '_ref': '$ref', '_not': 'not', '_type': 'type', '_default': 'default'}

def _simple_prop(n: str, q: str, K: str, tp: str) -> str:
    O = '''    {}: {}
    if '{}' not in d:
        raise ValueError('{} must be defined for {}')
    if not isinstance(d['{}'], {}):
        raise ValueError('{} must be of type `{}` in {}, instead got %s' % str(type(d['{}'])))
    {} = cast({}, d['{}'])
'''.format(n, tp, q, q, K, q, tp, q, tp, K, q, n, tp, q)
    return O

def _simple_prop_opt(n: str, q: str, K: str, tp: str) -> str:
    O = '''    {}: Optional[{}]
    if '{}' not in d:
        {} = None
    elif not isinstance(d['{}'], {}):
        raise ValueError('{} must be of type `{}` in {}, instead got %s' % str(type(d['{}'])))
    else:
        {} = cast({}, d['{}'])
'''.format(n, tp, q, n, q, tp, q, tp, K, q, n, tp, q)
    return O

# Optional[Mapping[str, Union[Link, Reference]]]
def _omsu_r(n: str, q: str, K: str, tp: str):
    O = '''    {}: Optional[Mapping[str, Union[{}, Reference]]]
    if '{}' not in d:
        {} = None
    elif not isinstance(d['{}'], dict):
        raise ValueError('{} must be of type `dict` in {}, instead got %s' % str(type(d['{}'])))
    else:
        _ret = dict()
        for k, v in d['{}'].items():
            if type(k) != str:
                raise ValueError('{} in {} can only have string keys, but encountered %s.' % k)
            e: Exception = ValueError('')
            try:
                _ret[k] = convert_to_Reference(v)
            except:
                try:
                    _ret[k] = convert_to_{}(v)
                except Exception as ee:
                    e = ee
            if k not in _ret:
                #raise ValueError('%s\\n{} in {} at key %s has a value %s which cannot be cast to Union[{}, Reference].' % (str(e), k, str(v)))
                raise e
        {} = cast(Mapping[str, Union[{}, Reference]], _ret)
'''.format(n, tp, q, n, q, q, K, q, q, q, K, tp, q, K, tp, n, tp)
    return O

# Optional[Sequence[Union[Schema, Reference]]]
def _osu_r(n: str, q: str, K: str, tp: str):
    O = '''    {}: Optional[Sequence[Union[{}, Reference]]]
    if '{}' not in d:
        {} = None
    elif not isinstance(d['{}'], list):
        raise ValueError('{} must be of type `dict` in {}, instead got %s' % str(type(d['{}'])))
    else:
        _ret = []
        for k in d['{}']:
            _lr = len(_ret)
            e: Exception = ValueError('')
            try:
                _ret.append(convert_to_Reference(k))
            except:
                try:
                    _ret.append(convert_to_{}(k))
                except Exception as ee:
                    e = ee
            if _lr == len(_ret):
                #raise ValueError('%s\\n{} in {} has a value %s which cannot be cast to Union[{}, Reference].' % (str(e), str(k)))
                raise e
        {} = cast(Sequence[Union[{}, Reference]], _ret)
'''.format(n, tp, q, n, q, q, K, q, q, tp, q, K, tp, n, tp)
    return O

# Optional[Union[Sequence[Union[Schema, Reference]], Schema, Reference]]
def _ousu_r_r(n: str, q: str, K: str, tp: str):
    O = '''    {}: Optional[Union[Sequence[Union[{}, Reference]], {}, Reference]]
    if '{}' not in d:
        {} = None
    elif not isinstance(d['{}'], list):
        try:
            {} = convert_to_Reference(d['{}'])
        except:
            try:
                {} = convert_to_{}(d['{}'])
            except Exception as e:
                #raise ValueError('%s\\n{} in {} cannot be cast to Union[{}, Reference].' % str(e))
                raise e
    else:
        _ret = []
        for k in d['{}']:
            _lr = len(_ret)
            e: Exception = ValueError('')
            try:
                _ret.append(convert_to_Reference(k))
            except:
                try:
                    _ret.append(convert_to_{}(k))
                except Exception as ee:
                    e = ee
            if _lr == len(_ret):
                # raise ValueError('%s\\n{} in {} has a value %s which cannot be cast to Union[{}, Reference].' % (str(e), str(k)))
                raise e
        {} = cast(Sequence[Union[{}, Reference]], _ret)
'''.format(n, tp, tp, q, n, q, n, q, n, tp, q, q, K, tp, q, K, q, q, tp, q, K, tp, n, tp)
    return O

# Optional[Union[bool, int]]
def oubi(n, q, K):
    O = '''    {}: Optional[Union[bool, int]]
    if '{}' not in d:
        {} = None
    elif (not isinstance(d['{}'], bool)) and (not isinstance(d['{}'], int)):
        raise ValueError('{} must be of type `bool` or `int` in {}, instead got %s' % str(type(d['{}'])))
    else:
        {} = cast(Union[bool, int], d['{}'])
'''.format(n, q, n, q, q, q, K, q, n, q)
    return O

# Optional[Union[Schema, Reference]]
def _ou_r(n: str, q: str, K: str, tp: str):
    O = '''    {}: Optional[Union[{}, Reference]]
    if '{}' not in d:
        {} = None
    elif not isinstance(d['{}'], dict):
        raise ValueError('{} must be of type `dict` in {}, instead got %s' % str(type(d['{}'])))
    else:
        try:
            {} = convert_to_Reference(d['{}'])
        except:
            try:
                {} = convert_to_{}(d['{}'])
            except Exception as e:
                # raise ValueError('%s\\n{} in {} has a value %s which cannot be cast to Union[{}, Reference].' % str(e))
                raise e
'''.format(n, tp, q, n, q, q, K, q, n, q, n, tp, q, q, K, tp)
    return O

# Optional[Union[Schema, Reference, bool]]
def _ou_rb(n: str, q: str, K: str, tp: str):
    O = '''    {}: Optional[Union[{}, Reference, bool]]
    if '{}' not in d:
        {} = None
    else:
        try:
            {} = convert_to_Reference(d['{}'])
        except:
            try:
                {} = convert_to_{}(d['{}'])
            except:
                if isinstance(d['{}'], bool):
                    {} = d['{}']
                else:
                    raise ValueError('{} in {} cannot be cast to Union[{}, Reference].')
'''.format(n, tp, q, n, n, q, n, tp, q, n, q, n, q, q, K, tp)
    return O


# Optional[Mapping[str, ServerVariable]]
def _oms_r(n: str, q: str, K: str, tp: str):
    O = '''    {}: Optional[Mapping[str, {}]]
    if '{}' not in d:
        {} = None
    elif not isinstance(d['{}'], dict):
        raise ValueError('{} must be of type `dict` in {}, instead got %s' % str(type(d['{}'])))
    else:
        _ret = dict()
        for k, v in d['{}'].items():
            e: Exception = ValueError('')
            if type(k) != str:
                raise ValueError('{} in {} can only have string keys, but encountered %s.' % k)
            try:
                _ret[k] = convert_to_{}(v)
            except Exception as ee:
                e = ee
            if k not in _ret:
                #raise ValueError('%s\\n{} in {} at key %s has a value %s which cannot be cast to {}.' % (str(e), k, str(v)))
                raise e
        {} = cast(Mapping[str, {}], _ret)
'''.format(n, tp, q, n, q, q, K, q, q, q, K, tp, q, K, tp, n, tp)
    return O

# Mapping[str, MediaType]
def _ms_r(n: str, q: str, K: str, tp: str):
    O = '''    {}: Mapping[str, {}]
    if '{}' not in d:
        raise ValueError('{} must be present in {}')
    elif not isinstance(d['{}'], dict):
        raise ValueError('{} must be of type `dict` in {}, instead got %s' % str(type(d['{}'])))
    else:
        _ret = dict()
        for k, v in d['{}'].items():
            e: Exception = ValueError('')
            if type(k) != str:
                raise ValueError('{} in {} can only have string keys, but encountered %s.' % k)
            try:
                _ret[k] = convert_to_{}(v)
            except Exception as ee:
                e = ee
            if k not in _ret:
                #raise ValueError('%s {} in {} at key %s has a value %s which cannot be cast to {}.' % (str(e), k, str(v)))
                raise e
        {} = cast(Mapping[str, {}], _ret)
'''.format(n, tp, q, q, K, q, q, K, q, q, q, K, tp, q, K, tp, n, tp)
    return O

# Optional[Sequence[str]]
def _oss_r(n: str, q: str, K: str, tp: str):
    O = '''    {}: Optional[Sequence[{}]]
    if '{}' not in d:
        {} = None
    elif not isinstance(d['{}'], list):
        raise ValueError('{} must be of type `list` in {}, instead got %s' % str(type(d['{}'])))
    else:
        _ret = []
        for k in d['{}']:
            try:
                _ret.append(convert_to_{}(k))
            except Exception as e:
                #raise ValueError('%s\\n{} in {} has a value %s which cannot be cast to {}.' % (str(e), str(k)))
                raise e
        {} = cast(Sequence[{}], _ret)
'''.format(n, tp, q, n, q, q, K, q, q, tp, q, K, tp, n, tp)
    return O

# AuthorizationCodeOAuthFlow
def _kls(n: str, q: str, K: str, tp: str):
    O = '''    {}: {}
    if '{}' not in d:
        raise ValueError('{} must be defined for {}')
    try:
        {} = convert_to_{}(d['{}'])
    except Exception as e:
        #raise ValueError('%s\\n{} must be of type `{}` in {}, instead got %s' % (str(e), str(type(d['{}']))))
        raise e
'''.format(n, tp, q, q, K, n, tp, q, q, tp, K, q)
    return O

# Optional[License]
def _kls_o(n: str, q: str, K: str, tp: str):
    O = '''    {}: Optional[{}]
    if '{}' not in d:
        {} = None
    else:
        try:
            {} = convert_to_{}(d['{}'])
        except Exception as e:
            #raise ValueError('%s\\n{} must be of type `{}` in {}, instead got %s' % (str(e), str(type(d['{}']))))
            raise e
'''.format(n, tp, q, n, n, tp, q, q, tp, K, q)
    return O


def _AuthorizationCodeOAuthFlow(n, q, K):
    return _kls(n, q, K, 'AuthorizationCodeOAuthFlow')

def _Paths(n, q, K):
    return _kls(n, q, K, 'Paths')

def _Info(n, q, K):
    return _kls(n, q, K, 'Info')

def _ImplicitOAuthFlow(n, q, K):
    return _kls(n, q, K, 'ImplicitOAuthFlow')

def _PasswordOAuthFlow(n, q, K):
    return _kls(n, q, K, 'PasswordOAuthFlow')

def _ClientCredentialsFlow(n, q, K):
    return _kls(n, q, K, 'ClientCredentialsFlow')

def _OAuthFlows(n, q, K):
    return _kls(n, q, K, 'OAuthFlows')

def _Schema(n, q, K):
    return _kls(n, q, K, 'Schema')

def _Reference(n, q, K):
    return _kls(n, q, K, 'Reference')

def __Server(n, q, K):
    return _kls_o(n, q, K, 'Server')

def __Components(n, q, K):
    return _kls_o(n, q, K, 'Components')

def __ExternalDocumentation(n, q, K):
    return _kls_o(n, q, K, 'ExternalDocumentation')

def __Contact(n, q, K):
    return _kls_o(n, q, K, 'Contact')

def __Discriminator(n, q, K):
    return _kls_o(n, q, K, 'Discriminator')

def __Operation(n, q, K):
    return _kls_o(n, q, K, 'Operation')

def __License(n, q, K):
    return _kls_o(n, q, K, 'License')

def __XML(n, q, K):
    return _kls_o(n, q, K, 'XML')

def __Any(n, q, K):
    return _kls_o(n, q, K, 'Any')

def _Responses(n, q, K):
    return _kls(n, q, K, 'Responses')

def oususrsr(n: str, q: str, K: str):
    return _ousu_r_r(n, q, K, 'Schema')

def ousr(n: str, q: str, K: str):
    return _ou_r(n, q, K, 'Schema')

def ousrb(n: str, q: str, K: str):
    return _ou_rb(n, q, K, 'Schema')

def ourr(n: str, q: str, K: str):
    return _ou_r(n, q, K, 'RequestBody')

def msmr(n: str, q: str, K: str):
    return _ms_r(n, q, K, 'MediaType')

def omsusr(n: str, q: str, K: str):
    return _omsu_r(n, q, K, 'Schema')

def omsulr(n: str, q: str, K: str):
    return _omsu_r(n, q, K, 'Link')

def omsuhr(n: str, q: str, K: str):
    return _omsu_r(n, q, K, 'Header')

def omsupr(n: str, q: str, K: str):
    return _omsu_r(n, q, K, 'Parameter')

def omsuer(n: str, q: str, K: str):
    return _omsu_r(n, q, K, 'Example')

def omsucr(n: str, q: str, K: str):
    return _omsu_r(n, q, K, 'Callback')

def omsurr(n: str, q: str, K: str):
    return _omsu_r(n, q, K, 'RequestBody')

def omsurrr(n: str, q: str, K: str):
    return _omsu_r(n, q, K, 'Response')

def omsussr(n: str, q: str, K: str):
    return _omsu_r(n, q, K, 'SecurityScheme')

def omssr(n: str, q: str, K: str):
    return _oms_r(n, q, K, 'ServerVariable')

def omsar(n: str, q: str, K: str):
    return _oms_r(n, q, K, 'Any')

def omstr(n: str, q: str, K: str):
    return _oms_r(n, q, K, 'str')

def mstr(n: str, q: str, K: str):
    return _ms_r(n, q, K, 'str')

def omshr(n: str, q: str, K: str):
    return _oms_r(n, q, K, 'Header')

def omser(n: str, q: str, K: str):
    return _oms_r(n, q, K, 'Encoding')

def omsmr(n: str, q: str, K: str):
    return _oms_r(n, q, K, 'MediaType')

def osstr(n: str, q: str, K: str):
    return _oss_r(n, q, K, 'str')

def ossar(n: str, q: str, K: str):
    return _oss_r(n, q, K, 'Any')

def ossgr(n: str, q: str, K: str):
    return _oss_r(n, q, K, 'Tag')

def ossqr(n: str, q: str, K: str):
    return _oss_r(n, q, K, 'SecurityRequirement')

def osssr(n: str, q: str, K: str):
    return _oss_r(n, q, K, 'Server')

def osusr(n: str, q: str, K: str):
    return _osu_r(n, q, K, 'Schema')

def osupr(n: str, q: str, K: str):
    return _osu_r(n, q, K, 'Parameter')

def sstr(n: str, q: str, K: str) -> str:
    return _simple_prop(n, q, K, 'str')

def sint(n: str, q: str, K: str) -> str:
    return _simple_prop(n, q, K, 'int')

def sbool(n: str, q: str, K: str) -> str:
    return _simple_prop(n, q, K, 'bool')

def sfloat(n: str, q: str, K: str) -> str:
    return _simple_prop(n, q, K, 'float')

def sstro(n: str, q: str, K: str) -> str:
    return _simple_prop_opt(n, q, K, 'str')

def sinto(n: str, q: str, K: str) -> str:
    return _simple_prop_opt(n, q, K, 'int')

def sboolo(n: str, q: str, K: str) -> str:
    return _simple_prop_opt(n, q, K, 'bool')

def sfloato(n: str, q: str, K: str) -> str:
    return _simple_prop_opt(n, q, K, 'float')

_CONVERTERS = {
    'float': sfloat,
    'str': sstr,
    'int': sint,
    'bool': sbool,
    'AuthorizationCodeOAuthFlow': _AuthorizationCodeOAuthFlow,
    'Responses': _Responses,
    'OAuthFlows': _OAuthFlows,
    'Optional[float]': sfloato,
    'Optional[str]': sstro,
    'Optional[int]': sinto,
    'Optional[bool]': sboolo,
    'Optional[License]': __License,
    'Optional[Operation]': __Operation,
    'PasswordOAuthFlow': _PasswordOAuthFlow,
    'Optional[Contact]': __Contact,
    'Optional[Components]': __Components,
    'Optional[Any]': __Any,
    'Optional[Discriminator]': __Discriminator,
    'Optional[Components]': __Components,
    'Optional[ExternalDocumentation]': __ExternalDocumentation,
    'Optional[Mapping[str, Any]]': omsar,
    'Optional[Mapping[str, str]]': omstr,
    'Optional[Mapping[str, Header]]': omshr,
    'Optional[Mapping[str, ServerVariable]]': omssr,
    'Optional[Mapping[str, MediaType]]': omsmr,
    'Optional[Mapping[str, Encoding]]': omser,
    'Optional[Mapping[str, Union[Callback, Reference]]]': omsucr,
    'Optional[Mapping[str, Union[Link, Reference]]]': omsulr,
    'Optional[Mapping[str, Union[Header, Reference]]]': omsuhr,
    'Optional[Mapping[str, Union[Schema, Reference]]]': omsusr,
    'Optional[Mapping[str, Union[Parameter, Reference]]]': omsupr,
    'Optional[Mapping[str, Union[Example, Reference]]]': omsuer,
    'Optional[Mapping[str, Union[RequestBody, Reference]]]': omsurr,
    'Optional[Mapping[str, Union[Response, Reference]]]': omsurrr,
    'Optional[Mapping[str, Union[SecurityScheme, Reference]]]': omsussr,
    'Optional[Union[Sequence[Union[Schema, Reference]], Schema, Reference]]': oususrsr,
    'Optional[Sequence[Union[Schema, Reference]]]': osusr,
    'Optional[Sequence[Union[Parameter, Reference]]]': osupr,
    'Optional[Sequence[str]]': osstr,
    'Optional[Sequence[Server]]': osssr,
    'Optional[Sequence[Any]]': ossar,
    'Optional[Sequence[Tag]]': ossgr,
    'Optional[Sequence[SecurityRequirement]]': ossqr,
    'Optional[Union[Schema, Reference]]': ousr,
    'Optional[Union[RequestBody, Reference]]': ourr,
    'Optional[Union[Schema, Reference, bool]]': ousrb,
    'Paths': _Paths,
    'Optional[Server]': __Server,
    'Optional[XML]': __XML,
    'ClientCredentialsFlow': _ClientCredentialsFlow,
    'Schema': _Schema,
    'Reference': _Reference,
    'Info': _Info,
    'ImplicitOAuthFlow': _ImplicitOAuthFlow,
    'Mapping[str, str]': mstr,
    'Mapping[str, MediaType]': msmr,
    'Optional[Union[bool, int]]': oubi
}

with open('openapi_typed_2/openapi.py', 'r') as oai:
    OAI = oai.read()
    fl = [x for x in OAI.replace('@dataclass\n','').split('class')[1:]]
    fl = [[y for y in x.split('\n') if y not in ['@data', '']] for x in fl]
    types = list(set([q.replace("'", "") for q in sum([[y.split(':')[1].split('#')[0].strip() for y in x if ':' in y] for x in fl], []) if q not in ['', 'ignore']]))
    uc = [x for x in types if x not in _CONVERTERS]
    OUT = '''from typing import cast, Sequence, Union, Any, Mapping, Optional
from .openapi import *
from dataclasses import is_dataclass, fields

_TO_DICT_SUBS = {'_license': 'license', '_format': 'format', '_in': 'in', '_ref': '$ref', '_not': 'not', '_type': 'type', '_default': 'default'}

def convert_to_str(d: Any) -> str:
    if not isinstance(d, str):
        raise ValueError('%s is not a string' % str(d))
    return cast(str, d)

def convert_to_sequence_str(d: Any) -> Sequence[str]:
    if not isinstance(d, list):
        raise ValueError('%s is not a list' % str(d))
    for x in d:
        if not isinstance(x, str):
            raise ValueError('%s is not a str' % str(x))
    return cast(str, d)

def convert_to_Responses(d: Any) -> Responses:
    responses: Responses
    if not isinstance(d, dict):
        raise ValueError('obj must be of type `dict`, instead got %s' % str(type(d)))
    else:
        _ret = dict()
        for k, v in d.items():
            e: Exception = ValueError('')
            if type(k) != str:
                raise ValueError('obj can only have string keys, but encountered %s.' % k)
            try:
                _ret[k] = convert_to_Reference(v)
            except:
                try:
                    _ret[k] = convert_to_Response(v)
                except Exception as ee:
                    e = ee
            if k not in _ret:
                raise e #ValueError('%s\\nKey %s has a value %s which cannot be cast to Union[Response, Reference].' % (str(e), k, str(v)))
        responses = cast(Responses, _ret)
    return responses

def convert_to_Callback(d: Any) -> Callback:
    callback: Callback
    if not isinstance(d, dict):
        raise ValueError('obj must be of type `dict`, instead got %s' % str(type(d)))
    else:
        _ret = dict()
        for k, v in d.items():
            if type(k) != str:
                raise ValueError('obj can only have string keys, but encountered %s.' % k)
            try:
                _ret[k] = convert_to_PathItem(v)
            except Exception as e:
                raise ValueError('%s\\nKey %s has a value %s which cannot be cast to PathItem.' % (str(e), k, str(v)))
        callback = cast(Callback, _ret)
    return callback

def convert_to_Paths(d: Any) -> Paths:
    paths: Paths
    if not isinstance(d, dict):
        raise ValueError('obj must be of type `dict`, instead got %s' % str(type(d)))
    else:
        _ret = dict()
        for k, v in d.items():
            if type(k) != str:
                raise ValueError('obj can only have string keys, but encountered %s.' % k)
            try:
                _ret[k] = convert_to_PathItem(v)
            except Exception as e:
                raise ValueError('%s\\nKey %s has a value %s which cannot be cast to PathItem.' % (str(e), k, str(v)))
        paths = cast(Paths, _ret)
    return paths

def convert_to_SecurityRequirement(d: Any) -> SecurityRequirement:
    securityRequirement: SecurityRequirement
    if not isinstance(d, dict):
        raise ValueError('obj must be of type `dict`, instead got %s' % str(type(d)))
    else:
        _ret = dict()
        for k, v in d.items():
            if type(k) != str:
                raise ValueError('obj can only have string keys, but encountered %s.' % k)
            try:
                _ret[k] = convert_to_sequence_str(v)
            except:
                raise ValueError('Key %s has a value %s which cannot be cast to PathItem.' % (k, str(v)))
        securityRequirement = cast(SecurityRequirement, _ret)
    return securityRequirement

def convert_to_SecurityScheme(d: Any) -> SecurityScheme:
    try:
        return convert_to_APIKeySecurityScheme(d)
    except:
        try:
            return convert_to_HTTPSecurityScheme(d)
        except:
            try:
                return convert_to_OAuth2SecurityScheme(d)
            except:
                try:
                    return convert_to_OpenIdConnectSecurityScheme(d)
                except:
                    if isinstance(d, str):
                        return cast(str, d)
                    else:
                        raise ValueError('%s is not a valid SecurityScheme' % str(d))

def convert_to_Any(d: Any) -> Any:
    return d

'''
    sp = OAI.split('\n')
    n = 0
    inclass = False
    curr = None
    props = []
    while True:
        x = sp[n]
        if (x == '') and inclass:
            OUT += '    _x = { k: v for k,v in d.items() if k[:2] == "x-" }\n'
            OUT += '    return %s(\n' % curr
            for p in props:
                if p == '_x':
                    continue
                OUT += '        %s=%s,\n' % (p, p)
            OUT += '        _x=_x if len(_x) > 0 else None\n'
            OUT += '    )\n'
            inclass = False
            props.clear()
            OUT += '\n'
        if inclass:
            o = x.split(':')
            name = o[0].strip()
            _type = o[1].split('#')[0].replace("'","").strip()
            props.append(name)
            OUT += _CONVERTERS[_type](name, _TO_DICT_SUBS.get(name, name), curr)
        if ('class ' in x) and (':' in x):
            curr = x.split(' ')[1].split(':')[0]
            inclass = True
            OUT += 'def convert_to_%s(d: Any) -> %s:\n' % (curr, curr)
            OUT += '    if not isinstance(d, dict):\n'
            OUT += '        raise ValueError("%s must be a dictionary")\n' % curr
        n += 1
        if n >= len(sp):
            break
    OUT += '''
def convert_from_openapi(d: Any) -> Any:
    if is_dataclass(d):
        return {
            **({ k: v for k, v in d._x.items() } if hasattr(d, '_x') and (d._x is not None) else {}),
            **{
                _TO_DICT_SUBS.get(k, k): convert_from_openapi(getattr(d, k)) for k in [r.name for r in fields(d)] if (k != '_x') and (getattr(d, k) is not None)
            }
        }
    elif isinstance(d, dict):
        return { k: convert_from_openapi(v) for k, v in d.items() }
    elif isinstance(d, list):
        return [convert_from_openapi(x) for x in d]
    else:
        return d

convert_to_openapi = convert_to_OpenAPIObject
'''
    with open('openapi_typed_2/converters.py', 'w') as conv:
        conv.write(OUT)