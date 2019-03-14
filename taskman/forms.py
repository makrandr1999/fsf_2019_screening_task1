from django import forms

from .models import Task,Team

class TeamForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ('name','members')

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('creator','team','assignee','title','text','status')
