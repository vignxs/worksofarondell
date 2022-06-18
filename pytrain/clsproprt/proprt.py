class Person:
    def __init__(self, first, last):
        self.first = first
        self.last = last
        self.mail = '{},{}@gmail.com'.format(self.last, self.first)
     
    # @property   
    def fullname(self):
        return ('{} {}'.format(self.first.title(), self.last.title()))
        
    # def tellage(self):
    #     return 'my age is', self.age
    
person = Person('tommy', 'shelby')

person.last = 'londan'

# print(person.first)
# print(person.mail)
# print(person.fullname())

class PerfectPerson:
    def __init__(self, first, last):
        self.first = first
        self.last = last
    
    @property
    def mail(self):
        return '{},{}@gmail.com'.format(self.last, self.first)
        
    def fullname(self):
        return ('{} {}'.format(self.first.title(), self.last.title()))