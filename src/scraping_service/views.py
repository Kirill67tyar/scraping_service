from django.shortcuts import (render, HttpResponse,)
from datetime import datetime, date
from random import randrange, choice
from string import printable

def home(request):

    ch = ''.join([choice(printable[:62]) for i in range(randrange(30, 61))])
    today = date.today()
    td = datetime.now().today()
    day_and_time = datetime.now()
    _context = {
        'ch': ch,
        'td': td,
        'today': today,
        'day_and_time': day_and_time,
    }

    return render(request=request, template_name='some_template.html', context=_context)


