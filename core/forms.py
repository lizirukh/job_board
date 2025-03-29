from django import forms
from .models import Vacancy, Application

class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = '__all__'

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['first_name', 'last_name', 'email', 'motivational_letter', 'cv']



