import pandas as pd
import DBTasks as DB
import config as cfg

InstType = 'InstType'
Watt = 'Wattage'
Weight = 'Weight'
Conn_In = 'Connector In'
Conn_Out = 'Connector Out'
Manf_ID = 'ManufacturerID'
Manf_name = 'Manufacturer Name'


def getExcelData(cursor):
    df = pd.read_excel("ML Fixture IMport.xlsx")

    fixture_dict = df.to_dict()

    final_fix_data = []
    final_record_list = []

    used_manf_ids = []  # List of already used manufacturers IDs
    for eachInd in df.index:
        cur_manf_id = df[Manf_ID][eachInd]
        print(cur_manf_id)
        # fixture_dict = {cfg.fixture_name_fld: df[InstType][eachInd],
        #                 cfg.manf_ID_fld: cur_manf_id,
        #                 cfg.wattage_fld: df[Watt][eachInd],
        #                 cfg.weight_fld: df[Weight][eachInd],
        #                 cfg.userID_fld: '1',
        #                 cfg.conn_in_fld: df[Conn_In][eachInd],
        #                 cfg.conn_out_fld: df[Conn_Out][eachInd],
        #                 cfg.reputation_fld: '0'
        #        }
        fixture_tuple = (df[InstType][eachInd],
                        int(df[Manf_ID][eachInd]),
                        df[Watt][eachInd],
                        df[Weight][eachInd],
                        '1',
                        df[Conn_In][eachInd],
                        df[Conn_Out][eachInd],
                        '0'
               )
        if cur_manf_id not in used_manf_ids:
            print(f"{cur_manf_id} not in Manf ids inserting to manf table")
            manf_val_dict =   [{cfg.manf_ID_fld: int(cur_manf_id),
                                cfg.manufacturer_fld: df[Manf_name][eachInd],
                                cfg.userID_fld: '1'
                                }]

            InsertNewManufacturer(cursor,manf_val_dict)
            used_manf_ids.append(cur_manf_id)
        final_fix_data.append(fixture_dict)
        final_record_list.append(fixture_tuple)
        print(fixture_tuple)
    InsertFixture(cursor,final_record_list)

def InsertFixture(cursor,fixtureValues ):
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
    # Creates Fixture Table
    DB.createTable(cursor,cfg.FIXTURE_TBL_NAME,col_names,col_types)
    InsertMultipleFixRow(cursor, cfg.FIXTURE_TBL_NAME, col_names, fixtureValues)

def InsertMultipleFixRow(cursor, table_name, column_names, values):
    cols = f"{cfg.fixture_name_fld},{cfg.manf_ID_fld}, {cfg.wattage_fld},{cfg.weight_fld},{cfg.userID_fld},{cfg.conn_in_fld},{cfg.conn_out_fld},{cfg.reputation_fld}"
    sql = f"INSERT INTO {table_name} ({cols} ) VALUES (?,?,?,?,?,?,?,?)"

    try:
        # data = (eachRow[cfg.fixture_name_fld], eachRow[cfg.manf_ID_fld], eachRow[cfg.wattage_fld],
        #         eachRow[cfg.weight_fld], eachRow[cfg.userID_fld])
        print(values)
        cursor.executemany(sql, values)  # Inserts rows into DB
    except Exception as e:
        print("Insert Mutliple errorError!")
        print(e)

def InsertNewManufacturer(cursor, manf_vals):
    col_names = [cfg.manf_ID_fld,
                 cfg.manufacturer_fld,
                 cfg.userID_fld
                 ]

    col_types = {cfg.manf_ID_fld : 'INTEGER PRIMARY KEY' ,
                 cfg.manufacturer_fld: 'Text',
                 cfg.userID_fld: 'INTEGER'
                 }

    DB.InsertMafRow(cursor,cfg.MANUFACTURER_TBL_NAME,col_names, manf_vals)

def CreateManf_table(cursor):
    col_names = [cfg.manf_ID_fld,
                 cfg.manufacturer_fld,
                 cfg.userID_fld
                 ]

    col_types = {cfg.manf_ID_fld : 'INTEGER PRIMARY KEY' ,
                 cfg.manufacturer_fld: 'Text',
                 cfg.userID_fld: 'INTEGER'
                 }
    DB.createTable(cursor, cfg.MANUFACTURER_TBL_NAME, col_names, col_types)

if __name__ == '__main__':
    cursor, connection = DB.initConnection(cfg.DBFILEPATH)
    CreateManf_table(cursor)
    getExcelData(cursor)
    DB.CreateUserDB(cursor,connection)
    cursor.close()
    connection.commit()  # Commits Changes
    connection.close()