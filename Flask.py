from flask import Flask,jsonify, request
import config as cfg
from Database import GetFixtureByID, GetAllFixtures


app = Flask(__name__)  # Create Flask Server

@app.route("/Fixture",methods=['GET'])
def GetFixture():
    print("API Call Received!")
    params = request.args.to_dict()  # Converts params from GET request to dict

    fix_ID = request.args.get(cfg.fixture_ID_fld)  # Attempts to get the fixture ID if it has been included in request
    if fix_ID:
        # If a specific fixture ID has been specified in request URL
        fix_data_dict = GetFixtureByID(fix_ID)  # Gets the individual fixture Row based on Fix ID
    else:
        # If no fixture ID has been specified
        fix_data_dict = GetAllFixtures()  # Gets all fixtures in Fixture Table
    print(f"Final Fix Data: {fix_data_dict}")
    return jsonify(fix_data_dict)


if __name__ == '__main__':

    app.run(debug=True)