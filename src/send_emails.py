# ------------------------------------------------------- Запуск Django в не самого проекта
import os, sys
import django

proj = os.path.dirname(os.path.abspath('manage.py'))    # устанавливаем абсолютный путь

# тут мы добавляем путь в системные переменные путей
sys.path.append(proj)

os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

django.setup()
# ------------------------------------------------------- Запуск Django в не самого проекта
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from scraping.models import Vacancy

User = get_user_model()

qs = User.objects.filter(mailing=True).values('city', 'language', 'email')
users_dict = {}
# Держи в голове, что city и language - необязательные поля, и могут быть None
### ddd = dict(filter(lambda x: None not in x[0], d.items()))
# print(qs)
for data in qs:
    city = data.get('city')
    language = data.get('language')
    email = data['email']
    key = (city, language)
    print(key)
    users_dict.setdefault(key, [])
    users_dict[(city, language)].append(email)
# print(users_dict)

if users_dict:
    params = {'city_id__in': [], 'language_id__in': [],}
    for pair in users_dict.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[-1])
    qs = Vacancy.objects.filter(**params).values()[:10]

    vacancies = {}
    for v in qs:
        city = v['city_id']
        language = v['language_id']
        key = (city, language,)
        vacancies.setdefault(key, [])
        vacancies[key].append(v)
    print(*vacancies[(3,1)],sep='\n')

    for key, emails in users_dict.items():
        rows = vacancies.get(key, [])
        html = ''
        for row in rows:
            html += f'<h5><a href="{ row["url"] }" target="_blank">{ row["title"] }</a></h5>'
            html += f'<p>{row["company"]}<\p>'
            html += f'<p>{str(row["timestamp"])}</p><br><hr>'


"""
<h5 class="card-title"><a href="{{obj.url}}" target="_blank">{{obj.title}}</a></h5>
"""


subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
text_content = 'This is an important message.'
html_content = '<p>This is an <strong>important</strong> message.</p>'
msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
msg.attach_alternative(html_content, "text/html")
msg.send()