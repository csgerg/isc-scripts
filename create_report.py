# import modules
import os
import datetime
# https://simplejson.readthedocs.io/en/latest/
# use simplejson for easier decimal handling
import simplejson as json
 
# import own modules
# import modules https://docs.python.org/3/tutorial/modules.html
from get_data import convert_data
 
 
def save_data_into_file(file_data, file_name, file_path, overwrite='no_overwrite'):
    """Save data into file, check that, the path and filename are both exist."""
    path_with_filename = None
    # test the existence of path
    if os.path.exists(file_path):
        # get the current version and construct the full path with teh file name
        path_with_filename = os.path.join(file_path, file_name)
 
        # check if the file is exist
        file_exist = os.path.isfile(path_with_filename)
 
        def write_file():
            # write file with the constructed path and name
            try:
                with open(path_with_filename, 'w', encoding='utf-8') as f:
                    f.write(file_data)
                    f.close()
 
                return "Your data have saved successfully into: {}".format(file_path)
 
            except PermissionError:
                raise PermissionError(
                    "Your don't have right to writhe the data into the specific directory: {}".format(file_path))
            except UnicodeEncodeError as e:
                raise UnicodeEncodeError("Caracer encoding error during file save ({}). {}".format(
                    path_with_filename, e))
 
        # write file if doesn't exist
        if not file_exist:
            return write_file()
 
        # overwrite file if exist and parameter is overwrite
        elif overwrite == 'overwrite' and file_exist:
            return write_file()
 
        else:
            raise FileExistsError("""The file are exist, please use different filename ({})
                                    or use 'overwrite' parameter.""".format(file_name))
 
    else:
        raise FileNotFoundError("The file path isn't exist ({}). Please use valid file path.".format(file_path))
 
 
def read_data_from_file(full_path):
    """read file data from specific directory"""
    # read file without error handling (you can create similar as in save_data_into_file())
    with open(full_path, 'r') as f:
        read_data = f.read()
 
    return read_data
 
 
def custom_json_encoder(o):
    """Custom JSON converter what convert datetime object to string in isoformat"""
    # https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable
    # https://code-maven.com/serialize-datetime-object-as-json-in-python
    # if type is datetime than convert object to string
    if type(o) is datetime.date or type(o) is datetime.datetime:
        return o.isoformat()
 
 
def create_report_files():
    """get data and create txt and json file"""
 
    # get data for multiple use
    result_data = convert_data(20)
 
    # create report path
    path = './'
    file_name_json = 'saved_data.json'
    joined_path = os.path.join(path, file_name_json)  # use this if you like to create url or file/dir path
 
    def create_json_report(file_path, file_name):
        """Create simple JSON file and save the specified path"""
        # convert data to json https://en.wikipedia.org/wiki/JSON
        # json is very good if you like to print or store the data in file
        data_json = json.dumps(result_data,
                               use_decimal=True,  # decimal handling
                               default=custom_json_encoder,  # datetime handling
                               sort_keys=True,  # if you have keys than it will be sorted
                               indent=4 * ' ')  # create indentation (without this line you will get compact format)
 
        # save JSON data into file
        save_data_into_file(data_json, file_name, file_path, 'overwrite')
 
    def get_data_from_json_file(full_path):
        """read JSON file in a specific path and return python data"""
        # create small well structured functions what have only one role
        # later will be your life easier (easier to debug and reuse and it's eliminate the side effects)
 
        # read data from JSON file
        file_data_string = read_data_from_file(full_path)
        # show it is a string
        print("You will get string data from file: {}".format(type(file_data_string)))
 
        # convert data back to list of dictionaries
        python_data = json.loads(file_data_string)
 
        print("It is now a {}.".format(type(python_data)))
 
        # return with list of dictionaries
        return python_data
 
    def create_txt_report(file_data, file_path, file_name):
        """create simple txt file with sql data"""
 
        def compose_report_data(data):
            """create file header and put every dictionary's data into a separate line"""
            # create list for the separate lines
            data_rows = list()
 
            # create header string
            # formatting mini language https://docs.python.org/3/library/string.html#format-specification-mini-language
            header = "{:>6}{:>6}{:>17}{:>22}{:>17}{:>80}".format('code', 'id', 'status', 'last_data', 'country', 'url')
 
            # add the header as a first line
            data_rows.append(header)
 
            # create body rows
            for row in data:
                # convert everything to string (None is not a string)
                row_string = {key: str(value) for key, value in row.items()}
 
                # append every list element to our data_rows list
                # because we use dictionary than we can use format_map function
                # https://docs.python.org/3/library/stdtypes.html#str.format_map
                data_rows.append(
                    "{code:>6}{id:>6}{status:>17}{last_data:>22}{country:>17}{url:>80}".format_map(row_string)
                )
 
            # at the end join the list with page brakes
            constructed_file_string = "\n".join(data_rows)
 
            return constructed_file_string
 
        # get the file data to save (you can use directly this result without this line in the next function)
        result_string = compose_report_data(file_data)
 
        # save JSON data into file
        save_data_into_file(result_string, file_name, file_path, 'overwrite')
        pass
 
    # run functions inside the create_report_files (if you have only functions and don't call them than
    # nothing will happened)
    create_json_report(path, file_name_json)
 
    recovered_data_from_file = get_data_from_json_file(joined_path)
 
    create_txt_report(recovered_data_from_file, path, 'saved_report.txt')
 
 
# create report all files (this line call the function)
create_report_files()
