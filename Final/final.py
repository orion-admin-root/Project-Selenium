#!/usr/bin/env python3
#version 3.0
from fnmatch import fnmatch
import selenium, sys, time, os, fileinput, datetime, configparser, os.path, fnmatch, glob, re
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from glob import glob

#Reading configfile
config = configparser.ConfigParser()
config.read('config.ini')

#Directory of Test Suite from Config

directories = config['DEFAULT']['directory']
ndir = len(directories)
ndir = int(ndir)
directories= re.split('[|]',directories)
dircount = 0

while (dircount < ndir):

    #Checking all sub-diretories exist
    if not os.path.exists(os.getcwd() + "/tmp"):
        os.makedirs(os.getcwd() + "/tmp")
    if not os.path.exists(os.getcwd() + "/Original"):
        os.makedirs(os.getcwd() + "/Original")
    if not os.path.exists(os.getcwd() + "/Modified"):
        os.makedirs(os.getcwd() + "/Modified")
    directory = directories[dircount]
    #Defining Firefox Profile to bypass Download Dialog
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.dir", os.getcwd() + "/tmp")
    fp.set_preference("browser.preferences.instantApply",True)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain, application/octet-stream, application/binary, text/csv, application/csv, application/excel, text/comma-separated-values, text/xml, application/xml")
    fp.set_preference("browser.helperApps.alwaysAsk.force",False)
    fp.set_preference("browser.download.manager.showWhenStarting",False)
    browser = webdriver.Firefox(firefox_profile=fp)

    #Login into TestLink
    print("Accessing TestLink")
    browser.get("https://testlink.softathome.com/login.php")
    username = browser.find_element_by_name("tl_login")
    password = browser.find_element_by_name("tl_password")

    #Credentials
    username.send_keys("your_username")
    password.send_keys("your_password")
    browser.find_element_by_name("login_submit").click()

    #Exporting XML file of Test Suite from TestLink
    print("Downloading files")
    browser.get(directory)
    browser.switch_to.frame(browser.find_element_by_name("mainframe"))
    browser.switch_to.frame(browser.find_element_by_name("workframe"))
    browser.find_element_by_xpath('//*[@title="Actions"]').click()
    browser.find_element_by_xpath('//*[@title="Export"]').click()
    browser.find_element_by_name("export").click()

    #Waiting for file Download
    print("Awaiting download completion")
    fileexists = 0
    pattern = 'tmp/*.xml'
    while (fileexists < 1):
        if glob(pattern):
            fileexists = 1
            print("File downloaded")
        else:
            pass

    #Parameters of Custom Fiels to change from Config
    params = config['DEFAULT']['params']
    params = re.split('[|]',params)
    nparam = len(params)
    nparam = int(nparam)
    count = 0
    counter = 0

    #File Modification
    print("Modifying File")
    file = glob('tmp/*.xml')[0] #sets XML file to be opened
    fileout = '{}_new.xml'.format(os.path.splitext(file)[0]) #sets destination XML file
    f = open(file,'r')
    filedata = f.read()
    f.close()
    while (count < nparam):
        arg1 = params[counter]#raw_input('Enter first param: ')
        count = count + 1
        counter = counter + 1
        arg2 = params[counter]#raw_input('Enter second param: ')
        counter = counter + 1
        count = count + 1
        data = filedata.replace("<![CDATA[" + arg1 + "]]>", "<![CDATA[" + arg2 + "]]>") #Replacement of Custom Field
        data1 = data.replace("<![CDATA[" + arg1 + "|", "<![CDATA[" + arg2 + "|") #Replacement of Custom Field
        data2 = data1.replace("|" + arg1 + "|", "|" + arg2 + "|") #Replacement of Custom Field
        filedata = data2.replace("|" + arg1 + "]]>", "|" + arg2 + "]]>") #Replacement of Custom Field

    f = open(fileout,'w')
    f.write(filedata)
    f.close()

    #Upload of file
    upload = config['DEFAULT']['upload']
    if upload == "0":
        print("Files can be found under Original and Modified")
        t = time.localtime()
        timestamp = time.strftime('%b_%d_%Y_%H%M%S_', t)
        filenames = os.listdir("tmp/")
        os.rename(os.getcwd() + "/" + file, os.getcwd() + "/Original/" + filenames[0])
        os.rename(os.getcwd() + "/" + fileout, os.getcwd() + "/Modified/" + timestamp + filenames[1])
        dircount = dircount + 1
        browser.close()

    else:
        #Importing XML file of Test Suite to TestLink
        print("Uploading file")
        browser.find_element_by_name("cancel").click()
        browser.find_element_by_xpath('//*[@title="Actions"]').click()
        browser.find_element_by_xpath('//*[@title="Import"]').click()
        browser.find_element_by_xpath('//*[@name="uploadedFile"]').send_keys(os.getcwd()+"/" + fileout)
        select = Select(browser.find_element_by_id('hit_criteria'))
        select.select_by_visible_text('has same Internal ID')
        select = Select(browser.find_element_by_name('action_on_duplicated_name'))
        select.select_by_visible_text('Update data on Latest version')
        browser.find_element_by_name("UploadFile").click()
        browser.close()

        #Sorting files
        print("Files can be found under Original and Modified")
        t = time.localtime()
        timestamp = time.strftime('%b_%d_%Y_%H%M%S_', t)
        filenames = os.listdir("tmp/")
        os.rename(os.getcwd() + "/" + file, os.getcwd() + "/Original/" + filenames[0])
        os.rename(os.getcwd() + "/" + fileout, os.getcwd() + "/Modified/" + timestamp + filenames[1])
        dircount = dircount + 1
