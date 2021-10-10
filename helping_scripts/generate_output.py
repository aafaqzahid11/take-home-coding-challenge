"""
This file is helping file to create the output results for local
timezone and 2 cameras
"""
from datetime import datetime, timedelta
import os
import json

# As this is one time used functions so copied the map over from test class
TIME_ZONE_MAP = {
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


def generate_output_timezone_files():
    """
    This function generates the files for testing
    the output for get_files_in_local_timezone.
    This function generates the files according to given format
    """
    folder_path = '../input2/node/images/frames/farm-xxx/'
    cameras = ['camera-1', 'camera-2']

    output_path = '../output/node/images/frames/farm-xxx/expected_output/timezone_wise'

    # The query will be done on following date
    query_date = datetime(2020, 11, 3)

    for key in TIME_ZONE_MAP.keys():
        main_obj = {}
        main_list = []
        utc_offset = float(key)
        utc_offset = -utc_offset
        start_time = query_date + \
            timedelta(hours=float(utc_offset))

        files = []

        # Store the camera files and create output
        for camera in cameras:

            # Create base path
            base_path = os.path.join(folder_path, camera, 'images')

            # Loop 24 times
            for x in range(24):

                # Add/Subtract UTC hours to date
                cont_time = start_time + \
                    timedelta(hours=float(x))
                
                # Create hour folder path
                hour_folder_path = os.path.join(base_path, cont_time.date().strftime(
                    '%Y-%m-%d'), cont_time.time().strftime('%H'), "*")
                file_names = []

                # Generate file names
                for y in range(6):
                    file_name = 'farm-xxx_barn-3_{camera}_{date}T{hour}h{min}m00s+0000.png'.format(camera=camera, date=cont_time.date(
                    ).strftime('%Y-%m-%d'), hour=cont_time.time().strftime('%H'), min=cont_time.time().strftime('%M'))
                    
                    # Store files in file name object
                    file_names.append(file_name)

                    # Add a minute for each file
                    cont_time = cont_time + \
                        timedelta(minutes=float(1))

                # Format the output according to given output
                output = hour_folder_path + \
                    "{{{0}}}".format(str(file_names)[1:-1])
                files.append(output)

        # Generate list of dict
        main_obj['date_tz'] = query_date.strftime('%Y-%m-%d')
        main_obj['files'] = files
        main_list.append(main_obj)

        # Write output in the json format
        with open(os.path.join(output_path, 'utc{utc_offset}.out'.format(utc_offset=key)), 'w') as output_file:
            json.dump(main_list, output_file, indent=4, ensure_ascii=False)


def generate_output_timezone_camera_files():
    """
    This function generates the output for the timezone camera
    function to test.
    """
    folder_path = '../input/node/images/frames/farm-xxx/'

    # Test with camera-1
    camera = 'camera-1'

    output_path = '../output/node/images/frames/farm-xxx/expected_output/timezone_wise'
    query_date = datetime(2020, 11, 3)

    for key in TIME_ZONE_MAP.keys():

        # Initalize the object and list
        main_obj = {}
        main_list = []
        utc_offset = float(key)
        utc_offset = -utc_offset

        start_time = query_date + \
            timedelta(hours=float(utc_offset))

        files = []

        # Create path as camera is predefined in this function
        base_path = os.path.join(folder_path, camera, 'images')
        for x in range(24):

            cont_time = start_time + \
                timedelta(hours=float(x))

            hour_folder_path = os.path.join(base_path, cont_time.date().strftime(
                '%Y-%m-%d'), cont_time.time().strftime('%H'), "*")
            file_names = []

            for y in range(6):
                
                file_name = 'farm-xxx_barn-3_{camera}_{date}T{hour}h{min}m00s+0000.png'.format(camera=camera, date=cont_time.date(
                ).strftime('%Y-%m-%d'), hour=cont_time.time().strftime('%H'), min=cont_time.time().strftime('%M'))
                
                file_names.append(file_name)
                
                cont_time = cont_time + \
                    timedelta(minutes=float(1))
            
            output = hour_folder_path + "{{{0}}}".format(str(file_names)[1:-1])
            files.append(output)

        # Create the out put
        main_obj['date_tz'] = query_date.strftime('%Y-%m-%d')
        main_obj['camera'] = camera
        main_obj['files'] = files
        main_list.append(main_obj)

        # Write in json file
        with open(os.path.join(output_path, 'utc{utc_offset}.out'.format(utc_offset=key)), 'w') as output_file:
            json.dump(main_list, output_file, indent=4, ensure_ascii=False)


def generate_output_timezone_camera_dict():
  """
  This function generates the output files for
  testing timezone dictionary
  """
  folder_path = '../input/node/images/frames/farm-xxx/'
  cameras = ['camera-1', 'camera-2', 'camera-11', 'camera-21']

  output_path = '../output/node/images/frames/farm-xxx/expected_output/timezone_wise'
  query_date = datetime(2020, 11, 3)

  for key in TIME_ZONE_MAP.keys():

      # initialize the list
      main_list = []
      utc_offset = float(key)
      utc_offset = -utc_offset

      start_time = query_date + \
          timedelta(hours=float(utc_offset))

      for camera in cameras:

          # As object and files are initialized per camera
          # so moved initialization inside camera loop
          main_obj = {}
          files = []

          base_path = os.path.join(folder_path, camera, 'images')

          for x in range(24):

              cont_time = start_time + \
                  timedelta(hours=float(x))

              hour_folder_path = os.path.join(base_path, cont_time.date().strftime(
                  '%Y-%m-%d'), cont_time.time().strftime('%H'), "*")
              file_names = []
              
              for y in range(6):
                  
                  file_name = 'farm-xxx_barn-3_{camera}_{date}T{hour}h{min}m00s+0000.png'.format(camera=camera, date=cont_time.date(
                  ).strftime('%Y-%m-%d'), hour=cont_time.time().strftime('%H'), min=cont_time.time().strftime('%M'))
                  
                  file_names.append(file_name)
                  
                  cont_time = cont_time + \
                      timedelta(minutes=float(1))
              
              output = hour_folder_path + \
                  "{{{0}}}".format(str(file_names)[1:-1])
              
              files.append(output)
          
          # Store object per camera
          main_obj['date_tz'] = query_date.strftime('%Y-%m-%d')
          main_obj['camera'] = camera
          main_obj['files'] = files
          main_list.append(main_obj)

      # Write in json format
      with open(os.path.join(output_path, 'utc{utc_offset}.out'.format(utc_offset=key)), 'w') as output_file:
          json.dump(main_list, output_file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    generate_output_timezone_files()
    generate_output_timezone_camera_files()
    generate_output_timezone_camera_dict()
