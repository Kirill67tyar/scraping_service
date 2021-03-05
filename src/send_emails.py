# ------------------------------------------------------- Запуск Django в не самого проекта
import os, sys
from datetime import date, timedelta
import django

proj = os.path.dirname(os.path.abspath('manage.py'))    # устанавливаем абсолютный путь

# тут мы добавляем путь в системные переменные путей
sys.path.append(proj)

os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

django.setup()
# ------------------------------------------------------- Запуск Django в не самого проекта
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from scraping.models import Vacancy, Error, Url, City, Language
from scraping.utils import get_object_or_null
from scraping_service.settings import EMAIL_HOST_USER


today = date.today()
subject = f'Рассылка вакансий за {today}'
text_content = 'Вакансии:'
from_email = EMAIL_HOST_USER
admin_user = EMAIL_HOST_USER
empty = f'<h4>На сегодняшний день ({today}) вакансий нет.</h4>'
fresh_date = today - timedelta(days=10)

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
    users_dict.setdefault(key, [])
    users_dict[(city, language)].append(email)

# -----------------------------------------------------------------

users_dict = dict(filter(lambda x: None not in x[0], users_dict.items()))

# ------------------------------------------------------------------

# это не совсем хороший алгоритм. Мы коллкуционируем записи по ключу и значению.
# Допустим есть два пользователя, у одного city_id и language_id равны 3 и 1. У другого 2 и 5
# Нам нужны вакансии, привязанные к городу и языку 3-1 и 2-5. Но этот алгоритм
# будет находить нам вакансии помимо тех что нужно также и 3-5 и 2-1.
if users_dict:
    params = {'city_id__in': [], 'language_id__in': [],}
    for pair in users_dict.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[-1])
    qs = Vacancy.objects.filter(**params, timestamp=today).values()

    vacancies = {}
    for v in qs:
        city = v['city_id']
        language = v['language_id']
        key = (city, language,)
        vacancies.setdefault(key, [])
        vacancies[key].append(v)
    # print(*vacancies[(3,1)],sep='\n')

    for key, emails in users_dict.items():
        rows = vacancies.get(key, [])
        html = ''
        if rows:
            for row in rows:
                html += f'<h3><a href="{ row["url"] }" target="_blank">{ row["title"] }</a></h3>'
                html += f'<p>{row["company"]}</p>'
                html += f'<p>{str(row["timestamp"])}</p><br><hr>'
        html_content = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


error = get_object_or_null(Error, datestamp=today)
subject = text_content = html_content = ''
to = admin_user






# ---------------------------------------------------------- Ищем ошибки скрапинга (START)
if error:
    errors_data = error.data.get('errors', [])
    feedback_data = error.data.get('feedback', [])
    html_content += f'<h3>Ошибки скрапинга:</h3>'
    for i, err in enumerate(errors_data, start=1):
        html_content += f'<p>{i}) url: {err.get("url")}</p>'
        html_content += f'<p>cause: {err.get("cause")}</p>'
        html_content += f'<p>status code: {err.get("status_code")}</p>'
        html_content += f'<p>{error.timestamp}</p><br>'
        # html_content += f'<p>{"-"*50}</p>'
    subject += f'{today} Ошибки скрапинга'
    text_content += 'Ошибки скрапинга'
    html_content += f'<br><hr><h3>Сообщения от пользователей:</h3>'
    for i, message in enumerate(feedback_data, start=1):
        html_content += f'<p>{i}) Email - {message.get("email")}</p>'
        html_content += f'<p>language: {message.get("language")}</p>'
        html_content += f'<p>city: {message.get("city")}</p><br>'
        # html_content += f'<p>{"-"*50}</p>'
    subject += f' Обратная связь'
    text_content += ' Обратная связь'
# ---------------------------------------------------------- Ищем ошибки скрапинга (FINISH)








# ========================================================== Ищем пары город-язык к которым нет urls (START)
qs = Url.objects.all().values('city', 'language')
urls_dict = {(data['city'], data['language']): True for data in qs}


users_keys = set(users_dict.keys())
urls_keys = set(urls_dict.keys())
keys_without_urls = list(users_keys.difference(urls_keys))

# *** Эти две строчки, для того, чтобы отображать название городов в письме ***
city_names = City.objects.filter(pk__in=[i[0] for i in keys_without_urls]).values('name', 'pk')
language_names = Language.objects.filter(pk__in=[i[-1] for i in keys_without_urls]).values('name', 'pk')
# *** ***

url_errors = '<br><hr><h3>Для следующих городов и языков программирования отсутствуют urls</h3>'
if keys_without_urls:
    subject += f' Отстутсвующие urls'
    text_content += 'Отсутствующие urls'
    for city, language in keys_without_urls:
        name_city = list(filter(lambda x: x['pk'] == city,  city_names))[0]['name']
        name_language = list(filter(lambda x: x['pk'] == language, language_names))[0]['name']
        url_errors += f'<p>город: {name_city}, яп: {name_language} | ({city}, {language})</p>'
    html_content += url_errors
# ========================================================== Ищем пары город-язык к которым нет urls (FINISH)

# ------------ Посылаем письмо админу ------------
if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# with open('to_admin.html', 'w') as p:
#     p.write(html_content)















