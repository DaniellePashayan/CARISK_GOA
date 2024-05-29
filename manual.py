from main import *

if __name__ == '__main__':
    year = 24
    month = 5
    day = 24
    for folder in [r'M:\CPP-Data\Sutherland RPA\MedicalRecords\OC WCNF Records', r'M:\CPP-Data\Sutherland RPA\MedicalRecords\OC WCNF Manual Records']:
        date_frmt = f'{str(month).zfill(2)}_{str(day).zfill(2)}_{str(year)}'
        dated_path = rf'{folder}\20{str(year)}\{str(month).zfill(2)} 20{str(year)}\{date_frmt}'
        print(f'Combining folder: {dated_path}')
        if has_screenshots(dated_path):
            move_error_screenshots(dated_path)
        monitor_folder(dated_path, date_frmt)