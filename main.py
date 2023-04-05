import os
from PyPDF2 import PdfMerger, PdfReader
from datetime import datetime, timedelta


def run():
    USE = 'DEV'

    if USE == 'PROD':
        # gets yesterdays date
        today = datetime.today()
        ## manual testing date
        # str_date = '3/24/2023'
        # today = datetime.strptime(str_date, '%m/%d/%Y')
        delta = timedelta(days = -1)

        while True:
            date = today + delta
            print(date)
            if date.weekday() < 5:
                break
            delta -= timedelta(days = 1)

        # Gets the last business day
        if date.weekday() >= 5:
            date = date - datetime.timedelta(days = datetime.today().weekday() % 4 + 2)

        year = date.year
        month = datetime.strftime(date, format = '%m')
        # yesterdays date in MM_DD_YY format
        date_frmt = datetime.strftime(date, format = '%m_%d_%y')

        dated_path = f'M:/CPP-Data/Sutherland RPA/MedicalRecords/OC WCNF Records/{year}/{month} {year}/{date_frmt}/'
        dest_path = 'M:/CPP-Data/Sutherland RPA/MedicalRecords/OC WCNF Records/GOA Test/'

    elif USE == 'DEV':
        date = '03/29/2023'
        date = datetime.strptime(date, '%m/%d/%Y')
        year = date.year
        month = datetime.strftime(date, format = '%m')
        # yesterdays date in MM_DD_YY format
        date_frmt = datetime.strftime(date, format = '%m_%d_%y')

        dated_path = f'./GOA/{year}/{month} {year}/{date_frmt}/'
        dest_path = './GOA/'

    invoices = {}
    for filename in os.listdir(dated_path):
        if filename.endswith('.pdf'):
            invoice_number = filename.split('_')[0]
            if invoice_number not in invoices:
                invoices[invoice_number] = []
            invoices[invoice_number].append(os.path.join(dated_path, filename))

    for invoice_number, pdf_list in invoices.items():
        pdf_list = sorted(pdf_list)
        merger = PdfMerger()
        for pdf_file in pdf_list:
            with open(pdf_file, 'rb') as file:
                merger.append(file)
        path = dest_path + invoice_number + '.pdf'
        with open(path, 'wb') as output:
            merger.write(output)


if __name__ == '__main__':
    run()
