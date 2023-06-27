import os
from pypdf import PdfMerger
from datetime import datetime, timedelta
import tqdm
import pandas as pd
import time


def run():
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

    dated_path = f'M:/CPP-Data/Sutherland RPA/MedicalRecords/OC WCNF Records/{year}/{month} {year}/{date_frmt}/'
    dest_path = 'M:/CPP-Data/Sutherland RPA/MedicalRecords/OC WCNF Records/GOA/'

    log_path = 'M:/CPP-Data/Sutherland RPA/MedicalRecords/OC WCNF Records/script logs/'

    if os.path.exists(dated_path):
        invoices = {}
        for filename in os.listdir(dated_path):
            if filename.endswith('.pdf'):
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
            for pdf in pdf_list:
                with open(pdf, 'rb') as file:
                    merger.append(file)
            path = f'{dest_path}/{invoice}.pdf'
            if not os.path.exists(path) and not entry['Saved']:
                with open(path, 'wb') as output:
                    merger.write(output)
            entry['Saved'] = True

        df = pd.DataFrame.from_dict(invoices, orient='index')
        df.to_excel(f'{log_path}/{date_frmt}.xlsx', index=None)

    else:
        print("Folder missing, retrying in 10 minutes")
        wait_time = 600  # 10 minutes
        for remaining in tqdm(range(wait_time, 0, -1), desc="Countdown", unit="s"):
            time.sleep(1)
        run()


if __name__ == '__main__':
    run()
