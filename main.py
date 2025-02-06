import os
from datetime import datetime, timedelta
from tqdm import tqdm
import pandas as pd
import time
import shutil
from glob import glob
from loguru import logger
from pathlib import Path
import pymupdf
from orcca.status_handler import JSONStatus

# get yesterdays date
def get_last_business_day(date: datetime | str | None = None) -> datetime:
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            logger.error(f"Invalid date format, date must be in the format YYYY-MM-DD")
            raise ValueError
    elif date is None:
        date = datetime.today()
    delta = timedelta(days=-1)

    while True:
        date_new = date + delta
        # check if date is a weekday
        if date_new.weekday() < 5:
            break
        delta -= timedelta(days=1)
    return date_new 

class RootFolder():
    def __init__(self, folder_date: datetime):
        self.folder_date = folder_date
        self.setup_logger()
        self.audit_path = Path(r'\\NT2KWB972SRV03\SHAREDATA\CPP-Data\Sutherland RPA\MedicalRecords\OC WCNF Records\script logs')
        self.source_directory = Path(r'\\NT2KWB972SRV03\SHAREDATA\CPP-Data\Sutherland RPA\MedicalRecords\OC WCNF Records')
        self.destination = Path(r'\\NT2KWB972SRV03\SHAREDATA\CPP-Data\Sutherland RPA\MedicalRecords\OC WCNF Records\GOA')
        self.yearly_folder = self.source_directory / folder_date.strftime('%Y')
        self.monthly_folder = self.yearly_folder / folder_date.strftime('%m %Y')
        self.daily_folder = self.monthly_folder / folder_date.strftime('%m_%d_%y')

        self.file_names = self.get_file_names()
        self.invoices = self.get_invoice_list()
        self.records_per_invoice = self.get_records_per_invoice()
    
    def setup_logger(self):
        logger.add(f'./logs/log_{last_business_date.strftime("%m_%d_%y")}.log', rotation='1 day', retention='7 days', level='INFO')
    
    def get_file_names(self) -> list:
        files = os.listdir(self.daily_folder)
        logger.success(f"Found {len(files)} files in {self.daily_folder}")
        return files

    def get_invoice_list(self) -> set:
        invoice_list = set([file.split('_')[0] for file in self.file_names])
        # replace ".pdf.pdf" with ".pdf"
        invoice_list = {invoice.replace('.pdf.pdf', '.pdf') for invoice in invoice_list}
        logger.success(f"Found {len(invoice_list)} unique invoices in {self.daily_folder}")
        return invoice_list
        
    
    def get_records_per_invoice(self) -> dict:
        invoice_records = {}
        for invoice in self.invoices:
            invoice_records[invoice] = {
                'Files': [self.daily_folder / file for file in self.file_names if invoice in file],
                'File Count': len([file for file in self.file_names if invoice in file]),
                'Original Page Count': sum([pymupdf.open(os.path.join(self.daily_folder, file)).page_count for file in self.file_names if invoice in file]),
                'New Page Count': 0,
                'Saved': False
            }
        return invoice_records
    
    def combine_pdfs(self):
        for invoice, data in tqdm(self.records_per_invoice.items()):
            files = sorted(data['Files'])
            if len(data['Files']) > 1:
                try:
                    merger = PdfMerger()
                    for file in files:
                        merger.append(file)
                    if not os.path.exists(self.destination / f"{invoice}.pdf"):
                        merger.write(self.destination / f"{invoice}.pdf")
                        merger.close()
                        data['Saved'] = True
                except Exception as e:
                    logger.error(f"Error combining PDFs for invoice {invoice}: {e}")
            else:
                shutil.copy(files[0], self.destination / f"{invoice}.pdf")
                data['Saved'] = True
            data['New Page Count'] = pymupdf.open(self.destination / f"{invoice}.pdf").page_count
            if data['Original Page Count'] != data['New Page Count']:
                logger.critical(f"PDF IS MISSING PAGES{invoice}")
        logger.success(f"PDFs combined and saved to {self.destination}")
    
    def update_audit_log(self):
        audit_file = self.audit_path / f'{self.folder_date.strftime("%m_%d_%y")}.xlsx'
        
        df = pd.DataFrame.from_dict(self.records_per_invoice, orient='index').reset_index().rename(columns={'index': 'Invoice'})
        df['Page Count Match'] = df['Original Page Count'] == df['New Page Count']
        
        # check if any rows have Page Count Match as False
        if not df['Page Count Match'].all():
            status.update_status("Failed", errors="Page Count Mismatch")
        else:
            status.update_status("Completed")
        
        df.to_excel(audit_file, index=False)
        logger.success(f"Audit log updated: {audit_file}")
        return df

if __name__ == '__main__':
    status = JSONStatus(r"\\NT2KWB972SRV03\SHAREDATA\CPP-Data\CBO Westbury Managers\LEADERSHIP\Bot Folder\Automated Scripts Status.json","Carisk GOA")
    status.update_status("Running")

    last_business_date = get_last_business_day()
    
    folder = RootFolder(last_business_date)
    folder.combine_pdfs()
    df = folder.update_audit_log()
    logger.info(f"Script completed successfully for {last_business_date.strftime('%m_%d_%y')}")