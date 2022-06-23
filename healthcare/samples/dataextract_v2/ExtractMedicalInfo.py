# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 10:46:50 2022

@author: DK
"""


class ExtractMedicalInfo(object):

   

    def __init__(self, keyValuePairs , tableContents , lineContents):
        
        self._keyValuePairs = keyValuePairs
        self._tableContents = tableContents
        self._lineContents = lineContents
        
        self._patientName = ""
        self._patientDOB = None
        self._patientMRN = None
        self._patientGender = None
        
        self._patientAddress = None
        self._patientPhone = None
        self._patientCity = None
        self._patientStZip = None
        self._patientState = None
        
        self._refToName = ""
        self._refToDate = None
        self._refToAddress = None
        self._refToCity = None
        self._refToPhone = None
        self._refToFax = None 
        self._refToStZip = None
        self._refToState = None

        self._refByName = ""
        self._refByAddress = None
        self._refByCity = None
        self._refByZip = None
        self._refByPhone = None
        self._refByFax = None
        self._refByState = None
         
        self._refReason = None
        self._diagnosis = None
        self._icd_code = None
        self._icd_desc = None
        
    def extract(self):
        
        self.extractDefaultKeyValuePairs()
        
        self.extractInfoFromTable()
        
        self.extractMissingPatientInfoByLine()
        
        self.extractMissingReferalToInfoByLine()
        
        self.extractMissingReferalByInfoByLine()
        
            
        print("-----------------------")
        print("Patient Name :" ,self._patientName ,'\n',
              "Patient DOB :" , self._patientDOB ,'\n',
              "Patient MRN :" ,self._patientMRN ,'\n',
              "Patient Gender :" , self._patientGender ,'\n',
              "Patient Address: " ,self._patientAddress ,'\n',
              "Patient Phone : " ,self._patientPhone ,'\n',
              "Patient City : " ,  self._patientCity ,'\n',
              "Patient State Zip", self._patientStZip , '\n',
              "Patient State", self._patientState , '\n',
              "Rfereal To Name: " , self._refToName, '\n' , 
              "Ref To Date :" , self._refToDate , '\n' , 
              "Ref To Address :" , self._refToAddress , '\n',
              "Ref To City:" , self._refToCity , '\n', 
              "Ref To St Zip" , self._refToStZip , '\n' ,
              "Ref State", self._refToState , '\n',
              "Ref To Phone:" , self._refToPhone , '\n',
              "Ref To Fax", self._refToFax, '\n',
              "Ref By Name" , self._refByName , '\n',
              "Ref By Address" ,  self._refByAddress, '\n',
              "Ref By City" , self._refByCity , '\n',
              "Ref By Zip" , self._refByZip , '\n',
              "Ref By State", self._refByState , '\n',
              "Ref By Phone" , self._refByPhone, '\n',
              "Ref By Fax" ,  self._refByFax, '\n',
              "Ref reason " , self._refReason, '\n',
              "Diagnosis", self._diagnosis),       


    def extractInfoFromTable(self):
        
        pTop , pHeight , pTableName = self.getPatientInfoTable()
        if pTableName :           
            keyValueContent = self.extractKeyValueFromTable(pTop, pHeight)
            self.extractPatientContentInTable(keyValueContent)
        
        referTop , referHeight , refTableName = self.getReferInfoTable(pTableName)
        if refTableName:
            keyValueContent = self.extractKeyValueFromTable(referTop, referHeight)
            self.extractReferalContentInTable(keyValueContent)


    def extractDefaultKeyValuePairs(self):

        for content in self._keyValuePairs :
            if "patient" in content[0].lower() :
                if "name" in content[0].lower():
                    self._patientName = self._patientName + ' ' + content[1]
                   
            if ("dob" in content[0].lower()) or ("birth" in content[0].lower()) :    
                self._patientDOB = content[1]
                
            if "mrn" in content[0].lower():
                self._patientMRN = content[1]
               
            if ("gender" in content[0].lower()) or ("sex" in content[0].lower()):
                self._patientGender = content[1]

            if "refer" in content[0].lower() :
                if ("name" in content[0].lower()) or ("to" in content[0].lower()) or ("physician" in content[0].lower()):
                    self._refToName = self._refToName + " " + content[1]
            
            if ("refer" in content[0].lower()) and ("reason" in content[0].lower()):
                self._refReason = content[1]
             
            if ("diagnosis" in content[0].lower()):
                self._diagnosis = content[1]
                
            if ("refer" in content[0].lower()) and ("date" in content[0].lower()):
                self._refToDate = content[1]
                
            if "refer" in content[0].lower() :
                if ("from" in content[0].lower()) or ("by" in content[0].lower()):
                    self._refByName = self._refByName + " " + content[1]
                    
    
    def getPatientInfoTable(self):
        
        pateintInformationTable = False
        top , height , tableName = None , None , None
        for tableContent in self._tableContents :
            if pateintInformationTable :
                continue 
            
            for content in tableContent[2]:
                
                if "patient" in content.lower():
                    
                    width = tableContent[1][0]
                    height = tableContent[1][1]
                    top = tableContent[1][2]
                    left = tableContent[1][3]
                    
                    height = height + top
                    
                    newTop = (round(top,2)) - 0.03
                    
                    for line in self._lineContents : 
                        if round(line[1][2],2) >= newTop:
                            if round(line[1][2],2) <= (round(top,2)) :
                                if ("information" in line[0].lower()) or (("patient") in line[0].lower() ):                                       
                                      
                                    pateintInformationTable = True
                                    
                                    return top , height , tableContent[0]
        
        return top , height , tableName

    def getReferInfoTable(self,pTableName):

        referalInformationTable = False 
        top , height , tableName = None , None , None

        for tableContent in self._tableContents :
            if pTableName == tableContent[0]:
                continue
            if referalInformationTable:
                continue
            
            for content in tableContent[2]:
                
                if "refer" in content.lower():
                    
                    width = tableContent[1][0]
                    height = tableContent[1][1]
                    top = tableContent[1][2]
                    left = tableContent[1][3]
                    
                    height = height + top
                    
                    newTop = (round(top,2)) - 0.03
                    
                    for line in self._lineContents : 
                        if round(line[1][2],2) >= newTop:
                            if round(line[1][2],2) <= (round(top,2)) :
                                if ("information" in line[0].lower()) or (("refer") in line[0].lower() ):                                       
                                     
                                    referalInformationTable = True
                                    
                                    return top , height , tableContent[0]
     
        return top , height , tableName 

   
    def extractKeyValueFromTable(self,top , height):
      
        keyValueContent = []
        
        for kvp in self._keyValuePairs : 
            if str(kvp[4]).strip():                        
                if round(float(kvp[4]),2) >= round((top),2) :                                   
                    if round(float(kvp[4]),2) <= round((height),2):                   
                        keyValueContent.append([kvp[0] , kvp[1]])
        
        return keyValueContent
    
    def extractPatientContentInTable(self,patientContent):
        
      
        
        if not self._patientName:
            fname , mname , lname, name  = '' , '' , '' , ''
            for info in patientContent :
                if "name" in info[0].lower():
                    if "first" in info[0].lower() :
                        fname = info[1]
                    elif "middle" in info[0].lower() :
                        mname = info[1]
                    elif "last" in info[0].lower() :
                        lname = info[1]
                    else :
                        name = info[1]
            if name.strip():
                self._patientName = name
            elif fname.strip():
                self._patientName = fname + ' ' + mname + ' ' + lname
 
        
        for info in patientContent :
            if ("address" in info[0].lower()) and ("symptom" not in info[0].lower()):
                self._patientAddress = info[1]
                
            if ("phone" in info[0].lower()) or ("mobile" in info[0].lower()) or (("contact" in info[0].lower() and "number" in info[0].lower())):
                self._patientPhone = info[1]
                
            if ("city" in info[0].lower()) and ("zip" in info[0].lower()):
                if ',' in info[1]:
                    city , stzip = info[1].split(',')
                    self._patientCity = city
                    self._patientStZip = stzip
                else :
                    info[1] = info[1].strip()
                    self._patientCity = ' '.join(info[1].split(' ')[0:-2])
                    self._patientStZip = ' '.join(info[1].split(' ')[-2:])
                    
            if ("city" in info[0].lower()) and ("zip"  not in info[0].lower()):
                self._patientCity = info[1]
                
            if ("city" not in info[0].lower()) and ("zip"   in info[0].lower()):
                if info[1].strip(): 
                    self._patientStZip = info[1]
            
            if ("state" in info[0].lower()):
                if info[1].strip():
                    self._patientState = info[1]
                
    
    def extractReferalContentInTable(self, referalContent):
        
        self.removeLeadingTrailingSpaces()
        
        if not self._refToName:
            for info in referalContent :
                if ("name" in info[0].lower()) or ("to" in info[0].lower()):
                    if self._patientName  != info[1].strip() :
                        self._refToName = self._refToName + ' ' + info[1]
        
        for info in referalContent :
            if ("address" in info[0].lower()) and ("symptom" not in info[0].lower()):
                if self._patientAddress  != info[1].strip():
                    self._refToAddress = info[1]
                
            if ("phone" in info[0].lower()) or ("mobile" in info[0].lower()) or (("contact" in info[0].lower() and "number" in info[0].lower())):
                if self._patientPhone  != info[1].strip():
                    self._refToPhone = info[1]
                

            if ("city" in info[0].lower()) and ("zip" in info[0].lower()):
                if ',' in info[1]:
                    city , stzip = info[1].split(',')
                    if self._patientCity  != city.strip():
                        self._refToCity   =  city
                    if self._patientStZip  != stzip.strip():
                        self._refToStZip = stzip                    

                else :
                    info[1] = info[1].strip()
                    stzip = ' '.join(info[1].split(' ')[-2:])
                    city =  ' '.join(info[1].split(' ')[0:-2])
                    if self._patientCity  != city.strip():
                        self._refToCity   =  city
                    if self._patientStZip  != stzip.strip():
                        self._refToStZip = stzip  
                        
                   
            if ("city" in info[0].lower()) and ("zip"  not in info[0].lower()):
                if self._patientCity  != info[1].strip():
                    self._refToCity   =  city
                
            if ("city" not in info[0].lower()) and ("zip"   in info[0].lower()):
                    if self._patientStZip  != info[1].strip():
                        self._refToStZip = stzip 
            
            if "state" in info[0].lower():
                if self._patientState != info[1].strip():
                    self._refToState = info[1].strip()
                
            if ("date" in info[0].lower()) or (" on" in info[0].lower()):
                self._refToDate = info[1]
                
            if ("fax" in info[0].lower()):
                self._refToFax = info[1]
                
    def extractMissingPatientInfoByLine(self):
        
        self.removeLeadingTrailingSpaces()
        
        for line in self._lineContents :
            if (("patient" in line[0].lower()) or ("applicant" in line[0].lower())or ("client" in line[0].lower())) and  (("information" in line[0].lower()) or "name" in line[0].lower()):
                height , top = None , None

                height = round(line[1][1],2)
                top = round(line[1][2],2)                      
                height = height + top                
                height = height + 0.30
                kvContent = self.extractKeyValueFromTable(top , height)
               
                if not self._patientName :

                    fname , mname , lname, name  = '' , '' , '' , ''
 
                    for info in kvContent :
                        if "name" in info[0].lower():
                            
                            if "first" in info[0].lower() :
                                fname = info[1]
                                continue
                            elif "middle" in info[0].lower() :
                                mname = info[1]
                                continue
                            elif "last" in info[0].lower() :
                                lname = info[1]
                                continue
                            else :
                                if info[1].strip() :
                                    if not fname.strip():
                                        name = info[1]
                    if name:
                        self._patientName = name
                         
                    elif fname:
                        self._patientName = str(fname) + ' ' + str(mname) + ' ' + str(lname)                            
                         
 

                if not self._patientDOB :
                        for info in kvContent :
                            if ("dob" in info[0].lower()) or ("birth" in info[0].lower()) : 
                                if info[1].strip():
                                    self._patientDOB = info[1].strip()
                                 
                if not self._patientMRN :
                        for info in kvContent :
                            if ("mrn" in info[0].lower()) : 
                                if info[1].strip():
                                    self._patientMRN = info[1].strip()
                                 

                if not self._patientGender :
                        for info in kvContent :
                            if ("gender" in info[0].lower()) or ("sex" in info[0].lower()) : 
                                if info[1].strip():
                                    self._patientGender = info[1].strip()
                                 

                if not self._patientAddress :
                        for info in kvContent :
                            if ("address" in info[0].lower()): 
                                if ("symptom" not in info[0].lower()): 
                                    if info[1].strip():
                                        self._patientAddress = info[1].strip()
                                     
                                
                if not self._patientPhone :                    
                        for info in kvContent :
                            if ("phone" in info[0].lower()) or ("mobile" in info[0].lower()) or (("contact" in info[0].lower() and "number" in info[0].lower())): 
                                if len(info[1].strip()) > 4:
                                    self._patientPhone = info[1].strip()
                                 
                            
                if not self._patientCity :
                        for info in kvContent :
                            if ("city" in info[0].lower()) and ("zip" in info[0].lower()): 
                                if info[1].strip():
                                    if ',' in info[1]:
                                        city , stzip = info[1].split(',')
                                        self._patientCity = city.strip()
                                        self._patientStZip = stzip.strip()
                                         
                                    else :
                                        info[1] = info[1].strip()
                                        self._patientCity =  ' '.join(info[1].split(' ')[0:-2]).strip()
                                        self._patientStZip = ' '.join(info[1].split(' ')[-2:]).strip()
                                         
                            elif ("city" in info[0].lower()) :
                                if info[1].strip():
                                    self._patientCity = info[1].strip()
                                     

                if not self._patientStZip :
                        for info in kvContent :
                            if ("city" not in info[0].lower()) and ("zip" in info[0].lower()): 
                                if info[1].strip():
                                    self._patientStZip = info[1].strip()
                
                if not self._patientState:
                    for info in kvContent :
                        if "state" in info[0].lower():
                            self._patientState = info[1]  
                                
    def extractMissingReferalToInfoByLine(self):                               
         
        self.removeLeadingTrailingSpaces()
                  
        for line in self._lineContents : 
            if ("refer" in line[0].lower() ) and  (("information" in line[0].lower()) or "name" in line[0].lower()  or  "physician" in line[0].lower() or  "detail" in line[0].lower()):
                height , top = None , None

                height = round(line[1][1],2)
                top = round(line[1][2],2)                      
                height = height + top                
                height = height + 0.30
                kvContent = self.extractKeyValueFromTable(top , height)
                
                if not self._refToName:

                     for info in kvContent:
                       
                         if (("name" in info[0].lower()) or ("physician" in info[0].lower()) or ("referring" in info[0].lower())) :
                             #if (("provider" not in info[0].lower())) :
                            
                            if info[1].strip() not in  self._patientName :
                                if info[1].strip():
                                    self._refToName = info[1]
                                              
                            
                if not self._refToDate:
                        for info in kvContent :
                            if ("date " in info[0].lower()) or  (("on " in info[0].lower()) and ("refer" in info[0].lower())):
                                if info[1].strip():
                                    if info[1] != self._patientDOB :
                                        self._refToDate = info[1]

                                
                            
                if not self._refToAddress:
                        for info in kvContent :
                            if ("address" in info[0].lower()) and ("symptom" not in info[0].lower()):
                                if info[1].strip():                                 
                                    if info[1].strip() !=  self._patientAddress:
                                        self._refToAddress = info[1]

                                    
                            
                if not self._refToCity:
                        for info in kvContent :
                            if ("city" in info[0].lower()) and ("zip" in info[0].lower()) :
                                if info[1].strip():
                                    if ',' in info[1]:
                                        city , stzip = info[1].split(',')
                                        
                                        if self._patientCity != city.strip():
                                            self._refToCity = city
                                        if self._patientStZip  != stzip.strip():
                                            self._refToStZip = stzip
                                         
                                    else :
                                        info[1] = info[1].strip()
                                        city = ' '.join(info[1].split(' ')[-2:])
                                        stzip = ' '.join(info[1].split(' ')[0:-2])
                                        if self._patientCity  != city.strip():
                                            self._refToStZip   =  city
                                        if self._patientStZip  != stzip.strip():
                                            self._refToStZip = stzip
                                         
                            elif  ("city" in info[0].lower())  :
                                if info[1].strip():
                                    if self._patientCity  != info[1].strip():
                                        self._refToCity = info[1]
                                     
                            
                            
                if not self._refToStZip :
                        for info in kvContent :
                            if ("city" not in info[0].lower()) and ("zip" in info[0].lower()): 
                                if info[1].strip():
                                    if self._patientStZip != info[1].strip():
                                        self._refToStZip = info[1]

                if not self._refToState:
                    for info in kvContent :
                        if "state" in info[0].lower():
                            self._refToState = info[1].strip()


                                
                if not self._refToPhone:                    
                        for info in kvContent :
                             if ("phone" in info[0].lower()) or ("mobile" in info[0].lower()) or (("contact" in info[0].lower() and "number" in info[0].lower())): 
                                if len(info[1].strip()) > 4 :
                                    if self._patientPhone  != info[1].strip():
                                        self._refToPhone = info[1]
                                   
                            
                if not self._refToFax:
                        for info in kvContent :
                            if "fax" in info[0].lower():
                                if info[1].strip():
                                    self._refToFax = info[1]
                                 
            if not self._refReason:
                height , top = None , None
                if ("reason" in line[0].lower() ) :
                  
                    height = round(line[1][1],2)
                    top = round(line[1][2],2)                      
                    height = height + top                
                    height = height + 0.30
                    kvContent = self.extractKeyValueFromTable(top , height)
                    for info in kvContent :
                        if "reason" in info[0].lower():
                            if info[1].strip():
                                self._refReason = info[1]
                               
            
            if not self._diagnosis:
                height , top = None , None
                if ("diagnosis" in line[0].lower() ) :
                  
                    height = round(line[1][1],2)
                    top = round(line[1][2],2)                      
                    height = height + top                
                    height = height + 0.30
                    kvContent = self.extractKeyValueFromTable(top , height)
                    for info in kvContent :
                        if "description" in info[0].lower():
                            if info[1].strip():
                                self._diagnosis = info[1]
                                break 
                                            
                            
    def extractMissingReferalByInfoByLine(self):                          
        
        self.removeLeadingTrailingSpaces()
        
        for line in self._lineContents :             
           
            height , top = None , None
            if (("by" in line[0].lower() ) and  (("refer" in line[0].lower()) or "diagnos" in line[0].lower())) or (("from" in line[0].lower() ) and  (("refer" in line[0].lower()) or "diagnos" in line[0].lower())):
              
                height = round(line[1][1],2)
                top = round(line[1][2],2)                      
                height = height + top                
                height = height + 0.30
                kvContent = self.extractKeyValueFromTable(top , height)
                
                
                for info in kvContent :
                    
                    if not self._refByName:
                        if ("by" in info[0].lower()) or ("from" in info[0].lower()) or ("name" in info[0].lower()):
                          
                            if info[1] != self._patientName :
                                if info[1] != self._refToName:
                                    if info[1].strip():
                                        self._refByName = info[1]
                        
                    if not self._refByAddress:
                        if ("address" in info[0].lower()) and ("symptom" not in info[0].lower()):
                            
                            if info[1] != self._patientAddress :
                                if info[1] != self._refToAddress:
                                    if info[1].strip():
                                        self._refByAddress = info[1]

                    if not self._refByCity:
                        if "city" in info[0].lower() and "zip" in info[0].lower():
                            if info[1] != self._patientCity :
                                if info[1] != self._refToCity:
                                    if info[1].strip():
                                        if ',' in info[1]:
                                            city , stzip = info[1].split(',')
                                            
                                            self._refByCity = city
                                            self._refByZip = stzip
                                            
                                        else :
                                            info[1] = info[1].strip()
                                            self._refByZip  = ' '.join(info[1].split(' ')[-2:])
                                            self._refByCity  = ' '.join(info[1].split(' ')[0:-2])
                                            
                        if "city" in info[0].lower() and "zip" not in info[0].lower():
                            
                            if info[1] != self._patientCity :
                                if info[1] != self._refToCity:
                                    self._refByCity = info[1]
                            
                            
                    if not self._refByZip:
                        if "zip" in info[0].lower():
                            if info[1] != self._patientStZip :
                                if info[1] != self._refToStZip:
                                    self._refByZip = info[1]

                    if not self._refByState:
                        if "state" in info[0].lower():
                            self._refByState = info[1].strip()


                    if not self._refByPhone:
                        if "phone" in info[0].lower():
                            if info[1] != self._patientPhone :
                                if info[1] != self._refToPhone:
                                    if len(info[1].strip()) > 4 :
                                        self._refByPhone = info[1]
                        
                                
                    if not self._refByFax:
                        if "fax" in info[0].lower():
                            if info[1] != self._refToFax :
                                if info[1].strip():
                                    self._refByFax = info[1]
                                      

    def removeLeadingTrailingSpaces(self) :
        
        if self._patientName :
            self._patientName = self._patientName.strip()
        if self._patientDOB :
            self._patientDOB = self._patientDOB.strip()
        if self._patientMRN:
            self._patientMRN = self._patientMRN.strip()
        if self._patientGender:
            self._patientGender = self._patientGender.strip()
        if self._patientAddress:
            self._patientAddress = self._patientAddress.strip()
        if self._patientPhone:
            self._patientPhone = self._patientPhone.strip()
        if self._patientCity:
            self._patientCity = self._patientCity.strip()
        if self._patientStZip:
            self._patientStZip = self._patientStZip.strip()
        if self._refToName:
            self._refToName = self._refToName.strip()
        if self._refToDate:
            self._refToDate = self._refToDate.strip()
        if self._refToAddress:
            self._refToAddress = self._refToAddress.strip()
        if self._refToCity:
            self._refToCity = self._refToCity.strip()
        if self._refToPhone:
            self._refToPhone = self._refToPhone.strip()
        if self._refToFax:
            self._refToFax = self._refToFax.strip()
        if self._refToStZip:
            self._refToStZip = self._refToStZip.strip()
        if self._refByName:
            self._refByName = self._refByName.strip()
        if self._refByAddress:
            self._refByAddress  = self._refByAddress.strip()
        if self._refByCity:
            self._refByCity = self._refByCity.strip()
        if self._refByZip:
            self._refByZip = self._refByZip.strip()
        if self._refByPhone:
            self._refByPhone = self._refByPhone.strip()
        if self._refByFax:
            self._refByFax = self._refByFax.strip()
        if self._refReason:
            self._refReason = self._refReason.strip()
        if self._diagnosis:
            self._diagnosis = self._diagnosis.strip()

         
        if self._patientState:
            self._patientState = self._patientState.strip()
        if self._refToState:
            self._refToState = self._refToState.strip()
        if self._refByState:
            self._refByState = self._refByState.strip()
                
                    