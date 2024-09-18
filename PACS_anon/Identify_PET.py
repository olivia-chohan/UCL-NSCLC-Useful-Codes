# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:03:40 2024

@author: OLCHOHAN
"""

# Identify PET scans in folder of PACS downloads and label them

import os
import pydicom

def find_folders_with_series_description(parent_directory, target_description):
    matching_folders = []

    # Walk through the directory tree
    for root, dirs, files in os.walk(parent_directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Try to read the file as a DICOM file
                dicom_data = pydicom.dcmread(file_path, stop_before_pixels=True)
                # Check if the Series Description matches the target description
                if 'StudyDescription' in dicom_data and dicom_data.StudyDescription == target_description:
                    matching_folders.append(root)
                    break  # No need to check other files in the same folder
            except (pydicom.errors.InvalidDicomError, AttributeError):
                # Skip files that are not valid DICOM files or do not have the SeriesDescription attribute
                continue

    return matching_folders

def find_GE_medical_PET_scans(parent_directory, targer_manufacturer):
    matching_folders = []
    
    for dirName, subdirList, fileList in os.walk(parent_directory):
        if dirName.endswith('_PET'):
            for file in fileList:
                file_path = os.path.join(parent_directory, dirName, file)
                try:
                    dicom_data = pydicom.dcmread(file_path, stop_before_pixels=True)
                    if 'Manufacturer' in dicom_data and dicom_data.Manufacturer == target_manufacturer:
                        matching_folders.append(dirName)
                        break
                except (pydicom.errors.InvalidDicomError, AttributeError):
                    continue
                
    return matching_folders

# Define the parent directory and the target Series Description
parent_directory = r'C:\Users\OLCHOHAN\Documents\PACS_DATA\batch5\25'
target_description = 'NM WBDY FDG PET CT'  # Change this to the desired Series Description
target_manufacturer = "GE MEDICAL SYSTEMS"

# Find folders containing DICOM files with the specified Series Description
folders = find_folders_with_series_description(parent_directory, target_description)

# Print the results
if folders:
    print(f"Folders containing DICOM files with Study Description '{target_description}':")
    for folder in folders:
        print(folder)
        os.rename(folder, folder+'_PET')
else:
    print(f"No folders containing DICOM files with Study Description '{target_description}' were found.")

#print('GE Medical PET scans:')    
#more_folders = find_GE_medical_PET_scans(parent_directory, target_manufacturer)
#if more_folders:
#    for more_folder in more_folders:
#        print(more_folder)
#else:
#    print('Help')
    