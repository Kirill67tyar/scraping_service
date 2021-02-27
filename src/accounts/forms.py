from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate
from scraping.models import Language, City
from scraping.utils import get_object_or_null


User = get_user_model()




class RegistrationUserForm(forms.ModelForm):

    password = forms.CharField(label='Введите пароль',
                               required=True, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control',}))
    password2 = forms.CharField(label='Введите пароль еще раз', 
                                required=True, 
                                widget=forms.PasswordInput(attrs={'class': 'form-control',}))



    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'password2', 'mailing',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            # 'mailing': forms.NullBooleanSelect(attrs={'class': 'form-control'}),
            # 'password': forms.PasswordInput(attrs={'class': 'form-control',}),
            # 'password2': forms.PasswordInput(attrs={'class': 'form-control',})
        }
        labels = {
            'email': 'Введите email',
            'mailing': 'Согласны ли вы на email рассылку? ',
        }
        

    def clean_password2(self, *args, **kwargs):
        data = self.cleaned_data
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2







class LoginUserForm(forms.Form):

    email = forms.CharField(label='Email', 
                            required=True,
                            widget=forms.EmailInput(attrs={'class': 'form-control',}))
    password = forms.CharField(label='Password',
                               required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',}))
    
    def clean(self, *args, **kwargs):
        email = self.cleaned_data['email'].strip()
        password = self.cleaned_data['password'].strip()
        user_exists = get_object_or_null(User, email=email)
        
        if not user_exists:
            raise forms.ValidationError('Такого пользователя не существует')
        if not check_password(password, user_exists.password):
            raise forms.ValidationError('Пароль не верный')
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError('Данный аккаунт отключен')
        
        return super(LoginUserForm, self).clean(*args, **kwargs)



class UpdateUserForm(forms.ModelForm):

    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  to_field_name='slug',
                                  required=True,
                                  widget=forms.Select(attrs={'class': 'form-select',}),
                                  label='Город')
    language = forms.ModelChoiceField(queryset=Language.objects.all(),
                                      to_field_name='slug',
                                      required=True,
                                      widget=forms.Select(attrs={'class': 'form-select',}),
                                      label='Язык программрования')
    mailing = forms.BooleanField(required=False,
                                 widget=forms.CheckboxInput,
                                 label='Получать рассылку')

    class Meta:
        model = get_user_model()
        fields = ('city', 'language', 'mailing',)





class ContactForm(forms.Form):

    city = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           label='Город')
    language = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control',}),
                               label='Язык программирования')
    email = forms.CharField(required=True,
                            widget=forms.EmailInput(attrs={'class': 'form-control',}),
                            label='Ваш email')


        
# фукнция check_password - шифрует пароль (возможно хеширует), и проверяет равен ли паролю, полученному у пользователя
