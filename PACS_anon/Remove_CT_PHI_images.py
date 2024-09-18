# -*- coding: utf-8 -*-
"""
Created on Thu May 23 16:52:37 2024

@author: OLCHOHAN
"""

# Code to remove CT series with PHI 
# Delete images with series number 999 for GE Medical Systems CT
# Delete images with series number 9000 for Toshiba CT

#import matplotlib.pyplot as plt
import os 
import pydicom

basepath = r'C:\Users\OLCHOHAN\Documents\PACS_DATA\batch5\25'

for dirName, subdirList, fileList in os.walk(basepath):
    for file in fileList:
        if file.endswith('.dcm'):
            ds = pydicom.dcmread(os.path.join(basepath, dirName, file), stop_before_pixels=True, force=True)
            
            if 'Manufacturer' in ds and ds.Manufacturer == 'GE MEDICAL SYSTEMS' and ds.SeriesNumber == 999:
                    os.remove(os.path.join(basepath, dirName, file))
                    print('Removed')
            
            
            if 'Manufacturer' in ds and ds.Manufacturer == 'TOSHIBA' and ds.SeriesNumber == 9000: 
                os.remove(os.path.join(basepath, dirName, file))
                print('Removed')


