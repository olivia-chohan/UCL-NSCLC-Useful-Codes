# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 17:31:39 2024

@author: OLCHOHAN
"""

import os
import pydicom
import numpy as np
import matplotlib.pyplot as plt
from pydicom.pixel_data_handlers.util import apply_voi_lut

def alter_pixels(dicom_file_path, left, top, right, bottom, value):
    """
    Alter pixels in a specified rectangular region of a DICOM image.

    Parameters:
    dicom_file_path (str): Path to the DICOM file.
    left (int): Left coordinate of the rectangle.
    top (int): Top coordinate of the rectangle.
    right (int): Right coordinate of the rectangle.
    bottom (int): Bottom coordinate of the rectangle.
    value (int): Value to set in the specified region.

    Returns:
    str: Path to the modified DICOM file.
    np.array: Modified pixel array.
    """
    try:
        # Read the DICOM file
        ds = pydicom.dcmread(dicom_file_path)

        # Check if the Manufacturer tag exists and matches 'GE MEDICAL SYSTEMS'
        if ds.Manufacturer == 'GE MEDICAL SYSTEMS' and str(ds.SeriesNumber).startswith('120'):
            # Decompress the pixel data if it's compressed
            if ds.file_meta.TransferSyntaxUID.is_compressed:
                ds.decompress()
            
            # Get the pixel array
            pixel_array = apply_voi_lut(ds.pixel_array, ds)
            
            # Modify the specified rectangular region
            pixel_array[top:bottom, left:right] = value
            
            # Update the pixel array in the DICOM dataset
            ds.PixelData = pixel_array.tobytes()
            
            # Save the modified DICOM file
            output_file_path = dicom_file_path.replace(".dcm", "_modified.dcm")
            ds.save_as(output_file_path)
            
            return output_file_path, pixel_array
        else:
            return None, None
    except Exception as e:
        print(f"Error processing file {dicom_file_path}: {e}")
        return None, None

def process_dicom_folder(folder_path, left, top, right, bottom, value):
    """
    Process all DICOM files in a folder and its subdirectories to alter pixels in a specified rectangular region.

    Parameters:
    folder_path (str): Path to the folder containing DICOM files.
    left (int): Left coordinate of the rectangle.
    top (int): Top coordinate of the rectangle.
    right (int): Right coordinate of the rectangle.
    bottom (int): Bottom coordinate of the rectangle.
    value (int): Value to set in the specified region.
    """
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith('.dcm'):
                dicom_file_path = os.path.join(root, filename)
                output_file_path, modified_pixel_array = alter_pixels(dicom_file_path, left, top, right, bottom, value)
                if output_file_path:
                    print(f"Modified DICOM file saved to {output_file_path}")

                    # Display the modified image (optional)
                    plt.imshow(modified_pixel_array, cmap=plt.cm.gray)
                    plt.title(f"Modified {filename}")
                    plt.axis('off')  # Hide axes for better visualization
                    plt.show()

                    # Delete the original file
                    os.remove(dicom_file_path)
                    print(f"Original DICOM file {dicom_file_path} deleted")

# Remove corner of PET scan containing patient data

folder_path = r'C:\Users\OLCHOHAN\Documents\PACS_DATA\batch5\25_anon\PET'
left = 250
top = 0
right = 512
bottom = 80
value = 100

process_dicom_folder(folder_path, left, top, right, bottom, value)
