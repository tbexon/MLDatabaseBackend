from flask import Flask,jsonify, request
import config as cfg
from Database import GetFixtureByID, GetAllFixtures, GetFixFromSearchString, GetAllManufacturers, AddFixtureToDB
import os


app = Flask(__name__)  # Create Flask Server

@app.route("/Fixture",methods=['GET'])
def GetFixture():
    print("API Call Received!")
    params = request.args.to_dict()  # Converts params from GET request to dict

    fix_ID = request.args.get(cfg.fixture_ID_fld)  # Attempts to get the fixture ID if it has been included in request
    # Attempts to get the fixture name if it has been included in request
    search_string = request.args.get(cfg.fixture_name_fld)
    manf_string = request.args.get(cfg.manufacturer_fld)
    if fix_ID:
        # If a specific fixture ID has been specified in request URL
        fix_data_dict = GetFixtureByID(fix_ID)  # Gets the individual fixture Row based on Fix ID
    elif search_string:
        if manf_string:
            fix_data_dict = GetFixFromSearchString(search_string,manf=manf_string)  # Searches DB for specific InstType
        else:
            fix_data_dict = GetFixFromSearchString(search_string)  # Searches DB for specific InstType
    else:
        if manf_string:
            # If no fixture ID has been specified
            fix_data_dict = GetAllFixtures(manf=manf_string)  # Gets all fixtures in Fixture Table
        else:
            # If no fixture ID has been specified
            fix_data_dict = GetAllFixtures()  # Gets all fixtures in Fixture Table

    print(f"Final Fix Data: {fix_data_dict}")
    response = jsonify(fix_data_dict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/AddFixture")
def AddFixture():
    # Attempts to get all params required to add a fixture
    InstType = request.args.get(cfg.fixture_name_fld)
    Manf_name = request.args.get(cfg.manufacturer_fld)
    wattage = request.args.get(cfg.wattage_fld)
    weight = request.args.get(cfg.weight_fld)
    user_ID = request.args.get(cfg.userID_fld)
    conn_in = request.args.get(cfg.conn_in_fld)
    conn_out = request.args.get(cfg.conn_out_fld)


    # Adds all values to DB
    fixture_dict = { cfg.fixture_name_fld: InstType,
                    cfg.manufacturer_fld: Manf_name,
                    cfg.wattage_fld:wattage,
                    cfg.weight_fld: weight,
                    cfg.userID_fld: user_ID,
                    cfg.conn_in_fld: conn_in,
                    cfg.conn_out_fld:conn_out
               }
    print(fixture_dict)
    check, fixture_dict = PerformChecks(fixture_dict)  # Checks Fixture info for problems
    if not check:
        return 'Error in Fixture', 400
    check = AddFixtureToDB(fixture_dict)
    if not check:
        # If an error occured whilst inserting fixture
        return "Error Adding Fixture", 500
    return "Success!", 200

def PerformChecks(fixture_dict):
    """
    Chceks incoming fixture info for errors, and attempts to correct any errors
    :param fixture_dict: dict
    :return: bool, dict
    """
    if not CheckIfInstTypeIsBlank(fixture_dict[cfg.fixture_name_fld]):
        return False,fixture_dict

    return True,fixture_dict


def CheckIfInstTypeIsBlank(InstType):
    """
    Checks if Inst Type field is Blank
    :param InstType: str
    :return: bool
    """
    if InstType == '':
        return False
    else:
        return True
@app.route("/Manufacturer", methods=['GET'])
def GetManufacturers():
    print("API Call Received to /Manufactuer!")
    manf_id = request.args.get(cfg.manf_ID_fld)  # Attempts to get the Manufacturers ID if it has been included in request
    if manf_id:
        pass
    else:
        manf_data_dict = GetAllManufacturers()
    response = jsonify(manf_data_dict)  # Converts Manufacturers data into json object
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/FixImg/<int:fix_id>")  #{cfg.fix_img_API_Dir}
def ServeImg(fix_id):

    img_FilePath = os.path.join(os.getcwd(), cfg.fixture_img_FilePath)
    test_FP = os.path.join(img_FilePath, f"{fix_id}.png")
    if os.path.isfile(test_FP) is True:
        print(f"Specific Fixture image specified sending {test_FP}")
        return app.send_static_file(f"{fix_id}.png")

    else:
        print(f"No Fixture image found updating to {cfg.stock_image_FileName}")
        return app.send_static_file(cfg.stock_image_FileName)

if __name__ == '__main__':

    app.run(debug=True)