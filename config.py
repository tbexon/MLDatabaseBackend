# Global Variables

DBNAME = 'MLDatabase.db'
DBFILEPATH = f"DB/{DBNAME}"

# Table Names

FIXTURE_TBL_NAME = "Fixtures"
DMXPROF_TBL_NAME = "DMXProfiles"
MANUFACTURER_TBL_NAME = "Manufacturers"
USERS_TBL_NAME = "Users"

# Fixture Table Column Names
fixture_ID_fld = 'FixID'
fixture_name_fld = 'InstType'
wattage_fld = 'Wattage'
weight_fld = 'Weight'
conn_in_fld = 'Connector_In'
conn_out_fld = 'Connector_Out'
reputation_fld = 'Reputation'
img_name_fld = "Image_Name"


# Manufactere Table Column Names
manf_ID_fld = 'ManufacturerID'
manufacturer_fld = 'Manufacturer'

# User Table
userID_fld = 'UserID'
username_fld = 'Username'
email_fld = "Email"
password_fld = "Password"
admin_fld = "admin_grp"
edit_fld = "edit_grp"
add_fld = "add_grp"
view_fld = "view_grp"
manufacturer_grp_fld = "manufacturer_grp"
moderate_grp_fld = "moderate_grp"


# DMX Profile Table Column Names
DMXprofID_fld = "DMXProfID"
prof_name = "profile_name"
dmxcnt_fld = "DMX_count"

# COLUMN LISTS

# List of Fixture Table Columns Names
fixture_col_names = [fixture_ID_fld,
             fixture_name_fld,
             manf_ID_fld,
             wattage_fld,
             weight_fld,
             userID_fld,
             conn_in_fld,
             conn_out_fld,
             reputation_fld,
             img_name_fld
             ]

# List of Manufacturer Table Columns Names
manf_col_names = [manf_ID_fld,
             manufacturer_fld,
             userID_fld
             ]

# List of User Column names
user_col_names = [userID_fld,
             username_fld,
             email_fld,
             password_fld,
             admin_fld,
             add_fld,
             edit_fld,
             view_fld,
             manufacturer_grp_fld]

