"""
These are tests for the LocalFileConversion class
"""
import sys
sys.path.append('../src')

import json
from helpers.messages import Messages
from datetime import datetime, timedelta
from helpers.utc_offset_calculations import get_local_utc_offset
from file_converter.local_file_conversion import LocalFileConversion
import unittest
import logging
import os
from dateutil import tz
import time

class TestLocalFileConversion (unittest.TestCase):

    # Some predefined variables for testing different scenarios
    FOLDER_PATH = '../input/node/images/frames/'
    ERROR_PATH = '../../input/node/images/frames/'
    NEW_PATH = '../input2/node/images/frames/'
    LOCAL_UTC_OFFSET = ''
    TEST_LOCAL_ONLY = False
    __CAMERA_PATH = '../input/node/images/frames/farm-xxx/camera-1/images'
    __OUTPUT_PATH = '../output/node/images/frames/farm-xxx/expected_output/timezone_wise'
    __CAMERA_WISE_OUTPUT_PATH = '../output/node/images/frames/farm-xxx/expected_output/timezone_camera_wise'
    __CAMERA_WISE_DICT_OUTPUT_PATH = '../output/node/images/frames/farm-xxx/expected_output/timezone_camera_wise_dict'
    __TIME_ZONE_MAP = {
        "-12": "Etc/GMT+12",
        "-11": "Etc/GMT+11",
        "-10": "Etc/GMT+10",
        "-9.5": "Pacific/Marquesas",
        "-9": "Etc/GMT+9",
        "-8": "Etc/GMT+8",
        "-7": "Etc/GMT+7",
        "-6": "Etc/GMT+6",
        "-5": "Etc/GMT+5",
        "-4": "Etc/GMT+4",
        "-3.5": "America/St_Johns",
        "-3": "Etc/GMT+3",
        "-2": "Etc/GMT+2",
        "-1": "Etc/GMT+1",
        "0": "Etc/GMT",
        "+1": "Etc/GMT-1",
        "+2": "Etc/GMT-2",
        "+3": "Etc/GMT-3",
        "+4": "Etc/GMT-4",
        "+4.5": "Asia/Kabul",
        "+5": "Etc/GMT-5",
        "+5.5": "Asia/Colombo",
        "+5.75": "Asia/Kathmandu",
        "+6": "Etc/GMT-6",
        "+6.5": "Asia/Yangon",
        "+7": "Etc/GMT-7",
        "+8": "Etc/GMT-8",
        "+8.75": "Australia/Eucla",
        "+9": "Etc/GMT-9",
        "+9.5": "Australia/North",
        "+10": "Etc/GMT-10",
        "+10.5": "Australia/LHI",
        "+11": "Etc/GMT-11",
        "+12": "Etc/GMT-12",
        "+12.75": "Pacific/Chatham",
        "+13": "Etc/GMT-13",
        "+14": "Etc/GMT-14"
    }

    def test_folder_does_not_exists(self):
        # This test checks the creation of the object when the
        # wrong path is given, by default no object should be
        # created if the path is incorrect.

        logger.info('Running test case test_folder_does_not_exists')
        file_converter = LocalFileConversion(self.ERROR_PATH)
        self.assertIsNone(file_converter)
        logger.info('Test case passed test_folder_does_not_exists')

    def test_read_files(self):
        # This test check that files are read at the creation of
        # object. It fails if no valid files are read
        logger.info('Running test case test_read_files')

        file_converter = LocalFileConversion(self.FOLDER_PATH)
        self.assertIsNotNone(file_converter)

        self.assertTrue(file_converter.get_processed_files())
        logger.info('Test case passed test_read_files')

    def test_update_path_with_same_directory(self):
        # This test is to check if update file path returns
        # proper error if previous path is given

        logger.info('Running test test_update_path_with_same_directory')
        file_converter = LocalFileConversion(self.FOLDER_PATH)
        self.assertIsNotNone(file_converter)

        self.assertEqual(file_converter.update_path(
            self.FOLDER_PATH), Messages.SAME_FILE_PATH)
        logger.info('Test case passed test_update_path_with_same_directory')

    def test_update_path_with_non_existent_directory(self):
        # This test is to check if update file path returns
        # proper error if wrong path is given

        logger.info('Running test test_update_path_with_non_existent_directory')
        file_converter = LocalFileConversion(self.FOLDER_PATH)
        self.assertIsNotNone(file_converter)

        self.assertEqual(file_converter.update_path(
            self.ERROR_PATH), Messages.FILE_NOT_EXISTS)
        logger.info(
            'Test case passed test_update_path_with_non_existent_directory')

    def test_new_existent_directory(self):
        # This test is to check if update file path returns
        # proper message if proper path is given
        logger.info('Running test test_new_existent_directory')
        file_converter = LocalFileConversion(self.FOLDER_PATH)
        self.assertIsNotNone(file_converter)

        self.assertEqual(file_converter.update_path(
            self.NEW_PATH), Messages.FILE_PATH_UPDATED)
        logger.info('Test case passed test_new_existent_directory')

    def match_start_end_date_for_time_zone(self, utc_offset, value, file_converter, highest_date, lowest_date):
        # The function is helper function to match the results for
        # test_start_end_date

        # Set the local enviornment timezone to be each timezone
        os.environ['TZ'] = value
        time.tzset()

        # Read the files again to change the timezone
        file_converter.update_files()

        # Get the date range for current timezone
        date_range = file_converter.get_start_end_date()

        # As timezone map key is + or - with hour so adding/subtratcting
        # number of the hours in highest date and lowest date will convert
        # them to local timezone
        highest_date_processed = highest_date + \
            timedelta(hours=float(utc_offset))
        lowest_date_processed = lowest_date + \
            timedelta(hours=float(utc_offset))

        # Format the local date range calculated to the format provided
        date_range_local = "date range: {start_date} - {end_date}".format(start_date=lowest_date_processed.date(
        ).strftime('%Y-%m-%d'), end_date=highest_date_processed.date().strftime('%Y-%m-%d'))

        # The both date ranges should be equal
        self.assertEqual(date_range, date_range_local)

        # As both date ranges are equal means our highest processed and lowest processed dates are correct
        # just do bit of checking if highest date is greater than equal to lowest date

        self.assertGreaterEqual(
            highest_date_processed, lowest_date_processed)

        logging.info('Date Range passes for UTC{utc_num} with values: "{date_range}"'.format(
            utc_num=utc_offset, date_range=date_range))

    def test_start_end_date(self):
        # This test checks on camera-1 folder if the returned start and end date is correct
        # This test loops over a camera folder and converts the dates
        # in date format and look for highest and lowest dates to check
        # manually.
        #
        # This test then move the highest date to 23:59:59 time so adding one minute can
        # change the date.
        #
        # After performing initial processing this test loop over all UTC timezones
        # and manually converts the highest and lowest to that timezone
        #
        # Finally this test checks if the result given by class are equal to what
        # manual calculations brings.
        #
        # This test also checks if end date is greater than start date

        logger.info('Running test test_start_end_date')

        file_converter = LocalFileConversion(self.__CAMERA_PATH)
        self.assertIsNotNone(file_converter)

        # Read list of the folder with dates
        folder_date_list = os.listdir(self.__CAMERA_PATH)

        # Initialize the lowest and highest dates to minimum dates
        lowest_date = datetime.min
        highest_date = datetime.min

        # Loop over the list returned by os.listdir
        for value in folder_date_list:

            # Convert each folder name to date object for easier comparison
            date = datetime.strptime(
                value, '%Y-%m-%d')

            # Check if current folder date is lowest than previous lowest or is minimum
            if date < lowest_date or lowest_date == datetime.min:
                lowest_date = date

            # Check if current folder date is greater than previous highest
            if date > highest_date:
                highest_date = date

        # Make highest date to be last second of the day
        highest_date = highest_date.replace(hour=23, minute=59, second=59)

        # Set the enviornment to user local time offset
        # Some test might have changed the enviornment
        os.environ['TZ'] = self.__TIME_ZONE_MAP[self.LOCAL_UTC_OFFSET]
        time.tzset()

        if self.TEST_LOCAL_ONLY:

            # Test for local time zone only
            self.match_start_end_date_for_time_zone(
                self.LOCAL_UTC_OFFSET, self.__TIME_ZONE_MAP[self.LOCAL_UTC_OFFSET], file_converter, highest_date, lowest_date)
        else:

            # Check for all timezone
            for key, value in self.__TIME_ZONE_MAP.items():
                self.match_start_end_date_for_time_zone(
                    key, value, file_converter, highest_date, lowest_date)

        logger.info(
            'Test passed test_start_end_date')

    def match_files_by_local_timezone(self, utc_offset, value, file_converter):
        # The function is helper function to match the results
        # for test_files_by_local_timezone

        # Change the timezone for all available timezones
        os.environ['TZ'] = value
        time.tzset()

        # Update the files to read new timezone
        file_converter.update_files()

        # Get the files for specific timezone
        files_in_local_timezone = file_converter.get_files_in_local_timezone(
            "2020-11-03")

        # Check if files are actually returned for that date
        self.assertIsNot(files_in_local_timezone,
                         Messages.DATE_DOES_NOT_EXISTS)

        expected_output_from_file = []

        # Read the json files
        with open(os.path.join(self.__OUTPUT_PATH, 'utc{file}.out'.format(file=utc_offset))) as json_file:

            # Loads the json and convert into dict
            expected_output_from_file = json.load(json_file)

        # Asserts that all the files matches
        self.assertEqual(expected_output_from_file,
                         files_in_local_timezone)

        # Log the results in log file
        logging.info('Output passes for UTC{utc_num} with data: {data}'.format(
            utc_num=utc_offset, data=json.dumps(files_in_local_timezone, indent=4, ensure_ascii=False)))

    def test_files_by_local_timezone(self):
        # This test is to see if the files return are sorted and according to format provided
        #
        # This test checks for each timezone and reads the preprocessed json for the expected
        # output and matches if the results return for that timezone are correct
        #
        # Also as valid date is given in this test it ensures that error message should not
        # return

        logger.info('Running test test_files_by_local_timezone')
        file_converter = LocalFileConversion(self.NEW_PATH)
        self.assertIsNotNone(file_converter)

        # Set the enviornment to user local time offset
        # Some test might have changed the enviornment
        os.environ['TZ'] = self.__TIME_ZONE_MAP[self.LOCAL_UTC_OFFSET]
        time.tzset()

        if self.TEST_LOCAL_ONLY:

            # Test for local time zone only
            self.match_files_by_local_timezone(
                self.LOCAL_UTC_OFFSET, self.__TIME_ZONE_MAP[self.LOCAL_UTC_OFFSET], file_converter)
        else:

            # Loop over the map of the timezone
            for key, value in self.__TIME_ZONE_MAP.items():
                self.match_files_by_local_timezone(key, value, file_converter)

        # End test case log
        logger.info("Test passed test_files_by_local_timezone")

    def test_invalid_date(self):
        logger.info('Running test test_invalid_date')
        file_converter = LocalFileConversion(self.FOLDER_PATH)
        self.assertIsNotNone(file_converter)

        self.assertEqual(file_converter.get_files_in_local_timezone(
            "2020-11-08"), Messages.DATE_DOES_NOT_EXISTS)
        logger.info("Test passed test_invalid_date")

    def test_update_files_and_path(self):
        logger.info('Running test test_update_files_and_path')
        file_converter = LocalFileConversion(self.FOLDER_PATH)
        self.assertIsNotNone(file_converter)

        new_files = file_converter.update_path_and_files(self.NEW_PATH)
        self.assertIsNot(new_files, Messages.DATE_DOES_NOT_EXISTS)
        logger.info("Test passed test_update_files_and_path")

    def match_get_files_by_camera_and_timezone(self, utc_offset, value, file_converter):
        # This is the helper function to match the results
        # for test case test_get_files_by_camera_and_timezone

        # Change the timezone for all available timezones
        os.environ['TZ'] = value
        time.tzset()

        # Update the files to read new timezone
        file_converter.update_files()

        # Read the results from the algorithm
        camera_wise_files = file_converter.get_files_in_local_timezone_by_camera(
            '2020-11-03', 'camera-1')

        # Check if valid results are returned for current parameters
        self.assertIsNot(camera_wise_files,
                         Messages.CAMERA_DOES_NOT_EXISTS)
        self.assertIsNot(camera_wise_files, Messages.DATE_DOES_NOT_EXISTS)

        # Read the json files
        with open(os.path.join(self.__CAMERA_WISE_OUTPUT_PATH, 'utc{file}.out'.format(file=utc_offset))) as json_file:

            # Loads the json and convert into dict
            expected_output_from_file = json.load(json_file)

        # Log the results in log file
        logging.info('Output passes for UTC{utc_num} with data: {data}'.format(
            utc_num=utc_offset, data=json.dumps(camera_wise_files, indent=4, ensure_ascii=False)))

        # Asserts that all the files matches
        self.assertEqual(expected_output_from_file,
                         camera_wise_files)

    def test_get_files_by_camera_and_timezone(self):
        # This test case tests the filtering of the files based on camera
        # and timezone
        #
        # This test checks for each timezone and reads the preprocessed json for the expected
        # output and matches if the results return for that timezone and camera are correct
        #
        # This test also ensures that invalid camera and invalid date is not returned as
        # passed date and camera are correct

        logger.info('Running test test_get_files_by_camera_and_timezone')
        file_converter = LocalFileConversion(self.FOLDER_PATH)
        self.assertIsNotNone(file_converter)

        # Set the enviornment to user local time offset
        # Some test might have changed the enviornment
        os.environ['TZ'] = self.__TIME_ZONE_MAP[self.LOCAL_UTC_OFFSET]
        time.tzset()

        if self.TEST_LOCAL_ONLY:

            # Match for local timezone only
            self.match_get_files_by_camera_and_timezone(
                self.LOCAL_UTC_OFFSET, self.__TIME_ZONE_MAP[self.LOCAL_UTC_OFFSET], file_converter)
        else:

            # Loop over the map of the timezone
            for key, value in self.__TIME_ZONE_MAP.items():
                self.match_get_files_by_camera_and_timezone(
                    key, value, file_converter)

        logger.info("Test passed test_get_files_by_camera_and_timezone")

    def match_get_files_in_local_timezone_dict_by_camera(self, utc_offset, value, file_converter):

        # Change the timezone for all available timezones
        os.environ['TZ'] = value
        time.tzset()

        # Update the files to read new timezone
        file_converter.update_files()

        # Read the results from the algorithm
        camera_wise_dict_files = file_converter.get_files_in_local_timezone_dict_by_camera(
            '2020-11-03')

        # Check if valid results are returned for current parameters)
        self.assertIsNot(camera_wise_dict_files,
                         Messages.DATE_DOES_NOT_EXISTS)

        expected_output_from_file = []

        # Read the json files
        with open(os.path.join(self.__CAMERA_WISE_DICT_OUTPUT_PATH, 'utc{file}.out'.format(file=utc_offset))) as json_file:

            # Loads the json and convert into dict
            expected_output_from_file = json.load(json_file)

        # Log the results in log file
        logging.info('Output passes for UTC{utc_num} with data: {data}'.format(
            utc_num=utc_offset, data=json.dumps(camera_wise_dict_files, indent=4, ensure_ascii=False)))

        # Asserts that all the files matches
        self.assertEqual(expected_output_from_file,
                         camera_wise_dict_files)

    def test_get_files_in_local_timezone_dict_by_camera(self):
        # This test case tests the filtering of the files by timezone grouped on camera
        #
        # This test checks for each timezone and reads the preprocessed json for the expected
        # output and matches if the results return for that timezone are correct and grouped by
        # cameras
        #
        # This test also ensures invalid date error is not returned as
        # passed date is correct

        logger.info(
            'Running test test_get_files_in_local_timezone_dict_by_camera')
        file_converter = LocalFileConversion(self.FOLDER_PATH)
        self.assertIsNotNone(file_converter)

        # Set the enviornment to user local time offset
        # Some test might have changed the enviornment
        os.environ['TZ'] = self.__TIME_ZONE_MAP[self.LOCAL_UTC_OFFSET]
        time.tzset()

        if self.TEST_LOCAL_ONLY:

            # Test for local timezone
            self.match_get_files_in_local_timezone_dict_by_camera(
                self.LOCAL_UTC_OFFSET, self.__TIME_ZONE_MAP[self.LOCAL_UTC_OFFSET], file_converter)
        else:

            # Loop over the map of the timezone
            for key, value in self.__TIME_ZONE_MAP.items():
                self.match_get_files_in_local_timezone_dict_by_camera(
                    key, value, file_converter)

        logger.info(
            "Test passed test_get_files_in_local_timezone_dict_by_camera")


if __name__ == '__main__':

    # Read Local UTC offset and save
    TestLocalFileConversion.LOCAL_UTC_OFFSET = get_local_utc_offset()

    # Read some enviornment variables
    TestLocalFileConversion.FOLDER_PATH = os.environ.get(
        'FOLDER_PATH', TestLocalFileConversion.FOLDER_PATH)
    TestLocalFileConversion.ERROR_PATH = os.environ.get(
        'ERROR_PATH', TestLocalFileConversion.ERROR_PATH)
    TestLocalFileConversion.NEW_PATH = os.environ.get(
        'NEW_PATH', TestLocalFileConversion.NEW_PATH)
    TestLocalFileConversion.TEST_LOCAL_ONLY = os.environ.get(
        'TEST_LOCAL_ONLY', str(TestLocalFileConversion.TEST_LOCAL_ONLY)).lower() not in ('false', '0', 'f')
    
    if TestLocalFileConversion.TEST_LOCAL_ONLY:
        # Create and initialize the logger
        logging.basicConfig(filename="../logs/tests_local_timezone.log",
                            format='%(asctime)s %(message)s',
                            filemode='w')
    else:
        # Create and initialize the logger
        logging.basicConfig(filename="../logs/tests_all_timezones.log",
                            format='%(asctime)s %(message)s',
                            filemode='w')

    # Create object for the logger
    logger = logging.getLogger()

    # Set the threshold level to debugging
    logger.setLevel(logging.DEBUG)

    unittest.main()
