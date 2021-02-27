from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy

from scraping.models import Vacancy, Language, City
from scraping.forms import SearchForm, ExperimentSearchForm
from datetime import datetime, date, timedelta
from random import randrange, choice
from string import printable

timestamp = date.today() - timedelta(days=10)



def experiments(request):

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
    print(f'\n\n**************************************\n'
          f'request.user - {request.user}\n'
          f'request.user.is_authenticated - {request.user.is_authenticated}\n'
          f'request - {request}\n'
          f'type(request) - {type(request)}\n'
          f'type(request).mro() - {type(request).mro()}\n'
          f'request.POST - {request.POST}\n'
          f'request.GET - {request.GET}\n'
          f'dir(request) - {dir(request)}'
          f'\n**************************************\n\n',end='\n'*10)
    for method in dir(request):
        print(f'request.{method} -', getattr(request, method), end='\n'*3)
    print('\n'*10)

    return render(request=request, template_name='some_template.html', context=_context)


def form_view(request):
    form = SearchForm()

    return render(request, template_name='scraping/home.html', context={'form': form,})


def list_view(request):
    form = SearchForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    page_obj = []

    if city or language:
        _filter = {}
        if city:
            _filter["city__slug"] = city
        if language:
            _filter["language__slug"] = language
        page_obj = Vacancy.objects.filter(**_filter, timestamp__gte=timestamp)
    count = len(page_obj)
    report = f'{f"По Вашему запросу найдено {count} вакансия(ий)" if count else "По вашему запросу нет вакансий"}'
    paginator = Paginator(page_obj, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'report': report,
        'city': city,
        'language': language,
    }
    # if request.method == 'POST':
    #     print(f'\n\n@@@@@@@@@@@@@@@@@@@@@@@@@@\n'
    #           f'request.POST - {request.POST}\n'
    #           f'request.POST.get("city") - {request.POST.get("city")}\n'
    #           f'\n@@@@@@@@@@@@@@@@@@@@@@@@@\n\n')
    # if request.method == 'GET':
    #     print(f'\n\n$$$$$$$$$$$$$$$$$$$$$$$$\n'
    #           f'request.GET - {request.GET}\n'
    #           f'request.GET.get("language") - {request.GET.get("language")}\n'
    #           f'$$$$$$$$$$$$$$$$$$$$$$$$$\n\n')
    return render(request=request, template_name='scraping/list.html', context=context)


