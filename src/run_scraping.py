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
import asyncio
from django.shortcuts import get_object_or_404
from django.db import DatabaseError
from django.contrib.auth import get_user_model
from scraping.parsers import *
from scraping.models import City, Language, Vacancy, Error, Url
from scraping.utils import get_object_or_null




parsers = (
            (work, 'work'),
            (rabota, 'rabota'),
            (job_dou, 'dou'),
            (djinni, 'djinni'),
           )

User = get_user_model()

jobs, errors = [], []

def get_settings():
    qs = User.objects.filter(mailing=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst


def get_url(_settings):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[-1]
        tmp['url_data'] = url_dict.get(pair, {})
        urls.append(tmp)
    return urls


# await запускает функцию, и при этом происходт переключение на другое выполнение,
# тем самым достигается распараллеливание, и как следствие - увеличение скорости работы
# но перед этим необходимо пометить, что наша функция и потавить ключевое слово async перед
# определением фукции.
# executor - исполнитель (implementer, performer)
async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    jobs.extend(job)
    errors.extend(err)




_settings = get_settings()
url_list = get_url(_settings)



# import time
# start = time.time()

# ---------------------------------------------------------------------    Асинхронный способ выполнения
# for i in range(10):
loop = asyncio.get_event_loop() #  сздаем loop для асинхронного программирования
tmp_tasks = [(func, data['url_data'].get(key, None), data['city'], data['language'])
                 for data in url_list
                 for func, key in parsers]

## когда wait вызывается - он регулирует переключение интерпритатора, для той  или иной таски
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
loop.run_until_complete(tasks)
loop.close()
# ---------------------------------------------------------------------    Асинхронный способ выполнения

            #                   OR

# # =====================================================================    Неасинхронный способ выполнения
# for i in range(10):
#     for data in url_list:
#         for func, key in parsers:
#             url = data['url_data'].get(key, None)
#             if url:
#                 # вот эта строчка - блокирующий вызов. Самый узкий проход нашего кода, бутылочное горлышко
#                 # весь код не может быть выполнен, пока не пройдут эти функции
#                 # поэтому мы здесь и используем асинхронный подход
#                 j, e = func(url, city=data['city'], language=data['language'])
#                 jobs.extend(j)
#                 errors.extend(e)
# # =====================================================================    Неасинхронный способ выполнения

# print((time.time() - start) / 10)
# print(*jobs,len(jobs), sep='\n')
# print(errors)


for vacancy in jobs:

    v = Vacancy(**vacancy)
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