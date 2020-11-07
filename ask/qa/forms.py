from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Question
from .models import Answer

class SignupForm(forms.Form):
	username = forms.CharField(max_length=100)
	email = forms.CharField(max_length=100)
	password = forms.CharField(max_length=100)

	def clean(self):
		return self.cleaned_data

	def save(self):
		user = User(**self.clean())
		return user

class LoginForm(forms.Form):
	username = forms.CharField(max_length=100)
	password = forms.CharField(max_length=100)

	def clean(self):
		return self.cleaned_data

	def save(self):
		user = User(**self.clean())
		return user

class AskForm(forms.Form):
	title = forms.CharField(max_length=80)
	text = forms.CharField(widget=forms.Textarea)

	def clean(self):
		return self.cleaned_data

	def save(self):
		question = Question(**self.clean())
		return question

class AnswerForm(ModelForm):
	class Meta:
		# exclude = ['question']
		model = Answer
		fields = ['text', 'question']

	def __init__(self, *args, **kwargs):
		super(AnswerForm, self).__init__(*args, **kwargs)
		self.fields['question'].widget = forms.HiddenInput()

	def clean(self):
		return self.cleaned_data

	def save(self):
		answer = Answer(**self.clean())
		return answer
