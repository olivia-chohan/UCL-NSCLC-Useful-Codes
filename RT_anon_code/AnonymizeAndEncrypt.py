# Read in unanonymised dicom file
# Read in NHS number (Other patient ID tag, (0010,1000))
# Encrypt NHS number
# Set encrypted NHS number as patient ID tag (0010,0020)
# Delete other patient ID tag

import pydicom
from pydicom import dcmread
import os, glob
from pathlib import Path
#import tempfile

import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import sys,binascii
import tqdm

from simpledicomanonymizer import *

def encrypt(key, source, encode=True):
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV =  b"1234567891234567"#Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    return data.hex()

def decrypt(key, source, decode=True):
    if decode:
        source =  binascii.unhexlify(source)
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return data[:-padding]  # remove the padding


password = "find this on NHS computer"
password = password.encode()

dataset_directory = sys.argv[1]
if(dataset_directory[-1]=="/"): dataset_directory = dataset_directory[:-1]
anon_directory    = dataset_directory+"_anon"


os.makedirs(anon_directory, exist_ok=True)
patientlist = os.listdir(dataset_directory)
progress_bar = tqdm.tqdm(total=len(patientlist))
for patient_folder in patientlist:
    print("Anonymizing", patient_folder)
    encrypted = False
    encrypted_id = None
    progress_bar.update(1)    
    for root, dirs, files in os.walk(os.path.join(sys.argv[1], patient_folder), topdown=True):
        print(root,dirs)
        for filename in files: ## assume files are only dcm
            ds = pydicom.read_file(os.path.join(root,filename))
            ds = anonymize_dicom_file(ds,  keep_private_tags=False)
            ds.PatientID = encrypt(password, ds.OtherPatientIDs.encode())
            ds.OtherPatientIDs = None   
            
            directory = root.replace(dataset_directory, anon_directory)
            os.makedirs(directory, exist_ok=True)
            pydicom.write_file(os.path.join(directory,filename), ds)
    encrypted=False
    progress_bar.close()
        
print('Done')
