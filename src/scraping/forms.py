from django import forms
from scraping.models import City, Language, Vacancy


class SearchForm(forms.Form):

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        to_field_name='slug',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control',}),
        label='Город'
    )

    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        to_field_name='slug',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control',}),
        label='Язык'
    )


class ExperimentSearchForm(forms.Form):

    main_field = forms.CharField(required=False,
                                 label="Эксперимент",
                                 widget=forms.TextInput(attrs={'name': 'anything'}))
