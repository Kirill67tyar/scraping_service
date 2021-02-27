from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from accounts.forms import LoginUserForm, RegistrationUserForm, UpdateUserForm, ContactForm
from scraping.utils import get_object_or_null
from scraping.models import Error
from datetime import date

User = get_user_model()

def login_view(request):

    form = LoginUserForm(request.POST or None)
    # print(f'\n\n###################################\n'
    #       f'form - {form}\n'
    #       f'#######################################\n\n')
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        messages.info(request, f'Добро пожаловать {email}')
        return redirect(reverse('scraping:home'))
    return render(request, template_name='accounts/login.html', context={'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse('accounts:login'))


def registration_view(request):
    
    form = RegistrationUserForm(request.POST or None)
    if form.is_valid():

        data = form.cleaned_data
        new_user = form.save(commit=False)
        new_user.set_password(data.get('password2'))
        new_user.save()
        messages.success(request, 'Вы успешно зарегистрировались')
        # login(request, new_user)
        return render(request, 'accounts/register_done.html', context={'new_user': new_user,})
    return render(request=request, template_name='accounts/registration.html', context={'form': form,})


def update_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':

            form = UpdateUserForm(instance=user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Данные сохранены')

                
                
                return redirect(reverse('accounts:update'))
            else:
                messages.error(request, 'Что-то пошло не так')
                return render(request, 'accounts/update_user.html', {'form': form, })
            
        elif request.method == 'GET':
            # form = UpdateUserForm(instance=user)
            form = UpdateUserForm(initial={'city': user.city, 
                                           'language': user.language,
                                           'mailing': user.mailing,})
            return render(request, 'accounts/update_user.html', {'form': form,})
        
    else:
        return redirect(reverse('accounts:login'))


def delete_view(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            user.delete()
            messages.info(request, 'Удаление прошло успешно')
    return redirect('accounts:registration')


def contact_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                feedback = [{'city': data.get('city'),
                            'language': data.get('language'),
                            'email': data.get('email')},]
                today = date.today()
                err = get_object_or_null(Error, datestamp=today)
                if err:
                    err.data['feedback'].extend(feedback)
                    err.save()
                else:
                    Error.objects.create(data={'errors': [], 'feedback': feedback,})
                messages.info(request, 'Данные отправлены нашей администрации')
                return redirect(reverse('scraping:home'))


        elif request.method == 'GET':
            form = ContactForm()
        return render(request, 'accounts/contact.html', context={'form': form,})
    return redirect('accounts:registration')
