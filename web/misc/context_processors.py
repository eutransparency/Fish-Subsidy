import random

def header_class(request):
    return {'header_class' : 'header_' + str(random.randint(1,6))}
