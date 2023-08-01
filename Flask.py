from flask import Flask,jsonify, request
import config as cfg
from Database import GetFixtureByID


app = Flask(__name__)  # Create Flask Server

@app.route("/Fixture",methods=['GET'])
def GetFixture():
    print("API Call Received!")
    params = request.args.to_dict()  # Converts params from GET request to dict

    fix_ID = params[cfg.fixture_ID_fld]
    fix_data_dict = GetFixtureByID(fix_ID)
    return jsonify(fix_data_dict)


if __name__ == '__main__':

    app.run(debug=True)