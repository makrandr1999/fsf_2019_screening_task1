from django import forms

from .models import Task,Team,Comment
from django.contrib.auth.models import User
from django.db.models import Q



class TeamForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ('name','members')

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('assignee','title','text','status',)

    
       
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['assignee'].required = True
   
       
    

        
        
    
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
class SelectTeamForm(forms.Form):
    team = forms.ModelChoiceField(queryset=None, empty_label="Leave this field blank and click on proceed to set assignee as self")
    

    def __init__(self,request,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team'].required = False
        teams= Team.objects.filter(Q(members__username=request.user) | Q(creator =request.user)).distinct()
        if not teams:
            self.fields['team'].queryset = Team.objects.none()
        else:
             self.fields['team'].queryset = teams

       
    
    class Meta:
        fields = ('team',)
    
    
        
           

           


