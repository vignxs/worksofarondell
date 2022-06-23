import boto3
client = boto3.client(service_name='comprehendmedical')
result = client.detect_entities_v2(Text= 'cerealx 84 mg daily')
entities = result['Entities']
for entity in entities:
    print('Entity', entity)
    
response = client.infer_icd10_cm(
    Text='string')