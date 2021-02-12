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




class Error(Model):

    timestamp = DateTimeField(auto_now_add=True)
    data = jsonfield.JSONField()


    def __str__(self):
        return self.timestamp

    class Meta:
        verbose_name = 'Ошибка'
        verbose_name_plural = 'Ошибки'



class Url(Model):

    city = ForeignKey('City', on_delete=CASCADE, verbose_name='Город')
    language = ForeignKey('Language', on_delete=CASCADE, verbose_name='Язык программирования')
    url_data = jsonfield.JSONField(default=get_default_urls)

    class Meta:

        unique_together = ('city', 'language',)
        # unique_together - означает, что мы не сможем для двух экземпляром один ко многим
        # сделать больше чем одна строка.
        # Допустим запись в таблицу url ссылается Киев для city и python для language
        # благодаря unique_together мы можем сделать только одну запись для сочетания Киев и python
#         Для каждой записи уникальное сочетание заданных полей, если вкратце.





