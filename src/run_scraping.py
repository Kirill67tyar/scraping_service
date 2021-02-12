# ------------------------------------------------------- Запуск Django в не самого проекта
import os, sys


proj = os.path.dirname(os.path.abspath('manage.py'))    # устанавливаем абсолютный путь

# тут мы добавляем путь в системные переменные путей
sys.path.append(proj)

os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'
# for p in os.environ:
#     print(f'{p} - {os.environ[p]}')
import django

django.setup()
# ------------------------------------------------------- Запуск Django в не самого проекта
import codecs
from scraping.parsers import *
from scraping.models import City, Language, Vacancy, Error
from scraping.utils import get_object_or_null
from django.shortcuts import get_object_or_404
from django.db import DatabaseError
from django.contrib.auth import get_user_model



parsers = (
            (work, 'https://www.work.ua/ru/jobs-kyiv-python/'),
            (rabota, 'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2'),
            (job_dou, 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python'),
            (djinni, 'https://djinni.co/jobs/location-kyiv/?primary-keyword=Python'),
           )

User = get_user_model()


def get_settings():
    qs = User.objects.filter(mailing=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst

q = get_settings()
print(q)

city = get_object_or_null(model=City, slug='kiev')
language = get_object_or_null(model=Language, slug='python')
jobs, errors = [], []

for func, url in parsers:
    ## не мой вариант
    j, e = func(url)
    jobs.extend(j)
    errors.extend(e)

    # мой вариант
    # jobs.extend(pair[0](pair[-1])[0])
    # errors.extend(pair[0](pair[-1])[-1])


for vacancy in jobs:

    v = Vacancy(**vacancy, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass


if errors:
    err = Error(data=errors).save()



# ------------------------------------------------------------------
# if __name__ == '__main__':
#     print(*jobs, sep='\n')
#     print('count jobs -', len(jobs))
#     print('errors -', errors)

# with codecs.open('work.txt', 'w', 'utf-8') as f:
#     f.write(str(jobs))