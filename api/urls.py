from django.urls import path
from . import views

urlpatterns = [
    path('quizes', views.quizes, name = 'quiz_detail'),
    path('quiz-detail/<int:id>', views.quiz_detail, name = 'quiz_detail'),
    path('question-detail/<int:id>', views.question_detail, name = 'question_detail'),
    path('create_answers/<str:code>', views.create_answers, name = 'create_answers')
    
    

]