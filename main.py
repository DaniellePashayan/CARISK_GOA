import os
from pypdf import PdfMerger
from datetime import datetime, timedelta
import tqdm
import pandas as pd
import time


def get_file_count(folder_path: str) -> int:
    if os.path.exists(folder_path):
        files = [f for f in os.listdir(folder_path) if os.path.isfile(
            os.path.join(folder_path, f))]
        return len(files)
    else:
        return 0


def monitor_folder(folder_path: str, date_frmt: str, interval=60) -> None:
    prev_file_count = get_file_count(folder_path)
    if prev_file_count > 0:
        keep_checking = True
        time.sleep(interval)
    else:
        keep_checking = False

    while keep_checking:
        curr_file_count = get_file_count(folder_path)

        if curr_file_count > prev_file_count:
            print("New files detected")
            prev_file_count = curr_file_count
        else:
            print("No new files detected after 60 seconds")
            run(folder_path, date_frmt)
            keep_checking = False


def get_folder(folder_path) -> (str, str):
    today = datetime.today()
    delta = timedelta(days=-1)

    #
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
    return dated_path, date_frmt


def run(dated_path: str, date_frmt: str) -> None:
    dest_path = 'M:/CPP-Data/Sutherland RPA/MedicalRecords/OC WCNF Records/GOA/'
    log_path = 'M:/CPP-Data/Sutherland RPA/MedicalRecords/OC WCNF Records/script logs/'

    if os.path.exists(dated_path):
        print(dated_path)
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

        for invoice_key in tqdm.tqdm(invoices.keys()):
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


if __name__ == '__main__':
    for folder in ['M:\CPP-Data\Sutherland RPA\MedicalRecords\OC WCNF Records', 'M:\CPP-Data\Sutherland RPA\MedicalRecords\OC WCNF Manual Records']:
        print(f'Combining folder: {folder}')
        dated_path, date_frmt = get_folder(folder)
        # dated_path = f'{folder}/2023/08 2023/08_07_23/'
        # date_frmt = '08_07_23'
        monitor_folder(dated_path, date_frmt)
