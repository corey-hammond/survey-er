from django import forms 
from .models import Question, Choice

class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('question_text', 'topic', 'pub_date',)