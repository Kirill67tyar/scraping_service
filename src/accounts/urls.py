from django.urls import path
from accounts.views import (login_view, logout_view, registration_view, update_view, delete_view, contact_view)

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registration/', registration_view, name='registration'),
    path('update/', update_view, name='update'),
    path('delete/', delete_view, name='delete'),
    path('contact/', contact_view, name='contact'),
]


