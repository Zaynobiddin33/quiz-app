from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from openpyxl import Workbook
from io import BytesIO
from datetime import datetime, timedelta
from django.utils import timezone

# Create your views here.
@login_required(login_url = 'dash:login')
def main(request):
    quizes = Quiz.objects.filter(author = request.user)
    context = {
        "quizes" : quizes,
        'main': request.build_absolute_uri()
    }
    return render(request, 'main.html', context)


@login_required(login_url = 'dash:login')
def create_quiz(request):
    if request.method == 'POST':
        title = request.POST['title']
        limit = request.POST['limit']
        start = request.POST['start']
        if not start:
            start = timezone.now()
        if limit:
            quiz = Quiz.objects.create(
                title = title,
                author = request.user,
                limited_date = limit,
                start_date = start
            )
        else:
            quiz = Quiz.objects.create(
                title = title,
                author = request.user,
                start_date = start
            )
        return redirect('dash:quest_create', quiz.id)
    return render(request, 'quiz/create-quiz.html')


@login_required(login_url = 'dash:login')
def create_question(request, id):
    print(request.POST)

    quiz = Quiz.objects.get(id = id)
    if request.method == 'POST':
        title = request.POST['title']
        ques = Question.objects.create(
            quiz = quiz,
            title = title
        )
        Option.objects.create(
            question = ques,
            name = request.POST['correct'],
            is_correct = True
        )
        for i in range(int(request.POST['input-count'])):
            string = 'incorrect' + str(i)
            Option.objects.create(
                question = ques,
                name = request.POST[string]
            )
        if request.POST['submit_action'] == 'exit':
            return redirect('dash:main')
            
    return render (request, 'quiz/create-question.html')


@login_required(login_url = 'dash:login')
def questions_list(request, id):
    quests = Question.objects.filter(quiz_id = id)
    context = {
        'questions': quests
    }
    return render (request, 'details/questions.html', context)

@login_required(login_url = 'dash:login')
def quest_detail(request, id):
    question = Question.objects.get(id = id)
    option_correct = Option.objects.get(question = question, is_correct = True)
    options = Option.objects.filter(question = question, is_correct = False).order_by('id')
    context = {
        'question': question,
        'options': options,
        'option_correct' : option_correct
    }
    if request.method == 'POST':
        question.title = request.POST['title']
        question.save()

        option_correct.name = request.POST['correct']
        option_correct.save()

        data = [request.POST['incorrect1'], request.POST['incorrect2'], request.POST['incorrect3']]

        for i, opt in enumerate(options):
            opt.name = data[i]
            opt.save()
    return render( request, 'details/detail.html', context)

@login_required(login_url = 'dash:login')
def quiz_delete(request, id):
    Quiz.objects.get(id = id).delete()
    return redirect('dash:main')


@login_required(login_url = 'dash:login')
def get_results(request, id):
    quiz = Quiz.objects.get(id=id)
    taker = QuizTaker.objects.filter(quiz=quiz)

    # results = []
    # for i in taker:
    #     results.append(Result.objects.get(taker=i))
    
    results = tuple(
            map(
            lambda x : Result.objects.get(taker=x),
            taker
        )
    )
    return render(request, 'quiz/results.html', {'results':results, 'quiz':quiz})

def result_detail(request, id):
    result = Result.objects.get(id=id)
    answers = Answer.objects.filter(taker=result.taker)
    context = {
        'taker':result.taker,
        'answers':answers
    }
    return render(request, 'quiz/result-detail.html', context)

#login


def logging_in(request):
    status = False
    if request.method == 'POST':
        username = request.POST['username']
        password =  request.POST['password']
        user = authenticate(username = username, password=password)
        if user:
            login(request, user)
            return redirect('dash:main')
        else:
            status = 'incorrect username or password'
    return render(request, 'auth/login.html', {'status':status})

def register(request):
    status = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username = username).first():
            User.objects.create_user(
                username=username,
                password=password
            )
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('dash:main')
        else:
            status  = f'the username {username} is occupied'
    return render(request, 'auth/register.html', {'status': status})

def success_page(request):
    return render(request, 'quiz/success.html' )


def excel_report(request, id):
    results = Result.objects.filter(taker__quiz = Quiz.objects.get(id = id)).order_by('-correct_answers')
    wb = Workbook()
    wsh = wb.active
    headers = ['#', 'Full name', "Phone", "Email", "Total Questions", "Correct answers", "Incorrect answers", "Percentage"]
    wsh.append(headers)
    for i , result in enumerate(results):
        if not result.taker.email:
            email = 'No'
        else:
            email = result.taker.email
        row_data = [i+1, result.taker.full_name, result.taker.phone, email, result.questions, result.correct_answers, result.incorrect_answers, f"{result.percentage}%"]
        wsh.append(row_data)

    for col in wsh.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        changed_width = (max_length + 2) * 1.2
        wsh.column_dimensions[column].width = changed_width

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="incomes.xlsx"'
    return response

def activate_deactivate(request, id):
    previous = request.META['HTTP_REFERER']
    quiz = Quiz.objects.get(id = id)
    if quiz.is_active == True:
        quiz.is_active = False
        quiz.save()
    else:
        quiz.is_active = True
        quiz.save()
    return redirect(previous)