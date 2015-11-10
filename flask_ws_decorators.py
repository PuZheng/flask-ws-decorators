# -*- coding: UTF-8 -*-
import pprint
import json
import types
import time
from functools import partial, wraps
from flask import request, current_app, jsonify, after_this_request
from flask.ext.login import login_required as __login_required__
from cStringIO import StringIO as IO
import gzip

sep = '-' * 16


def dump_request(*args):

    def decorator(f, methods=None):

        def _f(*args, **kwargs):
            if current_app.config.get('WS_DECORATORS_ENABLED') and \
                    (methods is None or request.method in methods):
                print sep + ' REQUEST PAYLOAD ' + sep
                if request.form:
                    print ';; FORM'
                    pprint.pprint(request.form.to_dict())
                if request.json:
                    print ':: JSON'
                    pprint.pprint(request.json)
                print sep + ' REQUEST PAYLOAD END ' + sep + '\n'
            return f(*args, **kwargs)

        _f.__name__ = f.__name__

        return _f

    if hasattr(args[0], '__iter__'):
        return partial(decorator, methods=args[0])

    assert isinstance(args[0], types.FunctionType)
    return decorator(args[0])


def dump_respond(*args):

    f = args[0]

    def _f(*args, **kwargs):
        ret = f(*args, **kwargs)
        print sep + ' RESPOND DATA ' + sep
        if isinstance(ret, types.TupleType):
            data = json.loads(ret[0].response[0])
        elif hasattr(ret, 'response'):
            data = json.loads(ret.response[0])
        else:
            data = ret
        pprint.pprint(data)
        print sep + ' RESPOND DATA END ' + sep
        return ret

    _f.__name__ = f.__name__
    return _f


def wait_for(seconds):

    def _decorator(f):

        def _f(*args, **kwargs):
            ret = f(*args, **kwargs)
            if current_app.config.get('WS_DECORATORS_ENABLED'):
                time.sleep(seconds)
            return ret

        _f.__name__ = f.__name__

        return _f
    return _decorator


def fake_error(arg):
    '''
    :param arg: the decorated function, or an error message. for example:

        @fake_error
        def view1():
            pass

        @fake_error(u'this is joking')
        def view2():
            pass

        are both accepted
    '''

    if isinstance(arg, basestring):

        def _decorator(f):

            def _f():
                return jsonify({
                    'msg': arg,
                }), 403

            _f.__name__ = f.__name__
            return _f

        return _decorator
    else:
        assert isinstance(arg, types.FunctionType)

        f = arg

        def _f():
            return jsonify({
                'msg': u'a faked error',
            }), 403

        _f.__name__ = f.__name__
        return _f


def gzipped(f):
    @wraps(f)
    def view_func(*args, **kwargs):
        @after_this_request
        def zipper(response):
            accept_encoding = request.headers.get('Accept-Encoding', '')

            if 'gzip' not in accept_encoding.lower():
                return response

            response.direct_passthrough = False

            if response.status_code < 200 or response.status_code >= 300 or \
                    'Content-Encoding' in response.headers:
                return response
            gzip_buffer = IO()
            gzip_file = gzip.GzipFile(mode='wb',
                                      fileobj=gzip_buffer)
            gzip_file.write(response.data)
            gzip_file.close()

            response.data = gzip_buffer.getvalue()
            response.headers['Content-Encoding'] = 'gzip'
            response.headers['Vary'] = 'Accept-Encoding'
            response.headers['Content-Length'] = len(response.data)

            return response

        return f(*args, **kwargs)

    return view_func


def login_required(*args):

    if isinstance(args[0], types.FunctionType):
        return __login_required__(args[0])

    def decorator(func):
        def _f(*args, **kwargs):
            if request.method in args:
                return __login_required__(func)(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        _f.__name__ = func.__name__
        return _f

    return decorator
