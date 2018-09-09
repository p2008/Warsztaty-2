from psycopg2 import connect, OperationalError, ProgrammingError
import time


def create_connection(db_name: str) -> connect:
    """ Create connection do database of db_name"""
    username = "postgres"
    passwd = "coderslab"
    hostname = "127.0.0.1"  # lub "localhost"

    cnx = None
    try:
        # tworzymy nowe połączenie
        cnx = connect(user=username, password=passwd,
                      host=hostname, database=db_name)
        cnx.autocommit = True
        print("Connection successful.")
    except OperationalError as error:
        cnx = None
        print(error)
        print("Connection unsuccessful.")

    return cnx


def execute_sql(cnx: connect, sql: str, values: tuple) -> list:
    """Pass sql query"""
    start = time.time()
    cursor = cnx.cursor()

    if '.sql' in sql:
        file = open(sql, 'r')
        sql = file.read()
        file.close()

    result = []
    sql_command = sql.split(';')
    try:
        for sql in sql_command:
            if sql == '' or '--' in sql:
                continue
            try:
                cursor.execute(sql, values)

                if 'SELECT' in sql:
                    column_names = tuple(desc[0] for desc in cursor.description)
                    result.append({"query": sql, 'column_names': column_names, "data": cursor.fetchall()})
                elif 'DELETE' in sql:
                    stop = time.time() - start
                    result.append({"query": sql, "data": 'query executed in {:06.3f}s. {} rows affected'.format(stop, cursor.rowcount)})
                else:
                    stop = time.time() - start
                    result.append({"query": sql, "data": 'query executed in {:06.3f}s'.format(stop)})
            except ProgrammingError as error:
                print(error)
                print("query unsuccessful: {}".format(sql))
                result.append({"query": sql, "data": 'query unsuccessful: {}'.format(error)})
    finally:
            cursor.close()
            cnx.close()

    return result