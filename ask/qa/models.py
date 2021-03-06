from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models



# Create your models here.

class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-id')
    def popular(self):
        return self.order_by('-rating')

class Question(models.Model):
    objects = QuestionManager()
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='likes_set')

def __str__(self):
    return (self.title)


class AnswerManager(models.Manager):
    def answers_for_question(self, pk):
        return self.filter(question_id=pk)


class Answer(models.Model):
    objects = AnswerManager()
    text = models.TextField()
    added_at = models.DateTimeField( auto_now_add=True)
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
