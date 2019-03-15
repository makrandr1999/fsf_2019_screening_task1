from django import forms

from .models import Task,Team
from django.contrib.auth.models import User


class TeamForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ('name','members')

class TaskForm(forms.ModelForm):
    #team = forms.ModelChoiceField(queryset=Team.objects.filter(members__username=User))
    class Meta:
        model = Task
        fields = ('team','assignee','title','text','status')
        '''
        city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        label=u"City",
        widget=ModelSelect2Widget(
            model=City,
            search_fields=['name__icontains'],
            dependent_fields={'country': 'country'},
            max_results=500,
        )
    )
       '''

        
    def __init__(self,request,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team'].queryset = Team.objects.filter(members__username=request.user)
        #self.fields['assignee'].queryset = Team.objects.none()
        

