from datetime import datetime
import os
from tqdm import tqdm

def cleanup_archive_folder(dir_path="M:/CPP-Data/Sutherland RPA/MedicalRecords/OC WCNF Records/GOA Archive"):
    # get a list of files in teh folder
    files = os.listdir(dir_path)
    files = [file for file in files if os.path.isfile(f'{dir_path}/{file}')]
    for file in tqdm(files):
        # get the modified date of the file
        modified_date = os.path.getmtime(f'{dir_path}/{file}')
        # convert modified date in datetime format
        modified_date = datetime.fromtimestamp(modified_date)
        folder_format = f'{modified_date.year}/{str(modified_date.month).zfill(2)} {modified_date.year}/{modified_date.month}_{modified_date.day}_{str(modified_date.year)[2:]}'
        # make a folder for the year, month, and day
        os.makedirs(f'{dir_path}/{folder_format}', exist_ok=True)
        os.rename(f'{dir_path}/{file}', f'{dir_path}/{folder_format}/{file}')

if __name__ == "__main__":
    cleanup_archive_folder()