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
    Wraps a function that returns a dict of dicts into a Flask JSON response with status
    :param func: function that should return at least {"json_data": dict_to_be_JSONed}
        Hopefully it also contains a "status" key(e.g. {"json_data: ..., "status": ...})
    :return:
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        returned_value = func(*args, **kwargs)
        if "json_data" in returned_value:
            payload = json.dumps(returned_value["json_data"])            
        else:
            print("Function for the status response does not return a proper value!")
            raise ValueError
        if "status" in returned_value:            
            return Response(
                payload, 
                status=returned_value["status"], 
                mimetype='application/json'
            )
        else:
            return Response(
                payload, 
                status=returned_value["status"], 
                mimetype='application/json'
            )

    return decorated_function