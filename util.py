from functools import wraps
from flask import jsonify, Response, json


def json_response(func):
    """
    Converts the returned dictionary into a JSON response
    :param func:
    :return:
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        return jsonify(func(*args, **kwargs))

    return decorated_function


def status_response(func):
    """
    Wraps a function (function which returns a dict of dicts) into a Flask response 
    of type JSON with provided status ("status" key in dict of dicts)

    :param func: function that should return at least {"json_data": dict_to_be_JSONed}
    Hopefully it also contains a "status" key (e.g. {"json_data": ..., "status": ...})

    :return:
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        returned_value = func(*args, **kwargs)
        if "json_data" in returned_value:
            actual_data = json.dumps(returned_value["json_data"])            
        else:
            print("Function for the status response does not return a proper value!")
            raise ValueError
        if "status" in returned_value:            
            return Response(
                actual_data, 
                status=returned_value["status"], 
                mimetype='application/json'
            )
        else:
            return Response(
                actual_data, 
                status=200, 
                mimetype='application/json'
            )

    return decorated_function


def construct_default_reply(func):
    """
    Wraps a function that returns a dictionary into something that works with status_response.     
    This exemplifies how the dict of dicts in status_response should be constructed (for building
    custom logic for HTTP status replies)
    (e.g. if you want a 200 HTTP response on a function that returns nothing, func must return 
    an empty dictionary!)
    
    :param func: func(request_object) - since func logic may depend on the actual request and
    the STATUS replies wrapped here also depend on the actual request, the way this is
    currently implemented is that you decorate a function that has at least a 'request_object'
    parameter and then you return the actual value of the decorated function for ARGUMENT
    the actual 'request' (the object that makes sense only inside a Flask app_route)

    :return: decorated function
    """
    @wraps(func)
    def decorated_function(request_object, *args, **kwargs):
        reply = {}
        if (
            ('Content-Type' in request_object.headers) and 
            (request_object.headers['Content-Type'] == 'application/json')
        ):
            return_value = func(request_object, *args, **kwargs)
            if type(return_value) == dict:
                reply["json_data"] = return_value
                return reply
            else:
                reply["json_data"] = {"STATUS_TEXT": "Mangled data"}
                reply["status"] = 400
                return reply
        else:
            reply["json_data"] = {"STATUS_TEXT": "Unsupported media type (expecting application/json)"}
            reply["status"] = 415
            return reply

    return decorated_function