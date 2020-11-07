from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required

import uuid


from .models import Question
from .models import Answer
from .forms import AskForm
from .forms import AnswerForm
from .forms import SignupForm
from .forms import LoginForm


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

@login_required
def question_view(request, pk=0):
	question = get_object_or_404(Question, id=pk)
	answers = Answer.objects.answers_for_question(pk)
	if request.method == "POST":
		form = AnswerForm(request.POST)
		if form.is_valid():
			answer = form.save()
			answer.author = request.user
			answer.save()
			return HttpResponseRedirect(reverse(question_view, kwargs={'pk': question.id}))
	else:
		form = AnswerForm(initial={"question": question.pk})

	return render(request, 'pages/question.html', {
		    'title': question.title,
		    'question': question.text,
		    'answers': answers,
			'form': form
	})

@login_required
def question_add(request):
	if request.method == "POST":
		form = AskForm(request.POST)
		if form.is_valid():
			question = form.save()
			question.author = request.user
			question.save()
			return HttpResponseRedirect(reverse(question_view, kwargs={'pk': question.id}))
	else:
		form = AskForm()
	return render(request, 'pages/ask.html', {
	'form': form
	})


def signup_view(request):
	if request.method == "POST":
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save()
			User.objects.create_user(user.username, user.email, user.password)
			user = authenticate(username=user.username, password=user.password)
			login(request, user)
			return HttpResponseRedirect('/')
	else:
		form = SignupForm()
	return render(request, 'pages/ask.html', {
	'form': form
	})

def login_view(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			user = form.save()
			user = authenticate(username=user.username, password=user.password)
			if user is not None:
				response = HttpResponseRedirect('/')
				response.set_cookie('sessid', uuid.uuid4(),
									domain='.site.com', httponly=True,
									expires = datetime.now()+timedelta(days=5)
)
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				form = LoginForm
				return render(request, 'pages/ask.html', {
					'form': form
				})

	else:
		form = LoginForm()
	return render(request, 'pages/ask.html', {
	'form': form
	})


