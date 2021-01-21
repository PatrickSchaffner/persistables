class Meta(type):
    def __new__(self, name, bases, attrs, **kwargs):
        print(name)
        print(bases)
        print(attrs)
        print(kwargs)
        return type(name, bases, attrs)

class Base(metaclass=Meta):
    pass

class Obelix(Base):
    pass

y = Obelix(5)
