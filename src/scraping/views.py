from django.core.paginator import Paginator
from django.shortcuts import render
from scraping.models import Vacancy, Language, City
from scraping.forms import SearchForm, ExperimentSearchForm
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


def home_view(request):

    form = SearchForm()
    form_experiment = ExperimentSearchForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    qs = []
    report = None
    if city or language:
        _filter = {}
        if city:
            _filter["city__slug"] = city
        if language:
            _filter["language__slug"] = language
        qs = Vacancy.objects.filter(**_filter)
        count = qs.count()
        report = f'{f"По Вашему запросу найдено {count} вакансия(ий)" if count else "По вашему запросу нет вакансий"}'
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'object_list': qs,
        'page_obj': page_obj,
        'form': form,
        'form_experiment': form_experiment,
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
    return render(request=request, template_name='scraping/home.html', context=context)


