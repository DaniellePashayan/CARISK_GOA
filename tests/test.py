import datetime as dt
import os
from PyPDF2 import PdfMerger

TEST_PDF_LOC = os.path.abspath('./test_data/OC WCNF Records/2023/05 2023/05_01_23/')
TEST_GOA_LOC = os.path.abspath('./test_data/OC WCNF Records/GOA/')

class Test_Business_Days:
    def test_get_last_business_day_M(self):
        today = dt.datetime(2023,5,1,0,0,0,0)
        delta = dt.timedelta(days=-1)
        while True:
            date = today + delta
            if date.weekday() < 5:
                break
            delta -= dt.timedelta(days=1)
        
        if date.weekday() >= 5:
            date = date - dt.timedelta(days = today.weekday() % 4 + 2)
        assert date == dt.datetime(2023,4,28,0,0,0,0)
        
    def test_get_last_business_day_T(self):
        today = dt.datetime(2023,5,2,0,0,0,0)
        delta = dt.timedelta(days=-1)
        while True:
            date = today + delta
            if date.weekday() < 5:
                break
            delta -= dt.timedelta(days=1)
        
        if date.weekday() >= 5:
            date = date - dt.timedelta(days = today.weekday() % 4 + 2)
        assert date == dt.datetime(2023,5,1,0,0,0,0)
        
    def test_get_last_business_day_W(self):
        today = dt.datetime(2023,5,3,0,0,0,0)
        delta = dt.timedelta(days=-1)
        while True:
            date = today + delta
            if date.weekday() < 5:
                break
            delta -= dt.timedelta(days=1)
        
        if date.weekday() >= 5:
            date = date - dt.timedelta(days = today.weekday() % 4 + 2)
        assert date == dt.datetime(2023,5,2,0,0,0,0)
        
    def test_get_last_business_day_Th(self):
        today = dt.datetime(2023,5,4,0,0,0,0)
        delta = dt.timedelta(days=-1)
        while True:
            date = today + delta
            if date.weekday() < 5:
                break
            delta -= dt.timedelta(days=1)
        
        if date.weekday() >= 5:
            date = date - dt.timedelta(days = today.weekday() % 4 + 2)
        assert date == dt.datetime(2023,5,3,0,0,0,0)
        
    def test_get_last_business_day_F(self):
        today = dt.datetime(2023,5,5,0,0,0,0)
        delta = dt.timedelta(days=-1)
        while True:
            date = today + delta
            if date.weekday() < 5:
                break
            delta -= dt.timedelta(days=1)
        
        if date.weekday() >= 5:
            date = date - dt.timedelta(days = today.weekday() % 4 + 2)
        assert date == dt.datetime(2023,5,4,0,0,0,0)
        

class Test_File_Retrieval:
    def test_get_file_count(self):
        inv_count = os.listdir(TEST_PDF_LOC)
        assert len(inv_count) == 320
    
    def test_get_invoice_count(self):
        invoices = {filename.split('_')[0] for filename in os.listdir(TEST_PDF_LOC) if filename.endswith('.pdf')}
        assert len(invoices) == 56
                
    def test_invoice_number_extraction(self):
        invoices = {filename.split('_')[0] for filename in os.listdir(TEST_PDF_LOC) if filename.endswith('.pdf')}
        assert invoices == {'220635405', '681815165', '919581930', '16934186', '770448732', '636831435', '419288227', '963342039', '538604849', '61262679', '877276393', '85972630', '88777314', '575465850', '478134664', '105226025', '13270492', '696976054', '862201540', '974822550', '698551313', '652682533', '237574448', '241524932', '60757172', '170350887', '466736616', '150918655', '576149723', '765024459', '198648939', '359173701', '124564096', '994548329', '785398976', '658322709', '857704874', '380744630', '778000303', '181244577', '481816229', '672765816', '254380512', '872407298', '231553546', '879355680', '31667186', '816805332', '348226009', '53285766', '130622358', '434180231', '289676842', '20398791', '526536042', '922896864'}


class Test_File_Combine:
    def test_file_combine(self):
        if len(os.listdir(TEST_GOA_LOC)) > 0:
            for file in os.listdir(TEST_GOA_LOC):
                os.remove(file) 

                
        invoices = {}
        for filename in os.listdir(TEST_PDF_LOC):
            if filename.endswith('.pdf'):
                invoice_number = filename.split('_')[0]
                if invoice_number not in invoices:
                    invoices[invoice_number] = []
                invoices[invoice_number].append(os.path.join(TEST_PDF_LOC, filename))

        for invoice_number, pdf_list in (invoices.items()):
            pdf_list = sorted(pdf_list)
            merger = PdfMerger()
            for pdf_file in pdf_list:
                with open(pdf_file, 'rb') as file:
                    merger.append(file)
            path = f'{TEST_GOA_LOC}/{invoice_number}.pdf'
            with open(path, 'wb') as output:
                merger.write(output)
                    
        assert len(os.listdir(TEST_GOA_LOC)) == 56
