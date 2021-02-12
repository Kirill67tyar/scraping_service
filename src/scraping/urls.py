from django.urls import path
from scraping.views import home_view

app_name = 'scraping'

urlpatterns = [
    path('vacancy/', home_view, name='vacancy'),

]
