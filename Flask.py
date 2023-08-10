from flask import Flask,jsonify, request
import config as cfg
from Database import GetFixtureByID, GetAllFixtures, GetFixFromSearchString, GetAllManufacturers
import os


app = Flask(__name__)  # Create Flask Server

@app.route("/Fixture",methods=['GET'])
def GetFixture():
    print("API Call Received!")
    print(str(request))
    params = request.args.to_dict()  # Converts params from GET request to dict

    fix_ID = request.args.get(cfg.fixture_ID_fld)  # Attempts to get the fixture ID if it has been included in request
    # Attempts to get the fixture name if it has been included in request
    search_string = request.args.get(cfg.fixture_name_fld)
    if fix_ID:
        # If a specific fixture ID has been specified in request URL
        fix_data_dict = GetFixtureByID(fix_ID)  # Gets the individual fixture Row based on Fix ID
    elif search_string:
        fix_data_dict = GetFixFromSearchString(search_string)  # Searches DB for specific InstType
    else:
        # If no fixture ID has been specified
        fix_data_dict = GetAllFixtures()  # Gets all fixtures in Fixture Table
    print(f"Final Fix Data: {fix_data_dict}")
    response = jsonify(fix_data_dict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


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