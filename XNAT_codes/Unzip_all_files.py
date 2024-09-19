# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 11:01:57 2023

@author: OLCHOHAN
"""

import zipfile, os

working_directory = r'C:\Users\OLCHOHAN\Documents\PACS_DATA\batch5\25'
os.chdir(working_directory)

for file in os.listdir(working_directory):   # get the list of files
    if zipfile.is_zipfile(file): # if it is a zipfile, extract it
        with zipfile.ZipFile(file) as item: # treat the file as a zip
           item.extractall()  # extract it in the working directory
           #zipfile.close() # close file
           #os.remove(file) # delete zipped file
           
print('Done')