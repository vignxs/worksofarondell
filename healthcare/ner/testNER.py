from PyPDF2 import PdfFileReader
import json
import fitz

infile = r"C:\\Users\\hrint\\Documents\\Python2022\\healthcare\\samples\\Referral_Form.pdf"
# pdf_reader = PdfFileReader(open(infile, "rb"))

# dictionary = pdf_reader.getFormTextFields() # returns a python dictionary

# json_data=json.dumps(dictionary) # returns field name and field value in Key-Value pairs of JSON Format
# print(json_data)

# doc = fitz.open(infile) 
# f = open('test.json', 'w')
# for page in doc:

#     print(page.get_text('dict'))
#     data = str(page.get_text('dict'))
#     f.write(data)

x = 'vignesh'
y = 'vignesh'


name = f'name : {x}'
