from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from main.models import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def create_result(id):
    quiz_taker = QuizTaker.objects.get(id=id)
    correct = 0
    incorrect = 0
    for object in Answer.objects.filter(taker=quiz_taker):
        if object.is_correct:
            correct +=1
        else:
            incorrect +=1

    Result.objects.create(
        taker=quiz_taker,
        correct_answers=correct,
        incorrect_answers=incorrect
    )

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def quizes(request):
    quizes = Quiz.objects.filter(author = request.user)
    serializer = QuizSerializer(quizes, many = True)
    return Response({'your quizes': serializer.data})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def quiz_detail(request, id):
    quiz = Quiz.objects.get(id = id)
    questions = Question.objects.filter(quiz = quiz)
    quiz_serializer = QuizSerializer(quiz)
    questions_serializer = QuestionSerializer(questions, many = True)

    context = {
        'quiz': quiz_serializer.data,
        'questions' : questions_serializer.data
    }
    return Response(context)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def question_detail(request, id):
    question = Question.objects.get(id = id)
    quiz = Quiz.objects.get(question = question)
    quiz_serializer = QuizSerializer(quiz)
    options = Option.objects.filter(question = question)
    options_serializer = OptionSerializer(options, many = True)
    question_serialezer = QuestionSerializer(question)
    context = {
    'quiz': quiz_serializer.data,
    'question' : question_serialezer.data,
    'options' : options_serializer.data
    }
    return Response(context)

api_view(["POST"])
@csrf_exempt
def create_answers(request, code):
    quiz = Quiz.objects.get(code=code)
    full_name = request.data['full_name']
    phone = request.data['phone']
    email = request.data.get('email')
    quiz_taker = QuizTaker.objects.create(
        full_name=full_name,
        phone=phone,
        email=email,
        quiz=quiz
    )

    for key, value in request.data.items():
        if key.isdigit():
            Answer.objects.create(
                taker=quiz_taker,
                question_id=int(key),
                answer_id=int(value)
            )
    create_result(quiz_taker.id)
    return Response({'detail': 'success'})