from dataclasses import fields
from unicodedata import name
from django import forms
from .models import Homework, Notes, Todo_model,Youtube
from django.contrib.auth.forms import UserCreationForm
from .models import *

class Noteform(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']

class DateInput(forms.DateInput):
    input_type = 'date'

class Homeworkform(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due': DateInput()}
        fields = ['subject','title','description','due','iS_finished']

class DashbordForm(forms.ModelForm):
    class Meta:
        model = Youtube
        fields = "__all__"
    
class Todoform(forms.ModelForm):
    class Meta:
        model = Todo_model
        fields = ['title','iS_finished']


class UserRegistrationform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']



    