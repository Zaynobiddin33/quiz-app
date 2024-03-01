from django.urls import path
from . import views

app_name = 'front'

urlpatterns = [
    path('quiz/z<str:code>', views.quiz_detail, name='quiz_detail'),
    path('answer/<str:code>', views.create_answers, name='create_answers'),
    path('success/<int:id>', views.success, name = 'success')
]