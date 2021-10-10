# Take-Home coding challenge solution
***
This is the solution for take home coding challenge from cainthus.

## Algorithm explained
***
The algorithm is simple. It involves the following steps.
### Storing
1. Sort the directories with Camera number, Date and Hour.
2. Once the sorted files are given it reads the files for each folder.
3. Extracts the date of each file and extracts the camera number also.
4. Converts the date in local timezone.
5. Stores in a ordered map with key as local timezone and value as list of sorted hours with filename in that date.
6. As the files are sorted with camera number also so all camera files will be automatically grouped.
7. For the section Confusion and Solution it stores local timezone date and another ordereddict of camera to store files.
### Getting start date and end date
1. As the files were sorted and stored in OrderedDict. So the first and last key will return the start and end date.
### Getting the files by local timezone date
1. Every date has list of hours folders with sorted files (camera wise) so it returns the value in one operation.
### Getting files by local timezone in camera dictionaries
1. It will loop over all the cameras in date for formatting. 
### 
## Complexities
***
### Time complexities
1. Sorting complexing will be O(nlogn).
2. Looping over all files in directories will be O(nm).
3. Inserting in date will be O(1)
4. Getting start and end date will be first and last index of dictionary keys should take O(1).
5. Getting files by timezone will O(1)
6. Getting files by timezone in camera dictionary will have O(n) where n is number of Cameras.

## How to run
***
In order to run the code go to directory cainthus/tests.
Running the command python test_local_file_conversion.py will run the simple tests. There are multiple enviornment variables that can be set to make tests more personal for users testing preferences.
### Enviornment variables
1. FOLDER_PATH
2. ERROR_PATH
3. NEW_PATH
4. TEST_LOCAL_ONLY

#### 1. FOLDER_PATH
Folder path variable will read a path and update the existing folder path in test class. The folder path variable can be passed through the following command.
FOLDER_PATH=your_folder_path python test_local_file_conversion.py

#### 2. ERROR_PATH
Error path variable is to test what happened when the incorrect path is given to system. The error path variable can be passed through following command.
ERROR_PATH=error_folder_path python test_local_file_conversion.py

#### 3. NEW_PATH
New path variable is to test the updation of the path. The new path variable can be passed as below
NEW_PATH=error_folder_path python test_local_file_conversion.py

#### 4. TEST_LOCAL_ONLY
The tests that depend on timezones are written to be tested in 2 ways
1. Test for local timezone
2. Test for all the timezones
##### 1. Run tests for local timezone
Run all the tests for local timezone. The tests can be run with following command
TEST_LOCAL_ONLY=True python test_local_file_conversion.py
###### Output
Output of this kind of result will be shown in 'logs/test_local_timezone.log' file.
##### 2. Run tests for all timezone
This test loops over GMT-12 to GMT+14 and tests the results for each timezone. This kind of test can be run through following command.
TEST_LOCAL_ONLY=True python test_local_file_conversion.py
###### Output
Output of this kind of result will be shown in 'logs/test_all_timezones.log file.

##### Exceptions for all time zone tests
A map is created for the timezones where all the timezones don't have day light saving. But there are 3 exceptions
1. UTC+12.45
2. UTC+10.30
3. UTC-3:30

All the above UTC don't have any zone without day light saving. So files generated for the output for these UTC have been adjusted accordingly.
## Helping Scripts
***
The tests explained in previous section are tested against the automated scripts. These scripts are included in the directory helping_scripts. These scripts generate the files in the folder 'output' with utc offset.
* Note: There are some folders with different files like some have 4 or 6 files so the output files are adjusted according to that manually. If the scripts are run again the output files needed to be adjusted other wise some of the tests will fail. In future I wanted to add script to automatically adjust those output files.

## Confusion and Solution
There was some confusion in grouping the files camera wise as no sample was provided. So there were 2 possibilites
1. Files sorted in same list with each camera folders are shown togather.
2. As the return was list of dict so each camera can be returned in its own dict
### Solution
Both of these solutions were implemented to get rid of the solution. While implementing second solution another functionality was added in the class that files can be retrieved by timezone and camera.