
from django.shortcuts import render, redirect
from main import models
from django.http import HttpResponse
from datetime import datetime
from django.utils import timezone


def create_result(id):
    quiz_taker = models.QuizTaker.objects.get(id=id)
    correct = 0
    incorrect = 0
    for object in models.Answer.objects.filter(taker=quiz_taker):
        if object.is_correct:
            correct +=1
        else:
            incorrect +=1

    models.Result.objects.create(
        taker=quiz_taker,
        correct_answers=correct,
        incorrect_answers=incorrect
    )


def quiz_detail(request, code):
    quiz = models.Quiz.objects.get(code=code)
    if quiz.is_active == False:
        return HttpResponse('Inactive')
    elif quiz.limited_date and (timezone.now() < quiz.start_date or quiz.limited_date < timezone.now()):
        quiz.is_active = False
        return HttpResponse('unavailable quiz')     
    else:
        questions = models.Question.objects.filter(
            quiz = quiz
        )
        context = {
            'quiz':quiz,
            'questions':questions
        }
        return render(request, 'front/quiz-detail.html', context)


def create_answers(request, code):
    quiz = models.Quiz.objects.get(code=code)
    if (quiz.limited_date and quiz.limited_date < timezone.now()) or not quiz.limited_date:
        full_name = request.POST['full_name']
        phone = request.POST['phone']
        email = request.POST.get('email')
        quiz_taker = models.QuizTaker.objects.create(
            full_name=full_name,
            phone=phone,
            email=email,
            quiz=quiz
        )

        for key, value in request.POST.items():
            if key.isdigit():
                models.Answer.objects.create(
                    taker=quiz_taker,
                    question_id=int(key),
                    answer_id=int(value)
                )
        create_result(quiz_taker.id)
        return redirect('front:success', quiz_taker.id)
    else:
        quiz.is_active = False 
        quiz.save()
        return HttpResponse('Time had been already over, your answers were will not be written to the database')

def success(request, id):
    taker = models.QuizTaker.objects.get(id = id)
    result = models.Result.objects.get(taker = taker)
    answers = models.Answer.objects.filter(taker=result.taker)
    context = {
        'result' : result,
        'taker':result.taker,
        'answers':answers
    }
    return render(request, 'front/success.html', context)