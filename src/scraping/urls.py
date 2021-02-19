from django.urls import path
from scraping.views import form_view, list_view, experiments

app_name = 'scraping'

urlpatterns = [
    path('', form_view, name='home'),
    path('list/', list_view, name='vacancy_list'),
    path('experiment/', experiments),

]
