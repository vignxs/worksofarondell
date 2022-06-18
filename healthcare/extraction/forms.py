import boto3
from trp import Document

# Document
documentName = "C:/Users/hrint/Documents/Python2022/healthcare/extraction/Referral_Form_page-0001.jpg"

# Amazon Textract client
textract = boto3.client('textract')

# Call Amazon Textract
with open(documentName, "rb") as document:
    response = textract.analyze_document(
        Document={
            'Bytes': document.read(),
        },
        FeatureTypes=["FORMS"])

#print(response)

doc = Document(response)

# for page in doc.pages:
#     # Print fields
#     print("Fields:")
#     for field in page.form.fields:
#         print("Key: {}, Value: {}".format(field.key, field.value))

print(dir(doc.pages[0].form))

from tabulate import tabulate
print(tabulate([x[1:3] for x in doc.pages[0].content]))