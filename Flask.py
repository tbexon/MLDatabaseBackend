from flask import Flask,jsonify, request
import config as cfg


app = Flask(__name__)  # Create Flask Server

@app.route("/Fixture",methods=['GET'])
def GetFixture():
    print("API Call Received!")
    params = request.args.to_dict()  # Converts params from GET request to dict

    fix_ID = params[cfg.fixture_ID_fld]
    print(fix_ID)
    print(request.args.to_dict())
    return jsonify({'status': 'success'})


if __name__ == '__main__':

    app.run(debug=True)