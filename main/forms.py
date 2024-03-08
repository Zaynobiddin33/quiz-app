from django import forms
from .models import *

class QuizForm(forms.ModelForm):

      class Meta:
          model = Quiz
          fields = "__all__"
          exclude = ('code', 'author', 'is_active')
          widgets = {
               'title' :  forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Quiz name" , 'name':"title"}),
                'start_date' : forms.TextInput(attrs={'class':"form-control", 'name':"start", 'type':'datetime-local'}),
                'limited_date' : forms.TextInput(attrs={'class':"form-control", 'name':"limit", 'type':'datetime-local'})
          }