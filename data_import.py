import yaml
import pandas as pd
from sqlalchemy import create_engine
import os
# TODO More try catch statements for missing files and other errors


# TODO use argparser to place config filename as second command line argument 
# e.g. running the file would be:
#               python data_import.py <config_file_here> 
CONFIG_FILENAME = "config.yaml" 

def read_config(file):
    with open(file, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def retrieve_csv(config_data):
    csv_as_df = pd.read_csv(config_data["DATA_FILE"])
    csv_as_df.columns = [col.lower() for col in csv_as_df.columns]
    return csv_as_df


# TODO create a virtual envirnonment variable to store db_name, db_user, db_pwd
def get_database_info():
    # db credentials are saved in environment variables
    db_name = os.getenv("DATABASE_NAME")
    user = os.getenv("DATABASE_USER")
    return db_name, user


def format_db_string(db_name, uname, config_data):
    return config_data["DATABASE"] + '://' + str(uname) + ':@' + config_data["HOST"] + ':' + str(config_data["PORT"]) + '/' + str(db_name)


def main():
    config_data = read_config(CONFIG_FILENAME)

    csv_as_df = retrieve_csv(config_data)
    
    db_name, uname = get_database_info()
    db_info = format_db_string(db_name, uname, config_data)

    engine = create_engine(db_info)

    csv_as_df.to_sql(config_data["TABLE_NAME"], engine, if_exists='replace')
    
    print "Data has been successfully stored in TABLE {0} of DATABASE {1}".format(config_data["TABLE_NAME"], os.getenv("DATABASE_NAME"))

if __name__ == '__main__':
    main()