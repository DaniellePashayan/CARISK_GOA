from main import *

if __name__ == '__main__':
    if os.path.exists("M:/"):
        for folder in ['M:\CPP-Data\Sutherland RPA\MedicalRecords\OC WCNF Records', 'M:\CPP-Data\Sutherland RPA\MedicalRecords\OC WCNF Manual Records']:
            print(f'Combining folder: {folder}')

            # to run normally, leave this line commented. to run manually, uncomment these lines
            year = '2024'
            month = '01'
            day = '17'
            short_year = year[2:]
            
            dated_path = f'{folder}/{year}/{month} {year}/{month}_{day}_{short_year}'
            date_frmt = f'{month}_{day}_{short_year}'
            date = f'{month}{day}{year}'
            
            if has_screenshots(dated_path):
                move_error_screenshots(dated_path)
            run(dated_path, date_frmt)
    else:
        print("NOT CONNECTED TO M DRIVE")