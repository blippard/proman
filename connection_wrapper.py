# the connection between database and our server
import os
import psycopg2
import urllib

def get_local_connection_string():
    # setup connection string
    # to do this, please define these environment variables first
    user_name = os.environ.get('PSQL_USER_NAME')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    database_name = os.environ.get('PSQL_DB_NAME')
    port = 5432  # default PostgreSQL port

    env_variables_defined = user_name and password and host and database_name

    if env_variables_defined:
        # this string describes all info for psycopg2 to connect to the database
        return 'postgresql://{user_name}:{password}@{host}:{port}/{database_name}'.format(
            user_name=user_name,
            password=password,
            host=host,
            database_name=database_name,
            port=port
        )
    else:
        raise KeyError('Some necessary environment variable(s) are not defined')




def open_database():    
    
    # code for Heroku. 

    # urllib.parse.uses_netloc.append('postgres')     # uses the postgres syntax for the URI, namely: 
    # #                                               # postgres://username:password@host:port/path/to/resource/on/host
    # try:
    #     url = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))
    # except (TypeError, ValueError):        
    #     raise KeyError('Could not find required environment variables!')

    
    # try:        
    #     connection = psycopg2.connect(
    #         database=url.path[1:],  # skip the leading / in the 'path'
    #         user=url.username,  # use the rest of the parsed variables from the URI
    #         password=url.password,
    #         host=url.hostname,
    #         port=url.port
    #     )
    #     connection.autocommit = True    # leave True for now, maybe change later if needed
    # except psycopg2.DatabaseError as exception:
    #     print('Database connection problem')
    #     raise exception

    try:
        connection_string = get_local_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True    # leave True for now, maybe change later if needed
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception

    return connection


def connection_handler(function):

    # (*args and **kwargs are the convention, but this is for clarity)
    # *unspecified_args can be passed as a tuple
    # **unspecified_keyworded_args can be passed as a dictionary
    def wrapper(*unspecified_args, **unspecified_keyworded_args):
        

        connection = open_database()

        # we set the cursor_factory parameter to return with 
        # a RealDictCursor cursor (cursor which provides dictionaries)
        dict_cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        
        # The actual function to be wrapped ( named function() ) is used now:
        # any wrapped function() will be expected to have a (formal) argument representing a cursor
        # and which is of the RealDictCursor type (the rest are wildcards/unspecified)
        ret_value = function(dict_cursor, *unspecified_args, **unspecified_keyworded_args)

        
        dict_cursor.close()
        connection.close()
        

        return ret_value

    return wrapper  # wrapper is a function (all decorators should map functions to functions)
    #               # ...but it is a function which returns ret_value