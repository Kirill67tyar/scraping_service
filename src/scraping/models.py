from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User, AbstractUser
from django.db.models import \
    (Model, CharField, URLField, TextField, ForeignKey, DateField, IntegerField, DateTimeField, CASCADE)
from django.http import Http404

from django.shortcuts import get_object_or_404

from scraping.utils import from_cyrilic_to_eng
import jsonfield


def get_default_urls():
    return {'rabota':'',
            'work':'',
            'dou':'',
            'djinni':'',}


class City(Model):

    name = CharField(max_length=255, unique=True, verbose_name='Название города')
    slug = CharField(max_length=255, blank=True, verbose_name='Url города')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        
    def save(self, *args, **kwargs):
        self.name = self.name.title()
        if not self.slug:
            self.slug = from_cyrilic_to_eng(str(self.name))
        super().save(*args, **kwargs)





class Language(Model):
    
    name = CharField(max_length=255, unique=True, verbose_name='Язык программирования')
    slug = CharField(max_length=255, blank=True, verbose_name='Url языка программирования')
    
    def __str__(self):
        return self.name.title()
    
    class Meta:
        verbose_name='Язык программирования'
        verbose_name_plural = 'Языки программирования'
        
    def save(self, *args, **kwargs):
        self.name = self.name.title()
        if not self.slug:
            self.slug = from_cyrilic_to_eng(str(self.name))
        super().save(*args, **kwargs)
        


class Vacancy(Model):
    
    url = URLField(unique=True)
    title = CharField(max_length=255, verbose_name='Заголовок вакансии')
    company = CharField(max_length=255, verbose_name='Компания')
    description = TextField(verbose_name='Описание вакансии')
    city = ForeignKey('City', on_delete=CASCADE, verbose_name='Город')#, null=True, blank=True)
    language = ForeignKey('Language', on_delete=CASCADE, verbose_name='Язык программирования')#, null=True, blank=True)
    timestamp = DateField(auto_now_add=True, verbose_name='Дата публикации')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = '-timestamp',




class Error(Model):

    timestamp = DateTimeField(auto_now_add=True)
    data = jsonfield.JSONField()


    def __str__(self):
        return str(self.timestamp)

    class Meta:
        verbose_name = 'Ошибка'
        verbose_name_plural = 'Ошибки'



class Url(Model):

    city = ForeignKey('City', on_delete=CASCADE, verbose_name='Город')
    language = ForeignKey('Language', on_delete=CASCADE, verbose_name='Язык программирования')
    url_data = jsonfield.JSONField(default=get_default_urls)

    class Meta:

        unique_together = ('city', 'language',)
        # unique_together - означает, что мы не сможем для двух записей в столбике один ко многим
        # сделать больше чем одну строку.
        # Допустим запись в таблицу url ссылается Киев для city и python для language
        # благодаря unique_together мы можем сделать только одну запись для сочетания Киев и python
#         Для каждой записи уникальное сочетание заданных полей, если вкратце.



#                   Forms / ModelForms

# src:
# https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/
# https://docs.djangoproject.com/en/3.1/ref/forms/models/

# Как проверить юзера еще на этапе валидации?
# Каждая форма, когда вызывается - содержит метод clean()

# Очень важно: когда мы редактируем профиль, то очень не желательно в url передавать id пользователя
# как же передать в форму instance? И как вообще узнать какой профиль нужно редактировать?]
# Очень просто - request.user   даст нам представление о том, чей профиль нужно редактировать
# django сам определяет какой юзер к нам заходит
# если юзер не авторизирован, то request.user будет AnonymousUser (экземпляр специального класса AnonymousUser)
# проверить авторизирован он или нет можно request.user.is_authenticated - выдаст булевое значение
# приредактировании профиля имеет смысл проверить на авторизацию юзера, в общем
# смотри accounts.views update_view
# при update если мы используем обычную Form, то нужно сохранять изменения вручную
# data = form.cleaned_data >>> user.city = data['city'] >>> user.language = data['language']
# При ModelForm достаточно закинуть в форму instance и data, где instance - объект модели до изменений,
# а data это request.POST (или request.data в REST API)

# Кстати, на том, что такое request, django в консоли выдает <WSGIRequest: GET '/job-search/'>
# Погугли что такое WSGI
# Посмотри, что печатает в консоли в http://127.0.0.1:8000/job-search/experiment/