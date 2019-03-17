from django import forms

from .models import Task,Team,Comment
from django.contrib.auth.models import User


class TeamForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ('name','members')

class TaskForm(forms.ModelForm):
    #team = forms.ModelChoiceField(queryset=Team.objects.filter(members__username=User))
    class Meta:
        model = Task
        fields = ('assignee','title','text','status')
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
    
       
    def __init__(self,teamid,*args, **kwargs):
        super().__init__(*args, **kwargs)
        i=Team.objects.filter(id=teamid)
        self.fields['assignee'].queryset =i[0].members.all()
        #self.fields['assignee'].queryset = Team.objects.none()
    
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
class SelectTeamForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('team',)
    def __init__(self,request,*args, **kwargs):
        super().__init__(*args, **kwargs)
        teams= Team.objects.filter(members__username=request.user)
        if not teams:
           self.fields['team'].queryset = 'self'
        else:
           self.fields['team'].queryset = teams    
        #self.fields['assignee'].queryset = Team.objects.none()    


