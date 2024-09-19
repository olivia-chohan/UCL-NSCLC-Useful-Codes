# Code to import clinical data from a csv file into XNAT
# This code matches clinical data to XNAT subject

import xnat
import pandas as pd

# Read in csv with ID-column that matches XNAT subject IDs
# Columns are clinical data columns
# Convert csv to dictionary 
data = pd.read_csv('path-to-csv')
data.set_index('ID', inplace=True)
dictionary = data.to_dict(orient = 'index')

# Connect to XNAT session
session = xnat.connect('https://multimodal-ai.cs.ucl.ac.uk/', user = 'admin', password = 'admin', detect_redirect = False)

project = session.projects['UCLH_NSCLC']

# Make subject list from ID-column in csv
subject_list = data.index.values.tolist()

# Upload dictionary to XNAT project
# data matched to XNAT subject when item from subject list matches XNAT subject
for subject in project.subjects.values():
	for item in subject_list:
		if int(subject.label) == item:
			dictionary2 = subject.fields
			dictionary2.update(dictionary[item])

