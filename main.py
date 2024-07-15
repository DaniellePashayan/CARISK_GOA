import os
from PyPDF2 import PdfMerger
from datetime import datetime, timedelta
from tqdm import tqdm
import pandas as pd
import time
import shutil
from glob import glob
from loguru import logger


def get_folder(folder_path) -> tuple[str,str]:
    today = datetime.today()
    delta = timedelta(days=-1)
    logger.info(f'Getting folder for {folder_path}')

    while True:
        date = today + delta
        if date.weekday() < 5:
            break
        delta -= timedelta(days=1)

    # Gets the last business day
    if date.weekday() >= 5:
        date = date - \
            datetime.timedelta(days=datetime.today().weekday() % 4 + 2)

    year = date.year
    month = datetime.strftime(date, '%m')
    # yesterday's date in MM_DD_YY format
    date_frmt = datetime.strftime(date, '%m_%d_%y')

    dated_path = f'{folder_path}/{year}/{month} {year}/{date_frmt}/'
    date = datetime.strftime(date, '%m%d%Y')
    logger.info(f'Folder: {dated_path}')

    # returns:
    # M:\CPP-Data\Sutherland RPA\MedicalRecords\OC WCNF Records\2023\10 2023\10_27_23
    # 10_27_23
    # 10272023
    return dated_path, date_frmt, date


def get_file_count(folder_path: str) -> int:
    if os.path.exists(folder_path):
        files = [f for f in os.listdir(folder_path) if os.path.isfile(
            os.path.join(folder_path, f))]
        return len(files)
    else:
        return 0


def has_screenshots(folder_path: str) -> bool:
    if os.path.exists(folder_path):
        file_list = os.listdir(folder_path)
        # check if any files end in png
        for file in file_list:
            if file.endswith('.png'):
                return True
            else:
                return False


def monitor_folder(folder_path: str, date_frmt: str, interval=60) -> None:
    logger.info(f'Monitoring {folder_path} for new files')
    prev_file_count = get_file_count(folder_path)
    if prev_file_count > 0:
        keep_checking = True
        for remaining in tqdm(range(interval), desc="Countdown", unit="sec"):
            time.sleep(1)  # Pause for 1 second
    else:
        keep_checking = False

    while keep_checking:
        curr_file_count = get_file_count(folder_path)

        if curr_file_count > prev_file_count:
            logger.warning("New files detected")
            prev_file_count = curr_file_count
        else:
            logger.success("No new files detected after 60 seconds")
            run(folder_path, date_frmt)
            keep_checking = False


def move_error_screenshots(dated_path):
    logger.info(f'Moving error screenshots to error folder')
    error_path = f'{dated_path}/error screenshots'

    if os.path.exists(dated_path):
        if not os.path.exists(error_path):
            os.mkdir(error_path)
        for filename in os.listdir(dated_path):
            if filename.endswith('.png'):
                shutil.move(f'{dated_path}/{filename}', error_path)
    logger.success(f'Error screenshots moved to {error_path}')


def run(dated_path: str, date_frmt: str) -> None:
    os.makedirs('./logs', exist_ok=True)
    logger.add(f'./logs/log_{time}.log', rotation='1 day', retention='7 days', level='INFO')
    dest_path = 'M:/CPP-Data/Sutherland RPA/MedicalRecords/OC WCNF Records/GOA/'
    log_path = 'M:/CPP-Data/Sutherland RPA/MedicalRecords/OC WCNF Records/script logs/'

    # date = pd.to_datetime(date_frmt, format="%m_%d_%y").strftime('%m%d%Y')
    logger.info(f'Processing {date_frmt} folder')

    logger.debug(dated_path)
    if os.path.exists(dated_path):
        # df = read_input_file(date)
        # df = df['INVNUM'].astype(str).tolist()
        invoices = {}
        for filename in os.listdir(dated_path):
            if filename.endswith('.pdf'):

                # if filename contains a dash, replace it with an underscore
                if '-' in filename:
                    # rename the file, replacing the dash with udnerscroe
                    os.rename(os.path.join(dated_path, filename), os.path.join(
                        dated_path, filename.replace('-', '_')))
                    filename = filename.replace('-', '_')

                invoice_number = filename.split('_')[0]
                # if invoice_number in df:
                if invoice_number not in invoices:
                    invoices[invoice_number] = {
                        'Invoice': invoice_number,
                        'Files': [],
                        'File Count': 0,
                        'Saved': False
                    }
                    invoices[invoice_number]['Files'].append(
                        os.path.join(dated_path, filename))
                    invoices[invoice_number]['File Count'] += 1

        for invoice_key in tqdm(invoices.keys()):
            entry = invoices[invoice_key]
            invoice = entry['Invoice']
            pdf_list = sorted(entry['Files'])
            merger = PdfMerger()
            try:
                for pdf in pdf_list:
                    with open(pdf, 'rb') as file:
                        merger.append(file)
                path = f'{dest_path}/{invoice}.pdf'
                if not os.path.exists(path) and not entry['Saved']:
                    with open(path, 'wb') as output:
                        merger.write(output)
                entry['Saved'] = True
            except Exception as e:
                print(f'{invoice}/{pdf} has error: {e}')

        df = pd.DataFrame.from_dict(invoices, orient='index')
        df.to_excel(f'{log_path}/{date_frmt}.xlsx', index=None)

    else:
        print("Folder missing")
        logger.warning(f'{dated_path} is missing')


def read_input_file(date: str) -> pd.DataFrame:
    path = r'M:\CPP-Data\Sutherland RPA\Northwell Process Automation ETM Files\OC AllScripts'
    file = glob(f'{path}/*_{date}_OnC.xls')
    df = pd.read_excel(file[0])
    return df


if __name__ == '__main__':
    if os.path.exists("M:/"):

        for folder in ['M:/CPP-Data/Sutherland RPA/MedicalRecords/OC WCNF Records', 'M:/CPP-Data/Sutherland RPA/MedicalRecords/OC WCNF Manual Records']:
            print(f'Combining folder: {folder}')
            # to run normally, leave this line uncommented. to run manually, comment out this line
            dated_path, date_frmt, date = get_folder(folder)
            
            if has_screenshots(dated_path):
                move_error_screenshots(dated_path)
            run(dated_path, date_frmt)
    else:
        print("NOT CONNECTED TO M DRIVE")
