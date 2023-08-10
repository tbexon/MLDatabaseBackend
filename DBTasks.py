import sqlite3
import config as cfg


def initConnection(DBName):
    """
    Connects to specified SQL Database
    :param DBName: str
        Database Name
    :return: cursor object, connection object
    """
    print(DBName)
    try:
        connection = sqlite3.connect(DBName)
    except Exception as e:
        print(f"Error Occured: {e}")
        return False
    cursor = connection.cursor()
    return cursor, connection


def closeConnection(connection):
    """
    Closes a DB connection
    """
    connection.commit()
    connection.close()


def checkTableExists(cursor, table_name):
    """
    Checks if Table already exists
    :param cursor: cursor object
    :param table_name: str
        Table Name to look for
    :return: bool
    """
    # Checks if table already exists
    cursor.execute(f''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}' ''')
    if cursor.fetchone()[0] == 1:
        # If Table Already exists
        print(f"Table Already exists!")
        return True
    else:
        return False


def createTable(cursor, table_name, column_names, column_types_dict):
    """
    Creates Table, and adds columns
    :param cursor: class
        Cursor object for interacting with DB
    :param table_name: str
    name of table to create
    :param column_names: list
        List of Columns Names
    :param column_types_dict: dict
        Dict of column types
    :return:
    """

    # if checkTableExists(cursor, table_name):  # Checks if Table already exists
    #     # If Table Already exists
    #     print(f"Table Already exists!")
    #     return
    # else:
    # If Table does not already exist
    column = ''  # Blank string that will contain column names
    for eachColumnName in column_names:
        column += f'{eachColumnName} {column_types_dict[eachColumnName]},'
    print(f"CREATE TABLE {table_name} ({column[:-1]})")
    # Creates Table and inserts specified columns
    cursor.execute(f"CREATE TABLE {table_name} ({column[:-1]})")

def insertRows(cursor, table_name, column_names, values):
    """
    Inserts an interable list of value dicts into specified table
    :param cursor: cursor object
        for interacting with DB
    :param table_name: str
        Table Name to insert rows into
    :param column_names: list
        list of column names
    :param values: list
        list containing a dict for each row
    :return:
    """
    # print(f"Values Dict: {values}")
    column = ''
    for eachColumnName in column_names:
        column += f'{eachColumnName},'
    value_cols = [':' + eachColumnName for eachColumnName in column_names]
    print(f"INSERT INTO {table_name} ({column[:-1]}) VALUES ({turnListintoString(value_cols)[:-1]})")
    cursor.executemany(f"INSERT INTO {table_name} ({column[:-1]}) VALUES ({turnListintoString(value_cols)[:-1]})",values)
    print(cursor.execute("SELECT * from Fixtures").fetchall())


def InsertFixRow(cursor, table_name, column_names, values):
    cols = f"{cfg.fixture_name_fld},{cfg.manf_ID_fld}, {cfg.wattage_fld},{cfg.weight_fld},{cfg.userID_fld}"
    sql = f"INSERT INTO {table_name} ({cols} ) VALUES (?,?,?,?,?)"
    for eachRow in values:
        try:
            data = (eachRow[cfg.fixture_name_fld],eachRow[cfg.manf_ID_fld],eachRow[cfg.wattage_fld],
                    eachRow[cfg.weight_fld], eachRow[cfg.userID_fld])
            print(data)
            cursor.execute(sql,data)  # Inserts rows into DB
        except Exception as e:
            print("Error!")
            print(e)

def InsertMafRow(cursor, table_name, column_names, values):
    cols = f"{cfg.manf_ID_fld},{cfg.manufacturer_fld}, {cfg.userID_fld}"
    sql = f"INSERT INTO {table_name} ({cols} ) VALUES (?,?,?)"
    for eachRow in values:
        try:
            data = (eachRow[cfg.manf_ID_fld],eachRow[cfg.manufacturer_fld],eachRow[cfg.userID_fld])
            print(data)
            cursor.execute(sql,data)  # Inserts rows into DB
        except Exception as e:
            print("Error inserting into Manufacturers Table!")
            print(e)


def InsertUserRow(cursor, table_name, column_names, values):
    cols = f"{cfg.userID_fld},{cfg.username_fld}, {cfg.email_fld}, {cfg.password_fld}, {cfg.admin_fld}, {cfg.edit_fld}, " \
           f" {cfg.add_fld},{cfg.view_fld},{cfg.manufacturer_grp_fld},{cfg.moderate_grp_fld}"
    sql = f"INSERT INTO {table_name} ({cols} ) VALUES (?,?,?,?,?,?,?,?,?,?)"
    for eachRow in values:
        try:
            data = (eachRow[cfg.userID_fld],eachRow[cfg.username_fld],eachRow[cfg.email_fld],eachRow[cfg.password_fld]
                    ,eachRow[cfg.admin_fld],eachRow[cfg.edit_fld],eachRow[cfg.add_fld],eachRow[cfg.view_fld],
                    eachRow[cfg.manufacturer_grp_fld],eachRow[cfg.moderate_grp_fld])
            print(data)
            cursor.execute(sql,data)  # Inserts rows into DB
        except Exception as e:
            print("Error!")
            print(e)


def InsertDMXProfRow(cursor, table_name, column_names, values):
    cols = f"{cfg.DMXprofID_fld},{cfg.fixture_ID_fld}, {cfg.prof_name}, {cfg.dmxcnt_fld}, {cfg.userID_fld}"
    sql = f"INSERT INTO {table_name} ({cols} ) VALUES (?,?,?,?,?)"
    for eachRow in values:
        try:
            data = (eachRow[cfg.DMXprofID_fld],eachRow[cfg.fixture_ID_fld],eachRow[cfg.prof_name],eachRow[cfg.dmxcnt_fld]
                    ,eachRow[cfg.userID_fld])
            print(data)
            cursor.execute(sql,data)  # Inserts rows into DB
        except Exception as e:
            print("Error!")
            print(e)


def turnListintoString(list_to_convert, **kwargs):
    """
    Converts list into string with comma separator
    :param list_to_convert: list
        list of string values to combine into string
    :return: str
        String output
    """
    stringtooutput = ''
    if 'separator' in kwargs:
        separator = kwargs['separator']
    else:
        separator = ','
    for eachString in list_to_convert:
        stringtooutput += f'{eachString}{separator}'
    return stringtooutput


def CreateMLDB(cursor,connection):
    col_names = [cfg.fixture_ID_fld,
                 cfg.fixture_name_fld,
                 cfg.manf_ID_fld,
                 cfg.wattage_fld,
                 cfg.weight_fld,
                 cfg.userID_fld,
                 cfg.conn_in_fld,
                 cfg.conn_out_fld,
                 cfg.reputation_fld
                 ]

    col_types = {cfg.fixture_ID_fld: 'INTEGER PRIMARY KEY',
                 cfg.fixture_name_fld: 'TEXT',
                 cfg.manf_ID_fld: 'INTEGER',
                 cfg.wattage_fld: 'REAL',
                 cfg.weight_fld: 'REAL',
                 cfg.userID_fld: 'INTEGER',
                 cfg.conn_in_fld: 'TEXT',
                 cfg.conn_out_fld: 'TEXT',
                 cfg.reputation_fld: 'INTEGER'}

    values = [{ cfg.fixture_name_fld: 'Mac Viper Performance',
                cfg.manf_ID_fld: '1',
                cfg.wattage_fld: '1225',
                cfg.weight_fld: '32.2',
                 cfg.userID_fld: '1'
               },
              {
                cfg.fixture_name_fld: 'Perseo',
                cfg.manf_ID_fld: '2',
                cfg.wattage_fld: '800',
                cfg.weight_fld: '32.2',
                cfg.userID_fld: '1'
               }]
    createTable(cursor,cfg.FIXTURE_TBL_NAME,col_names,col_types)
    InsertFixRow(cursor, cfg.FIXTURE_TBL_NAME, col_names, values)


def CreateManfDB(cursor,connection):

    col_names = [cfg.manf_ID_fld,
                 cfg.manufacturer_fld,
                 cfg.userID_fld
                 ]

    col_types = {cfg.manf_ID_fld : 'INTEGER PRIMARY KEY' ,
                 cfg.manufacturer_fld: 'Text',
                 cfg.userID_fld: 'INTEGER'
                 }

    values = [{cfg.manf_ID_fld: '1',
               cfg.manufacturer_fld: 'Martin',
               cfg.userID_fld: '1'
               },
              {
                  cfg.manf_ID_fld: '2',
                  cfg.manufacturer_fld: 'Ayrton',
                  cfg.userID_fld: '1'
              }]
    createTable(cursor, cfg.MANUFACTURER_TBL_NAME, col_names, col_types)
    InsertMafRow(cursor, cfg.MANUFACTURER_TBL_NAME, col_names, values)


def CreateUserDB(cursor,connection):

    # Sets the Column Names
    col_names = [cfg.userID_fld,
                 cfg.username_fld,
                 cfg.email_fld,
                 cfg.password_fld,
                 cfg.admin_fld,
                 cfg.add_fld,
                 cfg.edit_fld,
                 cfg.view_fld,
                 cfg.manufacturer_grp_fld,
                 cfg.moderate_grp_fld]
    # Sets the Column Types
    col_types = {cfg.userID_fld: 'INTEGER PRIMARY KEY',
                 cfg.username_fld: 'TEXT',
                 cfg.email_fld: 'TEXT',
                 cfg.password_fld: 'TEXT',
                 cfg.admin_fld: 'BOOLEAN',
                 cfg.add_fld: 'BOOLEAN',
                 cfg.edit_fld: 'BOOLEAN',
                 cfg.view_fld: 'BOOLEAN',
                 cfg.manufacturer_grp_fld: 'BOOLEAN',
                 cfg.moderate_grp_fld: 'BOOLEAN'
                 }
    values = [{cfg.userID_fld: '1',
               cfg.username_fld: 'Auto_import',
               cfg.email_fld:'tom@tb-lx.com',
               cfg.password_fld:'Test',
               cfg.admin_fld:'1',
               cfg.edit_fld: '1',
               cfg.add_fld: '1',
               cfg.view_fld: '1',
               cfg.manufacturer_grp_fld: '1',
               cfg.moderate_grp_fld: '1'
               }]
    createTable(cursor,cfg.USERS_TBL_NAME,col_names,col_types)
    InsertUserRow(cursor, cfg.USERS_TBL_NAME, col_names, values)

if __name__ == '__main__':
    cursor, connection = initConnection(cfg.DBFILEPATH)
    CreateMLDB(cursor,connection)
    CreateUserDB(cursor,connection)
    CreateManfDB(cursor,connection)
    cursor.close()
    connection.commit()  # Commits Changes
    connection.close()