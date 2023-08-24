from flask import Flask,jsonify, request, make_response
from werkzeug.utils import secure_filename
import config as cfg
from Database import GetFixtureByID, GetAllFixtures, GetFixFromSearchString, GetAllManufacturers, AddFixtureToDB
import os
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler

def setupLogging():
    logging.basicConfig(level=logging.NOTSET)

    # Creates logger object with python module name as logger name
    log = logging.getLogger(cfg.MainLogName)

    # Creates Handler for sending error messages to console
    c_handler = logging.StreamHandler()
    # Creates for writing messages to file
    f_handler = ConcurrentRotatingFileHandler(os.path.abspath(cfg.MLBACKENDLOGPATH), "a", 1000 * 1024, 5)
    c_handler.setLevel(logging.WARNING)
    f_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    log.addHandler(c_handler)
    log.addHandler(f_handler)

    return log

UPLOAD_FOLDER = 'C:\Projects\MLDatabaseBackend\static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}  # File extensions allowed for image upload

log = setupLogging()
log.debug("Logging Setup!")


app = Flask(__name__)  # Create Flask Server
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/Fixture",methods=['GET'])
def GetFixture():
    log.debug("Get Fixture API Call Received!")
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

    log.debug(f"Final Fix Data: {fix_data_dict}")
    response = jsonify(fix_data_dict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/AddFixture", methods=['POST'])
def AddFixture():
    log.debug("Add Fixture API Call Received!")
    log.debug(request.__dict__)

    # fixture_dict = request.get_json()  # Gets JSON Body as dict

    # Attempts to get all params required to add a fixture
    InstType = request.form.get(cfg.fixture_name_fld)
    Manf_name = request.form.get(cfg.manufacturer_fld)
    wattage = request.form.get(cfg.wattage_fld)
    weight = request.form.get(cfg.weight_fld)
    user_ID = request.form.get(cfg.userID_fld)
    conn_in = request.form.get(cfg.conn_in_fld)
    conn_out = request.form.get(cfg.conn_out_fld)
    # log.debug(f"Fixture JSON Dict: {request.form.get(cfg.fixture_name_fld)}")

    # Adds all values to DB
    fixture_dict = {cfg.fixture_name_fld: InstType,
                    cfg.manufacturer_fld: Manf_name,
                    cfg.wattage_fld: wattage,
                    cfg.weight_fld: weight,
                    cfg.userID_fld: user_ID,
                    cfg.conn_in_fld: conn_in,
                    cfg.conn_out_fld: conn_out
                    }
    log.debug(f"Fixture Dict: {fixture_dict}")
    check, fixture_dict = PerformChecks(fixture_dict)  # Checks Fixture info for problems
    if not check:
        response = make_response("Error Adding Fixture")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 400
    check,fix_id = AddFixtureToDB(fixture_dict)
    if not check:
        # If an error occured whilst inserting fixture
        response = make_response("Error Adding Fixture")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 500
    if 'file' in request.files:
        log.debug(f"Image file detected in request adding image")
        file = request.files['file']
        if file.filename == '':
            log.debug('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Saves the image to the static image folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_name, file_extension = os.path.splitext(filename)
            file_extension = '.png'
            log.debug(file_extension)
            log.debug(fix_id)
            new_filename = str(fix_id)+file_extension
            # Renames Image file to fixture ID
            os.rename(os.path.join(app.config['UPLOAD_FOLDER'], filename),os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

    response = {}
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response,200

def PerformChecks(fixture_dict):
    """
    Chceks incoming fixture info for errors, and attempts to correct any errors
    :param fixture_dict: dict
    :return: bool, dict
    """
    if not CheckIfInstTypeIsBlank(fixture_dict[cfg.fixture_name_fld]):
        # Checks if Fixture Name is Blank
        log.debug("Fixture Name is Blank")
        return False,fixture_dict
    if not CheckIfInstAlreadyExists(fixture_dict[cfg.fixture_name_fld]):
        # Checks if Fixture Already Exists
        log.debug("Fixture Already Exists!")
        return False, fixture_dict

    return True,fixture_dict


def CheckIfInstTypeIsBlank(InstType):
    """
    Checks if Inst Type field is Blank
    :param InstType: str
    :return: bool
    """
    if InstType == '' or InstType is None:
        log.debug(f"Inst Type is Blank!")
        return False
    else:
        return True

def CheckIfInstAlreadyExists(InstType):
    """
    Checks if Instrument already exists
    :param InstType: str
        Fixture name
    :return: bool
    """
    Fix_data = GetFixFromSearchString(InstType)  # Checks if fixture is already in DB
    if Fix_data:
        log.debug(f"Fixture Already Exists! Returning False")
        return False
    else:
        log.debug("Fixture does not already exist returning True")
        return True


@app.route("/Manufacturer", methods=['GET'])
def GetManufacturers():
    log.debug("API Call Received to /Manufactuer!")
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
        log.debug(f"Specific Fixture image specified sending {test_FP}")
        return app.send_static_file(f"{fix_id}.png")

    else:
        log.debug(f"No Fixture image found updating to {cfg.stock_image_FileName}")
        return app.send_static_file(cfg.stock_image_FileName)

if __name__ == '__main__':

    app.run(debug=True)