from django import forms
from django.forms import ModelForm

from .models import Question
from .models import Answer


class AskForm(forms.Form):
	title = forms.CharField(max_length=80)
	text = forms.CharField(widget=forms.Textarea)

	def clean(self):
		return self.cleaned_data

	def save(self):
		question = Question(**self.clean())
		question.save()
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
		answer.save()
		return answer
