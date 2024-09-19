
import zipfile
import os
import shutil

anon_directory = r"C:/DicomData/UCLHRT/5_anon"

def zip_folder(folder_path, output_zip):
    """
    Zip a folder and its contents.

    Args:
    folder_path (str): The path to the folder you want to zip.
    output_zip (str): The name of the output ZIP file.

    Returns:
    None
    """
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))
                
anon_subfolder = os.listdir(anon_directory)
for sub in anon_subfolder:
    folder_to_zip = os.path.join(anon_directory, sub)
    output_zip_file = folder_to_zip + '.zip'
    zip_folder(folder_to_zip, output_zip_file)
    ### if you want to delete the original anonymised folder
#shutil.rmtree(directory)
print('Done')