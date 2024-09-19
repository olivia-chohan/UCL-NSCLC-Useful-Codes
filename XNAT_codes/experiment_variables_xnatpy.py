# Code to import clinical data from a csv file into XNAT
# This code matches clinical data to XNAT experiment (an RT course/image is an experiment)
# Can be multiple experiments per subject so this works well for RT-specific data

import xnat
import pandas as pd

# Read in csv with ID-column that matches XNAT experiment IDs (e.g. RT00001)
# Columns are clinical data columns
# Convert csv to dictionary 
data = pd.read_csv('path-to-csv')
data.set_index('ID', inplace=True)
dictionary = data.to_dict(orient = 'index')

# Connect to XNAT session
session = xnat.connect('https://multimodal-ai.cs.ucl.ac.uk/', user = 'admin', password = 'admin', detect_redirect = False)

project = session.projects['UCLH_NSCLC']

# Make list from index of csv
# When experiment value matches list item
# Use update to set custom variables

session_list = data.index.values.tolist()

for subject in project.subjects.values():
	for experiment in subject.experiments.values():
		#print(experiment.fields)
		for item in session_list:
			if experiment.label == item
				#print(dictionary[item])
				dictionary2 = experiment.fields
				dictionary2.update(dictionary[item])