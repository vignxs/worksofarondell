# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 10:23:29 2022

@author: DK
"""


import boto3

from xml_parse import ICD
from icd_analyzer import ICDMatcher
from Extract import Extract
from ExtractMedicalInfo import ExtractMedicalInfo
from icd_transform import ICDTransform

bucket = "textract-console-ap-south-1-13d8bdf3-2ddb-471a-a8ca-3ea2325bd65"
document = "med.jpg"
region = "ap-south-1"
parsed_icd_code = None
parsed_icd_desc = None


def getS3Client():
    client = boto3.client('textract', 
                          region_name=region,
                          aws_access_key_id="AKIAWOINZBSCR2Q6ZMLQ", 
                          aws_secret_access_key="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")
    
    return client


def getResponse(client):
    response = client.analyze_document(
                Document={'S3Object': {'Bucket': bucket, 'Name': document}},
                FeatureTypes=["TABLES", "FORMS"])
    
    return response


def run():
    
    print("** Inside main run method ***")
    client = getS3Client()
    response = getResponse(client)

    extract = Extract(response)
    keyValuePairs , tableContents , lineContents = extract.extractContent()

    extractMedicalInfo = ExtractMedicalInfo(keyValuePairs , tableContents , lineContents)
    extractMedicalInfo.extract()

    parsed_icd_code = extractMedicalInfo._icd_code
    parsed_icd_desc = extractMedicalInfo._icd_desc

    parsed_icd_code = '111'
    parsed_icd_desc = None
    if not parsed_icd_desc and parsed_icd_code:
        # ICD Code is given/invalid and No ICD desc
        icdObj = ICD(parsed_icd_code)
        icdResponse = icdObj.run()
        print(icdResponse)
        if icdResponse.get('Response') == 'True':
            parsed_icd_code = icdResponse.get('Name')
            parsed_icd_desc = icdResponse.get('Description')
        if icdResponse.get('Response') == 'False' and icdObj._logger[0] == 'Invalid ICD code':
            icdObj2 = ICDTransform(parsed_icd_code)
            icdResponse2 = icdObj2.tranform_gen_icd()
            print(icdResponse2)
            if icdResponse2.get('Response') == 'True':
                parsed_icd_code = icdResponse2.get('Name')
                parsed_icd_desc = icdResponse2.get('Description')

    # Test code will be deleted later
    parsed_icd_code = '27.21'
    parsed_icd_desc = None
    if not parsed_icd_desc and parsed_icd_code:
        # ICD Code is given and No ICD desc
        icdObj = ICD(parsed_icd_code)
        icdResponse = icdObj.run()
        print(icdResponse)
        if icdResponse.get('Response') == 'True':
            parsed_icd_code = icdResponse.get('Name')
            parsed_icd_desc = icdResponse.get('Description')
        if icdResponse.get('Response') == 'False' and icdObj._logger[0] == 'Invalid ICD code':
            icdObj2 = ICDTransform(parsed_icd_code)
            icdResponse2 = icdObj2.tranform_gen_icd()
            print(icdResponse2)
            if icdResponse2.get('Response') == 'True':
                parsed_icd_code = icdResponse2.get('Name')
                parsed_icd_desc = icdResponse2.get('Description')

    parsed_icd_code = None
    parsed_icd_desc = 'ndary pulmonary arterial'
    if parsed_icd_desc and not parsed_icd_code:
        # ICD Desc is given and No ICD Code - Match >= 65%
        myobj = ICDMatcher(parsed_icd_desc)
        match_score, icd_key, icd_value = myobj.get_icd_data()
        print(match_score, icd_key, icd_value)
        if match_score:
            parsed_icd_code = icd_key
            parsed_icd_desc = icd_value

    parsed_icd_code = 'I27.21'
    parsed_icd_desc = ' nonspecific idiopathic pericardit'
    if parsed_icd_desc and parsed_icd_code:
        # ICD Code is given and ICD desc is given
        # Verify Match >= 80%
        # Else fetch ICD Code based on desc - match >= 65%
        icdObj = ICD(parsed_icd_code)
        icdResponse = icdObj.run()
        if icdResponse.get('Response') == 'True':
            myobj = ICDMatcher(parsed_icd_desc)
            match_score, icd_key, icd_value = myobj.get_icd_data()
            print(match_score, icd_key, icd_value)
            if match_score:
                parsed_icd_code = icd_key
                parsed_icd_desc = icd_value

    parsed_icd_code = 'I27.21'
    parsed_icd_desc = '  Secondary pulmonary arterial'
    if parsed_icd_desc and parsed_icd_code:
        # ICD Code is given and ICD desc is given
        # Verify Match >= 80%
        # Else fetch ICD Code based on desc - match >= 65%
        icdObj = ICD(parsed_icd_code)
        icdResponse = icdObj.run()
        if icdResponse.get('Response') == 'True':
            myobj = ICDMatcher(parsed_icd_desc)
            match_score, icd_key, icd_value = myobj.get_icd_data()
            print(match_score, icd_key, icd_value)
            if match_score:
                parsed_icd_code = icd_key
                parsed_icd_desc = icd_value


if __name__ == "__main__":
    
    run()
