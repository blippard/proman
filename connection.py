import psycopg2  # you know what this is!
from psycopg2 import sql  # allows us to build up SQL compositions of identifier/literals
#                         # needed for security reasons (protect against SQL injection)

from psycopg2.extras import RealDictCursor  # import the type RealDictCursor
from connection_wrapper import connection_handler   # basically a submodule of connection; 
#                                                   # since the wrapper is long we separate it from the SQL queries


# This is a way to get the DB table headers as the variable 'column_names_dict'
# ... doing it this way is longer in lines of code but prevents the need to update this constant 
# (column_names_dict is a dictionary of lists, with key the tablenames, each list being the column names/headers) 
# when we insert new columns in tables (this still needs to be updated when adding new tables)
@connection_handler
def get_column_names_from_table(cursor: RealDictCursor, table_name):
    query = sql.SQL("""
        SELECT * FROM {sql_table_name}
    """).format(sql_table_name=sql.Identifier(table_name))
    cursor.execute(query)
    simple_dict = cursor.fetchone()
    column_names = [key for key in simple_dict]
    return column_names


column_names_dict = {}
for table_name in ['board', 'card', 'status', 'board_to_status', 'user']:
    column_names_dict.update({ table_name : get_column_names_from_table(table_name) })
# ...... END getting DB table headers/column names ..........................


# CREATE functions


@connection_handler
def append_row_in_table(cursor: RealDictCursor, some_dict: dict, table_name):
    table_fields = column_names_dict[table_name]
    intersection_fields = [field for field in table_fields if field in some_dict]    
    value_list = [some_dict[field] for field in intersection_fields]

    joined_value_list = tuple(n for n in value_list) 
    joined_sql_column_names = sql.SQL(', ').join( sql.Identifier(n) for n in intersection_fields )

    query = sql.SQL('''INSERT INTO {sql_table_name} ({column_names})
            VALUES %(list_of_values)s''').format(
                column_names=joined_sql_column_names, 
                sql_table_name=sql.Identifier(table_name)
            )
    cursor.execute(query, {"list_of_values": joined_value_list})


# READ functions


@connection_handler
def get_data_from_table(cursor: RealDictCursor, table_name):
    query = sql.SQL('''
        SELECT * FROM {sql_table_name}
    ''').format(sql_table_name=sql.Identifier(table_name))
    cursor.execute(query)
    result_rows = cursor.fetchall()
    
    return result_rows


@connection_handler
def variable_get_by_kw_value_pair_from_table(cursor: RealDictCursor, pair_dict, table_name, nresults=-1000):
    column_name = [key for key in pair_dict][0]
    column_value = pair_dict[column_name]
    query = sql.SQL("""
        SELECT * FROM {sql_table_name} 
        WHERE {sql_column_name} = %(column_val)s
    """).format(
        sql_table_name=sql.Identifier(table_name),
        sql_column_name=sql.Identifier(column_name)
        )
    cursor.execute(query, {"column_val": column_value})
    if nresults == -1000:
        result = cursor.fetchall()
    elif nresults == 1:
        result = cursor.fetchone()
    elif nresults > 1:
        result = cursor.fetchmany(nresults)
    else:
        result = None
    return result


def get_data_by_kw_value_pair_from_table(pair_dict, table_name):    
    return variable_get_by_kw_value_pair_from_table(pair_dict, table_name, nresults=-1000)


def get_single_row_by_kw_value_pair_from_table(pair_dict, table_name):
    return variable_get_by_kw_value_pair_from_table(pair_dict, table_name, nresults=1)


@connection_handler
def get_sorted_inner_join_where_table2_column_has_value_and_order_by_table1_column(
    cursor: RealDictCursor,
    table1_name,
    table2_name,    
    table2_column,
    table2_column_value,
    table1_keycol,
    table2_keycol,    
    table1_column_to_order,
    reverse=False
):
    list1 = [table1_name, table1_keycol]
    list2 = [table2_name, table2_keycol]    
    list3 = [table1_name, table1_column_to_order]
    keystring_t1 = sql.SQL('.').join(sql.Identifier(n) for n in list1)
    keystring_t2 = sql.SQL('.').join(sql.Identifier(n) for n in list2)
    column_string_t1 = sql.SQL('.').join(sql.Identifier(n) for n in list3)
    if reverse:
        query = sql.SQL("""
            SELECT {sql_table1_name}.* FROM {sql_table1_name} INNER JOIN {sql_table2_name}
                ON {sql_keystring_t1} = {sql_keystring_t2}
            WHERE {sql_table2_name}.{sql_table2_column} = %(table2_value)s
            ORDER BY {sql_column_string_t1} DESC
        """).format(
            sql_table1_name=sql.Identifier(table1_name),
            sql_table2_name=sql.Identifier(table2_name),
            sql_keystring_t1=keystring_t1,
            sql_keystring_t2=keystring_t2,
            sql_table2_column=sql.Identifier(table2_column),
            sql_column_string_t1=column_string_t1
            )
    else:
        query = sql.SQL("""
            SELECT {sql_table1_name}.* FROM {sql_table1_name} INNER JOIN {sql_table2_name}
                ON {sql_keystring_t1} = {sql_keystring_t2}
            WHERE {sql_table2_column} = %(table2_value)s
            ORDER BY {sql_column_string_t1} ASC
        """).format(
            sql_table1_name=sql.Identifier(table1_name),
            sql_table2_name=sql.Identifier(table2_name),
            sql_keystring_t1=keystring_t1,
            sql_keystring_t2=keystring_t2,
            sql_table2_column=sql.Identifier(table2_column),
            sql_column_string_t1=column_string_t1
            )
    cursor.execute(query, {"table2_value": table2_column_value})
    result_rows = cursor.fetchall()

    return result_rows


@connection_handler
def get_max_serial_from_table(cursor: RealDictCursor, table_name):
    query = sql.SQL("""
        SELECT max({sql_id}) FROM {sql_table_name}
    """).format(
        sql_id=sql.Identifier('id'),
        sql_table_name=sql.Identifier(table_name)
        )
    cursor.execute(query)
    result_dict = cursor.fetchone()
    try:
        max_serial = int(result_dict['max'])
    except (TypeError, ValueError):
        raise
    return max_serial


# UPDATE functions


@connection_handler
def update_data_in_table(cursor: RealDictCursor, some_dict: dict, table_name, id_val=None):
    table_fields = column_names_dict[table_name]
    intersection_fields = [field for field in table_fields if field in some_dict]
    value_list = [some_dict[field] for field in intersection_fields]
    
    joined_value_list = tuple(n for n in value_list)
    joined_sql_column_names = sql.SQL(', ').join( sql.Identifier(n) for n in intersection_fields )

    if id_val is None: 
        id_value = some_dict['id']
    else:
        id_value = id_val

    query = sql.SQL('''UPDATE {sql_table_name}
    SET ({column_names}) = %(list_of_values)s
    WHERE {id} = %(id_value)s
    ''').format(
        column_names=joined_sql_column_names, 
        id=sql.Identifier('id'),
        sql_table_name=sql.Identifier(table_name)
        )

    cursor.execute(query, {'list_of_values': joined_value_list, 'id_value': id_value})


# DELETE functions


@connection_handler
def delete_row_with_id(cursor: RealDictCursor, id_val, table_name):
    query = sql.SQL('''DELETE FROM {sql_table_name}
    WHERE {id} = %(id_value)s
    ''').format(id=sql.Identifier('id'),
                sql_table_name=sql.Identifier(table_name))
    cursor.execute(query, {'id_value': id_val})