"""
LocalFileConversion class reads the directory
converts the UTC timestamps to local timestamps
also return the max and min dates available
"""
import os
from dateutil import tz
from datetime import datetime
from helpers.messages import Messages
from collections import OrderedDict


class LocalFileConversion:

    def __init__(self, path: str):
        """
        Requires the path of the directory
        """
        self.path = path
        self.__process_files()
        pass

    def __new__(cls, path: str) -> bool:
        """
        Requires the valid path of the directory
        otherwise doesn't allow the object to be created
        """
        if cls.__is_path_exists(cls, path):
            return super(LocalFileConversion, cls).__new__(cls)
        else:
            return

    def __sort_on_camera_date_hour(self, file_name):
        """
        This is utility function for sorted to sort the string values
        according to camera, date and hour
        """
        # Check if the camera- string is available in the path
        if 'camera-' in file_name[0]:
            try:
                # Split the file to get the camera number
                splitted = file_name[0].split('camera-')[1].split('/')

                # Check to see if the date exists in the splitted path
                if len(splitted) >= 3:

                    # Get the date and split it in numbers
                    date = splitted[2].split('-')

                    # Cjeck to see if the  hour available in the path
                    if len(splitted) == 4:

                        # Sort camera wise then date wise and finally hour wise
                        sorting_value = splitted[0] + \
                            date[2]+date[1]+date[0]+splitted[3]
                    else:

                        # If hour directory is not available sort camera wise and date wise
                        sorting_value = splitted[0]+date[2]+date[1]+date[0]
                    return int(sorting_value)
            
            # If the file names are mixed this error will come
            except:
                return 0

        return 0

    def __process_files(self):
        """
        Process the files and stores them in the dictionary
        for fast access
        """
        # Parameters:
        #    None

        # Returns:
        #    None

        # The ordered dictionary is used to keep track of files inserted
        # as the files are sorted so order dictionary will do the job
        self.__processed_files = OrderedDict()

        # This is another dictionary created to keep track of file
        # camera wise, This is an extra dictionary that is kept if in
        # future have to filter the files camerawise instead of grouping them
        self.__camera_wise_processed_files = OrderedDict()

        # Reads the directory listings and sort them using sorted
        # This O(nlog(n)) sorting will save a lot of time later
        # This will group the files camera wise also
        dir_list = sorted(os.walk(self.path, topdown=False),
                          key=self.__sort_on_camera_date_hour)

        # Get the timezone for local time zone
        to_zone = tz.tzlocal()

        for root, _, files in dir_list:
            current_camera = ''
            file_date = ''
            datewise_map = {}
            files_processed = False
            for filename in files:
                # To tell the code that this loop is executed
                files_processed = True
                try:
                    # Split the file name to extract camera and date
                    splitted_file_name = filename.split('_')
                    current_camera = splitted_file_name[2]

                    # Read the date as files are png we can safely
                    # skip last 4 digits of the date
                    file_date = splitted_file_name[3][:-4]

                    # Convert the time in utc date
                    utc_date = datetime.strptime(
                        file_date, '%Y-%m-%dT%Hh%Mm%Ss%z')

                    # Convert the date in local timezone and read as date
                    key_local_date = utc_date.astimezone(
                        to_zone).date().strftime('%Y-%m-%d')

                    # Putting in map because there can be 3 time zones in an hour
                    # so in an hour folder there can be 3 dates to be stored
                    if key_local_date not in datewise_map.keys():
                        datewise_map[key_local_date] = []
                    
                    datewise_map[key_local_date].append(filename)
                
                # There can be multiple exception scenarios
                # if file name is wrong, date format is incorrect
                except:

                    # Continue in case of exception
                    continue

            if files_processed:
                self.__store_data(current_camera, root, datewise_map)

    def __store_data(self, camera: str, root: str, aggregated_files: dict):
        """
        This function stores the formulated data in the maps.
        Two maps are kept with enhancements in mind that the
        access might be required camera wise also
        """
        # Parameters:
        #    str (camera)            : The string name of the camera where image is from.
        #    str (root)              : The string file path of the root folder.
        #    dict (aggregated_files) : A dictionary of aggregated files that can contain
        #                              files for maximum 3 hours depending on timezone

        # Returns:
        #    None

        for key, value in aggregated_files.items():

            # Checks if key for that date is created, otherwise create
            # it in both dictionaries
            if key not in self.__processed_files.keys():
                self.__processed_files[key] = []
            if key not in self.__camera_wise_processed_files.keys():
                self.__camera_wise_processed_files[key] = {}

            # Check if camera key is created inside the date dictionary
            if camera not in self.__camera_wise_processed_files[key].keys():
                self.__camera_wise_processed_files[key][camera] = []

            # Format the files according to given format and add them
            self.__processed_files[key].append(os.path.join(
                root, "*{{{0}}}".format(str(sorted(value))[1:-1])))

            self.__camera_wise_processed_files[key][camera].append(os.path.join(
                root, "*{{{0}}}".format(str(sorted(value))[1:-1])))

    def get_processed_files(self) -> bool:
        """
        As processed_files variable is kind of hidden in class,
        this function helps to check if there are any files in the
        dictonary
        """
        # Parameters:
        #    None

        # Returns:
        #    bool (files_exist): true if there are files in the dictionary

        return bool(self.__processed_files)

    def __is_path_exists(self, absolutePath: str) -> bool:
        """
        Utility function to check if the path exists on the drive
        """
        # Parameters:
        #    str (absolutePath): The string path of the folder to be read.

        # Returns:
        #    bool: True if the path exists, False otherwise.

        return os.path.isdir(absolutePath.strip())

    def update_files(self):
        """
        Reads the files from the directory again and change the
        dictionary for new files, Call the function after updating path
        """
        # Parameters:
        #    None

        # Returns:
        #    None

        self.__process_files()

    def update_path(self, pathname: str) -> int:
        """
        Updates the path, This function updates the path only, 
        doesn't reads the latest files. Call update_path_and_files
        for changing the files list also
        """
        # Parameters:
        #    str (pathname): The string path of the folder to be read.

        # Returns:
        #    int: Returns integer for the error or success

        if self.path == pathname:
            return Messages.SAME_FILE_PATH
        if self.__is_path_exists(pathname):
            self.path = pathname
            return Messages.FILE_PATH_UPDATED
        else:
            return Messages.FILE_NOT_EXISTS

    def update_path_and_files(self, pathname: str) -> int:
        """
        Updates the path and dictionary for the files to be retrieved
        """
        # Parameters:
        #    str (pathname): The string path of the folder to be read.

        # Returns:
        #    int: Returns integer for the error or success

        message = self.update_path(pathname)
        if message == Messages.FILE_PATH_UPDATED:
            self.update_files()
        else:
            return message

    def get_start_end_date(self) -> str:
        """
        Get start and end date of the files
        """
        # Parameters:
        #    None

        # Returns:
        #    string: Returns string in format date range: {start_date} - {end_date}

        # As the dates are sorted before processing
        # First and last indexes will contain the start and end date respectively
        # Read the keys
        processed_list = list(self.__camera_wise_processed_files.keys())

        # Return first and last key for date range
        return "date range: {start_date} - {end_date}".format(start_date=processed_list[0], end_date=processed_list[-1])

    def get_files_in_local_timezone(self, date: str):
        """
        Give the files for local timezone
        """
        # Parameters:
        #     str (date): The string date for return the files in local timezone

        # Returns:
        # list(dict): Returns the files in list(dict) in following format
        # [
        #    {
        #       "date_tz" str: "2020-10-31",
        #       "files" list: [
        #           "absolute_file_path"
        #        ]
        #    },
        # ]

        # First need to check if the date exist in our data
        if date in self.__processed_files.keys():

            # Create the return data format
            return_list = []
            return_object = {}
            return_object["date_tz"] = date
            return_object["files"] = self.__processed_files[date]
            return_list.append(return_object)
            return return_list
        else:
            # Error Message if date is given out of the range
            return Messages.DATE_DOES_NOT_EXISTS

    def get_files_in_local_timezone_by_camera(self, date: str, camera: str):
        """
        Give the files for local timezone and camera
        """

        # Parameters:
        #     str (date): The string date for return the files in local timezone
        #     str (camera): The string camera for return the files of that camera

        # Returns:
        # list(dict): Returns the files in list(dict) in following format
        # [
        #    {
        #       "date_tz" str: "2020-10-31",
        #       "camera"  str: "camera-1",
        #       "files" list: [
        #           "absolute_file_path"
        #        ]
        #    },
        # ]
        if date in self.__camera_wise_processed_files.keys():
            if camera in self.__camera_wise_processed_files[date].keys():
                return_list = []
                return_object = {}
                return_object["date_tz"] = date
                return_object["camera"] = camera
                return_object["files"] = self.__camera_wise_processed_files[date][camera]
                return_list.append(return_object)
                return return_list
            else:
                # Error Message if camera is not available
                return Messages.CAMERA_DOES_NOT_EXISTS
        else:
            # Error Message if date is given out of the range
            return Messages.DATE_DOES_NOT_EXISTS

    def get_files_in_local_timezone_dict_by_camera(self, date: str):
        """
        Give the files for local timezone grouped by camera
        """
        # Parameters:
        #     str (date): The string date for return the files in local timezone

        # Returns:
        # list(dicts): Returns the files in list(dicts) in following format
        # [
        #    {
        #       "date_tz" str: "2020-10-31",
        #       "camera"  str: "camera-1",
        #       "files" list: [
        #           "absolute_file_path"
        #        ]
        #    },
        #    {
        #       "date_tz" str: "2020-10-31",
        #       "camera"  str: "camera-2"
        #       "files" list: [
        #           "absolute_file_path"
        #        ]
        #    },
        #
        # ]
        if date in self.__camera_wise_processed_files.keys():
            return_list = []

            # Read the cameras in processed camera dictionary
            for camera in self.__camera_wise_processed_files[date].keys():

                # Create the return object
                return_object = {}
                return_object["date_tz"] = date
                return_object["camera"] = camera
                return_object["files"] = self.__camera_wise_processed_files[date][camera]
                return_list.append(return_object)
            return return_list
        else:
            # Error Message if date is given out of the range
            return Messages.DATE_DOES_NOT_EXISTS
