from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator


from .models import Question
from .models import Answer

# Create your views here.

def test(request, *args, **kwargs):
	return render(request, 'base.html')


def main_page_view(request, *args, **kwargs):
	questions = Question.objects.new()
	page = request.GET.get('page', 1)

	limit = 10
	paginator = Paginator(questions, limit)
	paginator.baseurl = '/?page='
	page = paginator.page(page)

	return render(request, 'pages/main_page.html', {
		'questions': page.object_list,
		'paginator': paginator, 'page': page
	})


def popular_view(request, *args, **kwargs):
	questions = Question.objects.popular()
	page = request.GET.get('page', 1)
	limit = 10
	paginator = Paginator(questions, limit)
	paginator.baseurl = '/popular/?page='
	page = paginator.page(page)

	return render(request, 'pages/popular.html', {
		'questions': page.object_list,
		'paginator': paginator, 'page': page
	})


def question_view(request, pk=0):
	question = get_object_or_404(Question, id=pk)
	answers = Answer.objects.answers_for_question(pk)
	return render(request, 'pages/question.html', {
		    'title': question.title,
		    'question': question.text,
		    'answers': answers
	})