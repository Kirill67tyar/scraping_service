"""scraping_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import (path, include,)
from scraping_service.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home),
]

# lesson start 2-6 (15)


# Middleware - прослойка, которая может влиять на запрос, вносить в него изменения, или вообще его оклонять
# Вспомни, когда ты устанавливаешь приложение tool-bar которое подсчитывает sql запросы (и не только)
# ты вносишь изменения в middleware



# ----------------------------- SETTINGS -----------------------
# Как django узнает какой urls.py является главным?
# В settings.py есть константа ROOT_URLCONF, по ней django и ориентуриется какой urls.py задействовать.

# SECRET_KEY в настройках в django является уникальным, его нигде нельзя засвечивать.
# Для чего он нужен? не знаю, но возможно это как то связано с уникальностью проекта в django

# ALLOWED_HOSTS нужен когда мы будем размещать адрес сервера, адрес где у нас находится django проект.

# INSTALLED_APPS - какие модели используются в нашем проекте. Любое приложение в django - модуль.

# MIDDLEWARE - прослойка, которая может влиять на запрос, вносить в него изменения, или вообще его оклонять
# Вспомни, когда ты устанавливаешь приложение tool-bar которое подсчитывает sql запросы (и не только)
# ты вносишь изменения в middleware

# TEMPLATES - настройки для подключения шаблонов
# в значении ключа DIRS мы указываем где искать шаблоны
# (os.path.join(BASE_DIR, templates) - объединить корень проекта с templates)

# WSGI_APPLICATION - модуль для подключения сервера, чтобы это не значило.

# DATABASES - настройка для подключения и использования базы данных в проекте
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# AUTH_PASSWORD_VALIDATORS - валидаторы паролей, ша


# Internationalization Интернационализация
# https://docs.djangoproject.com/en/3.1/topics/i18n/
# LANGUAGE_CODE = 'en-us' - язык админки
#
# TIME_ZONE = 'UTC' - часовой пояс или таймзона
#
# USE_I18N = True
#
# USE_L10N = True
#
# USE_TZ = True - тоже к таймзоне относится


# STATIC_URL = '/static/' - адрес, где у нас будут находиться файлы статики

# BASE_DIR - говорит нам о том, где находится manage.py, т.е. корень проекта (находится вверху settings.py)


# ==========================================================================================
"""
Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git
Git Git GIT Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git
Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git Git
"""
# Если подсвечиваются красным, это говорит, то они не под присмотром Git

# Файлы с точкой, это скорее всего гитовские файлы.

# В .gitignore мы записываем файлы и папки, которые не должны попадать в репозиторий
# данные берутся так - прописываешь в поисковике gitignore django pycharm
# и там будут сайты с текстом, по типу того, то указан в .gitignore сейчас
# нужно перекинуть содержимое нужного сайта в .gitignore

# создать тренировочный аккаунт на github и потренироваться на нем. Или использовать уже имеющийся