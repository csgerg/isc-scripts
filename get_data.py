"""
=====
Database connection and data manipulation
=====
 
This example shows how you can easily connect to PG database
Use Psycopg2 to connect to the database http://initd.org/psycopg/docs/index.html
"""
# If you got error at te import line than please install the necessarily python module
# (pip install psycopg2 psycopg2-binary) https://docs.python.org/3/tutorial/venv.html
import psycopg2
 
 
def get_data_from_sql_auto(sql_query, sql_params=None):
    """Connect to the database and return with the data with AUTOMATIC transaction control"""
 
    # connection details
    db_connection = {
        'host': 'xxx.xxx.xxx.xxx',
        'host_test': 'xxx.xxx.xxx.xxx',
        'port': '5432',
        'db_name': 'dbname',
        'db_user': 'dbuser',
        'db_pass': 'dbpass'
    }
 
    # create connection more info: http://initd.org/psycopg/docs/module.html
    # you can create different way the connection string, in my case it is easy to change between the sql servers
    # (host, host_test)
    conn = psycopg2.connect(host=db_connection['host'],
                            port=db_connection['port'],
                            dbname=db_connection['db_name'],
                            user=db_connection['db_user'],
                            password=db_connection['db_pass'])
 
    # create connection https://docs.python.org/3/reference/compound_stmts.html#the-with-statement
    # http://initd.org/psycopg/docs/usage.html#with-statement
    with conn:
        # create cursor
        with conn.cursor() as cur:
            # execute cursor with sql
            # http://initd.org/psycopg/docs/cursor.html#cursor.execute
            cur.execute(sql_query, vars=sql_params)
            # fetch all results and put in a variable
            # http://initd.org/psycopg/docs/cursor.html#cursor.fetchone
            sql_result = cur.fetchall()
 
    # return with the results
    return sql_result
 
 
def convert_data(limit):
    """it is the docstring what describe the function and behavior of the function
    more info https://www.python.org/dev/peps/pep-0257/
 
    The function convert list of tuple to list of dictionaries"""
    # put your initial variables at tbe top of the file or function
    agency_list = list()
 
    # now i just putted the query inside the function to keep the things together (you can pass the sql as a parameter
    # how we did before in the tutorial)
 
    # our sql query
    query_with_kw_parameters = """
    SELECT id, code, country, status, last_data, web
    FROM tablename
    LIMIT %(limit)s
    """
 
    # use convert_data's limit parameter to pass the limit inside the function
    # create a variable and put the result in it
    # DRY: https://en.wikipedia.org/wiki/Don%27t_repeat_yourself
    # if you use multiple times your query result always put into a variable instead of executing sql multiple times
    # give a meaningful name of the variable nto 'e', 'k' etc.
    agency_data = get_data_from_sql_auto(query_with_kw_parameters, {'limit': limit})
 
    # loop and manipulate the data
    # Care about Big O notation https://medium.com/@cindychen13.work/a-beginners-guide-to-big-o-notation-793d654973d
    for item in agency_data:
        # create separate dictionaries for every item (agency) you can use list, tuples etc. what is fit for you
        # https://docs.python.org/3/tutorial/datastructures.html
        # append to the empty list all items separately (agency_list is a list())
        agency_list.append(
            {'id': item[0],  # every item is a tuple and it contains the query select elements
             'code': item[1],
             'country': item[2],
             'status': item[3],
             'url': item[5],  # you can change the keys if you like
             'last_data': item[4],  # you can change the order (the item indexing is important)
             }
        )
    else:
        # sometimes useful to do something at the last iteration
        # https://docs.python.org/3.6/tutorial/controlflow.html#break-and-continue-statements-and-else-clauses-on-loops
 
        # get the list length at the end of the iteration (it is just old school debugging purpose, delete the else:)
        print("!!!Debug information with print (agency_list length): {}".format(len(agency_data)))
 
    # return with the agency list
    return agency_list
