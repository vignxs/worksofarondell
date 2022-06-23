import json
import collections

class Checkups:
    def __init__(self) -> None:
        self.error = False
        self.filename = ''
        
    def prime_checks(self, filename):
        self.filename = filename
        content = self.get_content(self.filename)
        
        self.mobileno_validation(content)
        
        if not self.error:
            error = self.zip_validation(content)
            if not self.error:
                obj = json.loads(content, object_pairs_hook=self.validate_data)
    
    def mobileno_validation(self, content):
        
        if str(content['patient_phone']).isnumeric() and (len(str(content['patient_phone'])) == 10 ):
            print('checks are passed from patient phone number')
        else:
            print('checks are faild from patient phone number')
            self.error = True
            
        if str(content['ref_to_phone']).isnumeric() and (len(str(content['ref_to_phone'])) == 10 ):
            print('checks are passed ref to phone number')
        else:
            print('checks are faild ref to phone number')
            self.error = True
            
        if str(content['ref_by_phone']).isnumeric() and (len(str(content['ref_by_phone'])) == 10 ):
            print('checks are passed ref by phone number')
        else:
            print('checks are faild ref by phone number')
            self.error = True
            
        return self.error
    
    def zip_validation(self, content):
        
        self.error = False if str(content['patient_st_zip']).isnumeric() and (len(str(content['patient_st_zip'])) == 10 ) else True
        
        if str(content['patient_st_zip']).isnumeric() and (len(str(content['patient_st_zip'])) == 10 ):
            print('checks are passed from patient_st_zip number')
        else:
            print('checks are faild from patient_st_zip number')
            self.error = True
            
        if str(content['ref_to_st_zip']).isnumeric() and (len(str(content['ref_to_st_zip'])) == 10 ):
            print('checks are passed ref to_st_zip number')
        else:
            print('checks are faild ref to_st_zip number')
            self.error = True
            
        if str(content['ref_by_st_zip']).isnumeric() and (len(str(content['ref_by_st_zip'])) == 10 ):
            print('checks are passed ref by_st_zip number')
        else:
            print('checks are faild ref by_st_zip number')
            self.error = True
            
    def detect_duplicate_keys(self, list_of_pairs):
        
        key_count = collections.Counter(k for k,v in list_of_pairs)
        duplicate_keys = ', '.join(k for k,v in key_count.items() if v>1)

        if len(duplicate_keys) != 0:
            self.error = True
            
    def validate_data(self, list_of_pairs):
        self.detect_duplicate_keys(list_of_pairs)
        return self.error
                    
    def get_content(self, filename):
        """This function loads the given content available"""
        with open(self.filename, 'r') as file:
            content = json.load(file)
        return content
                
                
            
            
x = Checkups()
f = ('C:/Users/hrint/Documents/Python2022/healthcare/db/data.json')
x.prime_checks(f)
                
        
        
        
        