class Person:
    def __init__(self, first : str, last : str):
        self.first = first
        self.last = last
        self.mail = '{},{}@gmail.com'.format(self.last, self.first)
     
    # @property   
    def fullname(self):
        return ('{} {}'.format(self.first.title(), self.last.title()))


class PerfectPerson:
    def __repr__(self) -> str:
        return 'class for training on  property'
    
    def __str__(self) -> str:
        return 'class for training on str  property'
    
    def __init__(self, first, last):
        self.first = first
        self.last = last
    
    @property
    def mail(self) -> str:
        return '{},{}@gmail.com'.format(self.last, self.first)
        
    def fullname(self) -> str:
        return ('{} {}'.format(self.first.title(), self.last.title()))