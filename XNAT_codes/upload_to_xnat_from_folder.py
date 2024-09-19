# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 12:23:49 2024

@author: OLCHOHAN
"""
# Upload directory of zipped folders with DICOM data to XNAT

import os
import xnat

basepath = r'C:\DicomData\UCLHRT\5_anon'

#session = xnat.connect('https://multimodal-ai.cs.ucl.ac.uk', user='user', password='password', detect_redirect=False)

scans = []

for dirName, subdirList, fileList in os.walk(basepath):
    for file in fileList:
        if file.endswith('.zip'):
            scans.append(str(os.path.join(dirName, file)))

# Check if this makes upload faster            
session = xnat.connect('https://multimodal-ai.cs.ucl.ac.uk', user='user', password='password', detect_redirect=False,
                       verify=False)# timeout=30)

for i in scans:
    prearchive_session = session.services.import_(i, project='UCLH_NSCLC', destination='/prearchive')


            
