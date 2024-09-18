# Code to remove nested/private tags containing patient street adress from RP files
# This will overwrite existing RP files in base folder

import os 
import pydicom

basepath = r'C:\DicomData/UCLHRT_anon'

for dirName, subdirList, fileList in os.walk(basepath):
    for file in fileList:
        if file.endswith('.dcm'):
            ds = pydicom.dcmread(os.path.join(basepath, dirName, file))
            if ds.Modality == 'RTPLAN':
                for n in range(len(ds.BeamSequence)):
                    ds.BeamSequence[n].InstitutionName = None
                    ds.BeamSequence[n].InstitutionalDepartmentName = None
                    ds.BeamSequence[n].ManufacturerModelName = None
                    ds.BeamSequence[n].DeviceSerialNumber = None

                for p in range(len(ds.PatientSetupSequence)):
                    ds.PatientSetupSequence[p].SetupTechniqueDescription = None
            
                    ds.save_as(os.path.join(basepath, dirName, file))

            print(file)

                        