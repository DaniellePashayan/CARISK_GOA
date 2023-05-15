import os
import random
from PyPDF2 import PdfWriter
from pathlib import Path

# constants
MIN_INVOICE_NUM = 10000000
MAX_INVOICE_NUM = 999999999

MIN_FILES_PER_INVOICE = 1
MAX_FILES_PER_INVOICE = 10

OUTPUT_DIRECTORY = os.path.abspath('tests/test_data/OC WCNF Records/2023/05 2023/05_01_23/')

# Create the output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)
    
def create_empty_pdf(invoice_number, file_index):
    filename = f'{invoice_number}_{file_index}.pdf'
    filepath = os.path.join(OUTPUT_DIRECTORY, filename)
    
    # create empty PDF file using reportlab
    pdf_writer = PdfWriter()
    pdf_writer.add_blank_page(100,100) 
    with Path(filepath).open(mode='wb') as output_file:
        pdf_writer.write(output_file)
    

def generate_random_invoice_number():
    random_invoice_number = random.randint(MIN_INVOICE_NUM, MAX_INVOICE_NUM)
    # print(random_invoice_number)
    return random_invoice_number

def generate_pdfs(num_pdfs):
    for _ in range(num_pdfs):
        num_files = random.randint(MIN_FILES_PER_INVOICE, MAX_FILES_PER_INVOICE)
        inv_num = generate_random_invoice_number()
        for file_index in range(1, num_files+1):
            create_empty_pdf(inv_num, file_index)

generate_pdfs(50)