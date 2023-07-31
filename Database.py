import sqlite3


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


def createTable(cursor,table_name, column_names,column_types_dict):
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

    if checkTableExists(cursor,table_name):  # Checks if Table already exists
        # If Table Already exists
        print(f"Table Already exists!")
        return
    else:
        # If Table does not already exist
        column = ''  # Blank string that will contain column names
        for eachColumnName in column_names:
            column += f'{eachColumnName} {column_types_dict[eachColumnName]},'
        print(f"CREATE TABLE {table_name} ({column[:-1]})")
        # Creates Table and inserts specified columns
        cursor.execute(f"CREATE TABLE {table_name} ({column[:-1]})")

def GetFixtureByID(ID):
    cursor = initConnection('DB/ProdLx')
    if checkTableExists(cursor,table_name):  # Checks if Table already exists
        # If Table Already exists
        print(f"Table Already exists!")
        return