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