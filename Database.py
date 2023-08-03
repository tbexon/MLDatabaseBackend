import sqlite3
import config as cfg


def initConnection(DBFIlEPATH):
    """
    Connects to specified SQL Database
    :param DBFIlEPATH: str
        Database FilePath
    :return: cursor object, connection object
    """
    try:
        connection = sqlite3.connect(DBFIlEPATH)
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


def InsertSingleRow(cursor, table_name, column_names, values):
    """
    Inserts a new row into specified Table
    :param cursor: object
         SQL Cursor object
    :param table_name: str
        Name of table to insert row into
    :param column_names: list
        List of Column names for said table
    :param values: dict
        Dict of fixture values
    :return:
    """
    cols = ""
    final_value_string = ""
    for eachCol in column_names:
        # Adds each Column name along with a comma separator to overall column names list
        cols += eachCol+","
        # Gets the relavant columns value and adds to final value string
        final_value_string += values[eachCol]+","

    # cols = f"{cfg.fixture_name_fld},{cfg.manf_ID_fld}, {cfg.wattage_fld},{cfg.weight_fld},{cfg.userID_fld}"
    # Cols[:-1] & final_value_string[:-1] removes the last comma from both strings to stop any errors
    sql = f"INSERT INTO {table_name} ({cols[:-1]} ) VALUES ({final_value_string})"

    try:
        # data = (eachRow[cfg.fixture_name_fld],eachRow[cfg.manf_ID_fld],eachRow[cfg.wattage_fld],
        #         eachRow[cfg.weight_fld], eachRow[cfg.userID_fld])
        print(sql)
        cursor.execute(sql)  # Inserts rows into DB
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
            print("Error!")
            print(e)


def InsertUserRow(cursor, table_name, column_names, values):
    cols = f"{cfg.userID_fld},{cfg.username_fld}, {cfg.email_fld}, {cfg.password_fld}, {cfg.admin_fld}, {cfg.edit_fld}, " \
           f" {cfg.add_fld},{cfg.view_fld},{cfg.manufacturer_grp_fld}"
    sql = f"INSERT INTO {table_name} ({cols} ) VALUES (?,?,?,?,?,?,?,?,?)"
    for eachRow in values:
        try:
            data = (eachRow[cfg.userID_fld],eachRow[cfg.username_fld],eachRow[cfg.email_fld],eachRow[cfg.password_fld]
                    ,eachRow[cfg.admin_fld],eachRow[cfg.edit_fld],eachRow[cfg.add_fld],eachRow[cfg.view_fld],eachRow[cfg.manufacturer_grp_fld])
            print(data)
            cursor.execute(sql,data)  # Inserts rows into DB
        except Exception as e:
            print("Error!")
            print(e)

def GetRowByID(cursor,ID,table_name,ID_col_name):
    sql = f"SELECT * FROM {table_name} WHERE {ID_col_name} = {ID}"
    cursor.execute(sql)  # Querys DB
    output = cursor.fetchall()  # Gets results of query
    return output

def InsertFixtureIntoDB(fixture_val_dict):
    """
    Inserts a new fixture into Fixture Table
    :param fixture_val_dict: dict
        Dict of Fixture Values
    :return:
    """
    try:
        cursor,connection = initConnection(cfg.DBFILEPATH)  # Opens Connection to DB
    except Exception as e:
        print(f"Failed to initialise DB Connection!")
        print(f"Error Message: {e}")
    try:
        # Inserts row into Fixture Table
        InsertSingleRow(cursor,cfg.FIXTURE_TBL_NAME,cfg.fixture_col_names,fixture_val_dict)
    except:
        print(f"Failed to insert row into DB!")
        print(f"Error Message: {e}")
    closeConnection(connection)  # Commits Changes and closes connection


def GetManufacturerByID(Manf_ID):
    """
    Gets a specific Manufacturers row from DB based on Manufacturers ID
    :param Manf_ID: int
        Manufacturers Unique ID
    :return: dict
        Returns a dict containing Manufacturers info
    """
    try:
        cursor,connection = initConnection(cfg.DBFILEPATH)  # Opens Connection to DB
    except Exception as e:
        print(f"Failed to initialise DB Connection!")
        print(f"Error Message: {e}")
    # Get Manufacturers data as Tuple
    manf_data = GetRowByID(cursor,Manf_ID,cfg.MANUFACTURER_TBL_NAME,cfg.manf_ID_fld)
    final_data = {}  # Dict containing the final data to be returned
    ind = 0
    for eachCol in cfg.manf_col_names:
        # Convert raw Tuple data into a Dict where each Column name is the key
        final_data.update({eachCol:manf_data[0][ind]})
        ind += 1
    return final_data

def GetUserByID(User_ID):
    """
    Gets a specific User's row from DB based on User ID
    :param User_ID: int
        User's Unique ID
    :return: dict
        Returns a dict containing Users info
    """
    try:
        cursor,connection = initConnection(cfg.DBFILEPATH)  # Opens Connection to DB
    except Exception as e:
        print(f"Failed to initialise DB Connection!")
        print(f"Error Message: {e}")
    # Get User's data as Tuple
    data = GetRowByID(cursor,User_ID,cfg.USERS_TBL_NAME,cfg.userID_fld)
    final_data = {}  # Dict containing the final data to be returned
    ind = 0
    for eachCol in cfg.user_col_names:
        # Convert raw Tuple data into a Dict where each Column name is the key
        final_data.update({eachCol:data[0][ind]})
        ind += 1
    return final_data


def GetFixtureByID(Fix_ID):
    """
    Gets a specific Fixture's row from DB based on Fixture ID.
    Gets the Manufacturers name as a string from Manufacturers Table
    :param Fix_ID: int
        Fixtures Unique ID
    :return: dict
        Returns a dict containing Fixture's info
    """
    try:
        cursor,connection = initConnection(cfg.DBFILEPATH)  # Opens Connection to DB
    except Exception as e:
        print(f"Failed to initialise DB Connection!")
        print(f"Error Message: {e}")
    # Get specific Fixture Data as Tuple based on Fixture ID
    fixture_data = GetRowByID(cursor,Fix_ID,cfg.FIXTURE_TBL_NAME,cfg.fixture_ID_fld)

    final_data = {}  # Dict containing the final data to be returned
    ind = 0
    if not fixture_data:
        # If Fixture Data is empty, returns blank dictionary
        return final_data
    for eachCol in cfg.fixture_col_names:
        # Convert raw Tuple data into a Dict where each Column name is the key
        final_data.update({eachCol:fixture_data[0][ind]})
        ind += 1

    manufacturer_data = GetManufacturerByID(final_data[cfg.manf_ID_fld])  # Gets the Manufacturers name
    final_data.update({cfg.manufacturer_fld:manufacturer_data[cfg.manufacturer_fld]})  # Adds Manufacturers name to fixture data

    user_data = GetUserByID(final_data[cfg.userID_fld])
    final_data.update({cfg.username_fld:user_data[cfg.username_fld]})
    return final_data

if __name__ == '__main__':
    fix_data = GetFixtureByID(1)
    print(fix_data)