import json
import collections
import logging
logging.basicConfig(level=logging.NOTSET, format=' %(levelname)s - %(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)


class Checkups:
    """ checkups for checks"""
    def __init__(self) -> None:
        self.error = False
        self.filename = ''
    def __str__(self) -> str:
        return 'method for checkups'
    
    def prime_checks(self, filename):
        """ checkups for checks"""
        
        self.filename = filename
        content = self.get_content(self.filename)
        
        self.mobileno_validation(content)
        if not self.error:
            self.zip_validation(content)
            if not self.error:
                content = json.dumps(content)
                obj = json.loads(content, object_pairs_hook=self.validate_data)
            else:
                logger.warning('zip code validation failed', extra={'foo': 'Prime Checks' })  
            
        else:
            logger.warning('mobile number validation failed', extra={'foo': 'Prime Checks' })         
    
    def mobileno_validation(self, content):
        
        column_keys = ['patient_phone', 'ref_to_phone' , 'ref_by_phone']
        
        for key in column_keys:
            
            if content[key] is not None:
                if  str(content[key]).isnumeric() and  8 >= (len(str(content[key])) <= 12 ):
                    logger.info(f'{key} validation succesfull', extra={'foo': 'Prime Checks' })
                    
                else:
                    self.error = True
                    break
            else:
                logger.warning(f'{key} validation failed because it\'s null', extra={'foo': 'Prime Checks' })
                self.error = True
                break
                
                
                
        return self.error
    
    def zip_validation(self, content):
        column_keys = ['patient_st_zip', 'ref_to_st_zip' , 'ref_by_st_zip']
        for key in column_keys:
            if content[key] is not None:
                if  str(content[key]).isnumeric() and  (len(str(content[key])) == 5 ):
                    logger.info(f'{key} validation succesfull', extra={'foo': 'Prime Checks' })
                else:
                    self.error = True
            else:
                logger.warning(f'{key} validation failed because it\'s null', extra={'foo': 'Prime Checks' })
                
        return self.error
            
    def detect_duplicate_keys(self, list_of_pairs):
        
        key_count = collections.Counter(k for k,v in list_of_pairs)
        
        duplicate_keys = ', '.join(k for k,v in key_count.items() if v>1)
        if len(duplicate_keys) != 0:
            self.error = True
            
    def validate_data(self, list_of_pairs):
        self.detect_duplicate_keys(list_of_pairs)
        logger.info('duplicates validation success' if not self.error else "duplicates validation failed", extra={'foo': 'Prime Checks' })
        return self.error
                    
    def get_content(self, filename):
        with open(self.filename, 'r') as file:
            content = json.load(file)
        return content
                
         
            
        
                
        
        
        
        