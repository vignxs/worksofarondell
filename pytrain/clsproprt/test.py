from proprt import Person
from proprt import PerfectPerson


person = Person('vignesh', 'siva')
print('using Person')
person.first = 'siva'

print('\t' +  person.first)
print('\t' + person.mail)
print('\t' + person.fullname())

person = PerfectPerson('vignesh', 'siva')
print('using PerfectPerson')
person.first = 'siva'

print('\t' +  person.first)
print('\t' + person.mail)
print('\t' + person.fullname())