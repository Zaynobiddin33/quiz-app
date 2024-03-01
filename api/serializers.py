from rest_framework.serializers import ModelSerializer
from main.models import *

class QuizSerializer(ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"

class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

class OptionSerializer(ModelSerializer):
    class Meta:
        model = Option
        fields = "__all__"

class QuiztakerSerializer(ModelSerializer):
    class Meta:
        model = QuizTaker
        fields = "__all__"

class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"

class ResultSerializer(ModelSerializer):
    class Meta:
        model = Result
        fields = "__all__"