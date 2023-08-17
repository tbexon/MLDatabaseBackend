import sqlite3
import config as cfg
import os


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


def GetRowByID(cursor,ID,table_name,ID_col_name):
    sql = f"SELECT * FROM {table_name} WHERE {ID_col_name} = {ID}"
    cursor.execute(sql)  # Querys DB
    output = cursor.fetchall()  # Gets results of query
    return output

def GetRowByString(cursor,ID,table_name,ID_col_name):
    sql = f"SELECT * FROM {table_name} WHERE {ID_col_name} = '{ID}'"
    cursor.execute(sql)  # Querys DB
    output = cursor.fetchall()  # Gets results of query
    return output

def GetAllRows(cursor,table_name):
    """
    Gets all rows in specified table
    :param cursor: obj
        Cursor object for interacting with SQL
    :param table_name: str
        Name of Table to get data from
    :return: tuple
    """
    sql = f"SELECT * FROM {table_name}"
    cursor.execute(sql)  # Querys DB
    output = cursor.fetchall()  # Gets results of query
    return output


def ConvertFixtureTupleToFixtureDict(data):
    """
    Converts the raw Fixture Data from Fixture table into the final data.
    Gets Manufacturer name from Manufacturers table, and user name from Users table.
    :param data: tuple
    :return:
    """
    final_data = []

    for eachRow in data:
        # For Each Row in Fixture Table
        cur_row_data = {}  # Dict to store current rows data in
        ind = 0
        for eachCol in cfg.fixture_col_names:
            # For Each Column within Fixture Table
            try:
                # Convert raw Tuple data into a Dict where each Column name is the key
                cur_row_data.update({eachCol: eachRow[ind]})
                ind += 1
            except:
                print(f"Failed to add {eachCol} to Dict!")
                continue

        fix_img_path = GetFixtureImgURL(cur_row_data[cfg.fixture_ID_fld])  # Converts fixture ID to complete path of image
        cur_row_data.update({cfg.img_name_fld: fix_img_path})  # Updates Image path in final data

        # Gets the manufacturers string name from the ID
        manufacturer_data = GetManufacturerByID(cur_row_data[cfg.manf_ID_fld])  # Gets the Manufacturers name
        cur_row_data.update(  # Adds to current Row
            {cfg.manufacturer_fld: manufacturer_data[cfg.manufacturer_fld]})  # Adds Manufacturers name to fixture data

        # Gets the Username string name from the ID
        user_data = GetUserByID(cur_row_data[cfg.userID_fld])
        cur_row_data.update({cfg.username_fld: user_data[cfg.username_fld]})

        # Adds the completed Row to final Data Dict
        # final_data.update({cur_row_data[cfg.fixture_ID_fld] :cur_row_data})
        final_data.append(cur_row_data)
    return final_data

def ConvertManufacturerTupleToManfDict(manf_data):
    """
    Converts a tuple of the manufacturers data into a dict
    :param manf_data: list
    list where each row is a tuple with the manf data in it
    :return: dict
    """
    final_data = []  # Dict containing the final data to be returned
    ind = 0
    for eachRow in manf_data:
        # For Each Row in Manf Table
        cur_row_data = {}  # Dict to store current rows data in
        ind = 0
        for eachCol in cfg.manf_col_names:
            if eachCol == cfg.manufacturer_fld:
                final_data.append(eachRow[ind])
            # # Convert raw Tuple data into a Dict where each Column name is the key
            # cur_row_data.update({eachCol:eachRow[ind]})
            ind += 1
        # final_data.append(cur_row_data)
    return final_data


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


def GetManufacturerIDFromName(Manf_string,cursor):
    """
    Gets the Manufacturers ID based off the manufacturers name
    :param Manf_string: str
    :param cursor: cursor object
    :return: string
    """
    manf_data = GetRowByString(cursor,Manf_string,cfg.MANUFACTURER_TBL_NAME,cfg.manufacturer_fld)
    if manf_data:
        manf_id = manf_data[0][0]
    else:
        manf_id = None
    return manf_id

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

    fix_img_path = GetFixtureImgURL(final_data[cfg.fixture_ID_fld])  # Converts fixture ID to complete path of image
    final_data.update({cfg.img_name_fld:fix_img_path})  # Updates Image path in final data

    manufacturer_data = GetManufacturerByID(final_data[cfg.manf_ID_fld])  # Gets the Manufacturers name
    final_data.update({cfg.manufacturer_fld:manufacturer_data[cfg.manufacturer_fld]})  # Adds Manufacturers name to fixture data

    user_data = GetUserByID(final_data[cfg.userID_fld])
    final_data.update({cfg.username_fld:user_data[cfg.username_fld]})
    return final_data

def GetFixtureImgURL(fix_id):
    """
    Checks if there is an image file associated with specific fixture ID, and returns the full path to said image
    if no fixture image returns path to stock image
    :param fix_id: str
    :return: str
    """
    final_path = ''
    final_path = os.path.join("http://127.0.0.1:5000/", cfg.fix_img_API_Dir, f"{fix_id}")
    # img_FilePath = os.path.join(os.getcwd(),cfg.fixture_img_FilePath)
    # test_FP = os.path.join(img_FilePath,f"{fix_id}.png")
    # if os.path.isfile(test_FP) is True:
    #     final_path = os.path.join("http://127.0.0.1:5000/",cfg.fix_img_API_Dir,f"{fix_id}")
    #     #print(f"Specific Fixture image specified updating to {final_path}")
    #
    # else:
    #     final_path = os.path.join("http://127.0.0.1:5000/",cfg.fix_img_API_Dir,cfg.stock_image_FileName)
    #    # print(f"No Fixture image found updating to {final_path}")


    return final_path


def GetAllFixtures(**kwargs):
    """
    Gets all rows in the Fixture Table
    :return: list
        Dict where each row is a dict of a fixtures values
    """
    if 'manf' in kwargs:
        manf_string = kwargs['manf']
    else:
        manf_string = ""
    try:
        cursor,connection = initConnection(cfg.DBFILEPATH)  # Opens Connection to DB
    except Exception as e:
        print(f"Failed to initialise DB Connection!")
        print(f"Error Message: {e}")
    if manf_string != "":
        manf_id = GetManufacturerIDFromName(manf_string,cursor)  # Gets the manufacturer ID
        fixture_data = GetRowByString(cursor,manf_id,cfg.FIXTURE_TBL_NAME,cfg.manf_ID_fld)
    else:
        fixture_data = GetAllRows(cursor,cfg.FIXTURE_TBL_NAME)  # Gets all rows in Fixture Table

    # Converts Raw Tuple to Dict, and adds Manufacturer and USerID
    final_data = ConvertFixtureTupleToFixtureDict(fixture_data)

    return final_data

def GetAllManufacturers():
    """
    Gets all rows in the Manufacturers Table
    :return: list
        Dict where each row is a dict of a fixtures values
    """
    try:
        cursor,connection = initConnection(cfg.DBFILEPATH)  # Opens Connection to DB
    except Exception as e:
        print(f"Failed to initialise DB Connection!")
        print(f"Error Message: {e}")
    manf_data = GetAllRows(cursor,cfg.MANUFACTURER_TBL_NAME)  # Gets all rows in Manufacturer Table

    final_data = ConvertManufacturerTupleToManfDict(manf_data)  # Converts Data into useable data


    return final_data

def GetFixFromSearchString(search_string,**kwargs):
    if 'manf' in kwargs:
        manf_string = kwargs['manf']
    else:
        manf_string = ""
    try:
        cursor,connection = initConnection(cfg.DBFILEPATH)  # Opens Connection to DB
    except Exception as e:
        print(f"Failed to initialise DB Connection!")
        print(f"Error Message: {e}")
    if manf_string != "":
        manf_id = GetManufacturerIDFromName(manf_string,cursor)  # Gets the manufacturer ID
        print(f"manf_id: {manf_id}")
        sql = f"SELECT * FROM 'Fixtures' WHERE InstType LIKE \"%{search_string}%\" AND {cfg.manf_ID_fld} = {manf_id};"
        print(sql)
    else:
        sql = f"SELECT * FROM 'Fixtures' WHERE InstType LIKE \"%{search_string}%\";"
    cursor.execute(sql)

    output = cursor.fetchall()

    # Converts Raw Tuple to Dict, and adds Manufacturer and UserID
    final_data = ConvertFixtureTupleToFixtureDict(output)

    return final_data


def InsertRowIntoTable(cursor, table_name, Data_dict):
    """
    Inserts the a new row into the table. The Data_dict keys will be used as column names
    :param cursor: obj
    :param table_name: str
        Name of Table to insert Data into
    :param Data_dict: dict
        Dict containing data to insert into table
    :return:
    """

    columns = ', '.join(Data_dict.keys())
    val_names = [':' + Col_name for Col_name in Data_dict.keys()]
    placeholders = ', '.join(val_names)
    sql = f"INSERT INTO {table_name} ({columns} ) VALUES ({placeholders});"
    try:
        cursor.execute(sql, Data_dict)  # Inserts rows into DB
    except Exception as e:
        print("Error Inserting Row Into DB!")
        print(e)


def CheckManfExists(manf_name, cursor):
    """
    Checks if there is currently a manufacturer in the database with the specified string name, and attempts to return
    the manf_id
    :param manf_name:
    :param cursor:
    :return: bool, int
        Returns True if Manufacturer already exists along with the ID
    """

    try:
        Manf_ID = GetManufacturerIDFromName(manf_name, cursor)
    except Exception as e:
        print(f"Error Getting Manf ID from String, Setting Manf ID to None")
        print(f"Error: {e}")
        Manf_ID = None
    if Manf_ID is None:
        return False,None
    else:
        return True, Manf_ID


def AddNewManufacturer(Manf_name, cursor, **kwargs):
    """
    Adds a new manufacturer to the Manf Table
    If no user ID has been specified it will default to 1 (Auto Import User)
    :param Manf_name: str
        name of Manufacturer
    :param cursor: obj
        sqllite cursor object
    :param kwargs: UserID
    :return: int
        returns new Manf_ID
    """

    manf_dict = {cfg.manufacturer_fld:Manf_name}
    if cfg.userID_fld in kwargs:
        # If a user ID for the manufacturer has been specified
        manf_dict.update({cfg.userID_fld: kwargs[cfg.userID_fld]})
    else:
        manf_dict.update({cfg.userID_fld: 1})
    try:
        InsertRowIntoTable(cursor,cfg.MANUFACTURER_TBL_NAME,manf_dict)  # Inserts the new Manufacturer into DB
    except:
        print(f"Error Inserting New Manufacturer!")
    cursor.execute(f"Select * FROM {cfg.MANUFACTURER_TBL_NAME}")
    manf_exists, Manf_id = CheckManfExists(manf_dict[cfg.manufacturer_fld],cursor)
    if manf_exists:
        return Manf_id
    else:
        return None

def AddFixtureToDB(fixture_dict):
    """
    Gets required Manf ID from Manf Name, and adds fixture to Fixture Database
    :param fixture_dict: dict
        dict containing the fixture information
    :return: bool, int
        returns True if Fixture Successfully added
    """

    cursor, connection = initConnection(cfg.DBFILEPATH)
    # Checks if Manufuacturer already exists
    manf_exists, Manf_id = CheckManfExists(fixture_dict[cfg.manufacturer_fld],cursor)
    if not manf_exists:
        # If the Manufacturer does not already exist
        Manf_id = AddNewManufacturer(fixture_dict[cfg.manufacturer_fld],cursor)  # Adds new Manufacturer to DB
    if Manf_id is not None:
        fixture_dict.update({cfg.manf_ID_fld:Manf_id})
        # Deletes the Manufacturer Name from Fixture Dict so that only the Manf_ID is written to the Fixture DB
        del fixture_dict[cfg.manufacturer_fld]
    else:
        print(f"Manufacturer ID is None! Aborting!")
        return False   # Cancels Committing changes to DB and tells Flask operation failed

    try:
        # Inserts Fixture into DB
        InsertRowIntoTable(cursor,cfg.FIXTURE_TBL_NAME,fixture_dict)
    except Exception as e:
        print(f"Error Inserting Fixture into DB! Aborting")
        print(f"Error Msg: {e}")
        return False, None  # Cancels Committing changes to DB and tells Flask operation failed

    fix_id = cursor.lastrowid  # Gets the FixId for the last inserted Fixture
    print("Successfully Inserted Fixture Into Database saving, DB!")
    cursor.close()
    connection.commit()  # Commits Changes
    connection.close()
    return True, fix_id

if __name__ == '__main__':
    fix_data = GetFixtureByID(1)
    print(fix_data)