# Project Selenium
Project Selenium is an automation type project. The goal was to create a script that would automate the download, modification of an XML file, and re-upload from and to TestLink, the Test Case platform used by Product Validation Companies. To achieve this, Selenium Webdriver Python API was used to automate the Download and Upload of the XML file, and Python was used to find and replace the information needed.

#Reading configfile
I set up a configuration file tha  would contain all parameters. When read, those parameters would be assigned variables
#Directory of Test Suite from Config
As previously said, the Directory I wish to download is found in the config file
#While loop
A while loop with the purpose of looping through all directories in the config file
#Checking all sub-diretories exist
Checking if all necesseray directories exist, and creating if they don't
#Defining Firefox Profile to bypass Download Dialog
Creating a FirefoxProfile so that a download dialog box will not appear and to set the /tmp directory as the download one
#Login into TestLink
Opening TestLink on Firefox with selenium
#Credentials
Reading Login credentials from config
#Exporting XML file of Test Suite from TestLink
Using selenium, the program navigates to the Export page and downloads the XML file
#Waiting for file Download
Checks if the file is present in /tmp and will wait for confimations by iusing a while loop set to 0 only changed by the presence of an XML file
#Parameters of Custom Fiels to change from Config
Reads the parameters to change from config, creates an array by splitting them
#File Modification
Reads and replaces the parameters in the XML file
#While loop
A while loop with the purpose of looping through all parameters in the config file
#sets XML file to be opened
Creates a new XML file1
#sets destination XML file
Sets the /Modified directory as the destination
#Upload of file
Checks in config if upload was set to False or True
#Importing XML file of Test Suite to TestLink
Using selenium, the program navigates to the Import page and uploads the new XML file
#Sorting files
Sorts the orginal file to /Original and the new one to /Modified , thus clearing /tmp for the next usage








Prerequisites
Python3
Selenium Python API
geckodriver Webdriver
configparser
fnmatch


Version
For the versions available, see the tags on this repository.

Authors
Tomas Nobre

License
This project is licensed under the MIT License - see the LICENSE.md file for details
