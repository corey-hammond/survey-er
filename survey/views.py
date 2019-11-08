from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice
from .forms import QuestionForm

# GENERIC VIEW
class IndexView(generic.ListView):
    template_name = 'survey/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # Return the last five published questions (not including those set to be published in the future).
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

# FUNCTION BASED VIEW
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list' : latest_question_list,}
#     return render(request, 'survey/index.html', context)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'survey/detail.html'

    def get_queryset(self):
        # Excludes any questions that aren't published yet.
        return Question.objects.filter(pub_date__lte=timezone.now())

# def detail(request, pk):
#     question = get_object_or_404(Question, pk=pk)
#     return render(request, 'survey/detail.html', {'question': question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'survey/results.html'

# def results(request, pk):
#     question = get_object_or_404(Question, pk=pk)
#     return render(request, 'survey/results.html', {'question': question})

def vote(request, pk):
    question = get_object_or_404(Question, pk=pk)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'survey/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('survey:results', args=(pk,)))

def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            return redirect('survey:detail', pk=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'survey/question_form.html', {'form': form})

def question_edit(request, pk):
    question = Question.objects.get(pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect('survey:detail', pk=question.pk)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'survey/question_form.html', {'form': form})

def question_delete(request, pk):
    Question.objects.get(id=pk).delete()
    return redirect('survey:index')
