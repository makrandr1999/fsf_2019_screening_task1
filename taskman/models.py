from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=64)
    members = models.ManyToManyField(User)
    creator = models.CharField(max_length=200,default="admin")

    def __str__(self):
        return self.name

class Task(models.Model):
    PLANNED='Planned'
    INPROGRESS='InProgress'
    DONE='Done'
    STATUS_CHOICES = (
        (PLANNED, 'Planned'),
        (INPROGRESS, 'InProgress'),
        (DONE, 'Done'),
    )
    creator = models.ForeignKey('auth.User',verbose_name="Creator",default=1,on_delete=models.SET_DEFAULT)
    assignee = models.ManyToManyField('auth.User',related_name='assignee',default=User)
    title = models.CharField(max_length=200)
    text = models.TextField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE,default=1)
    published_date = models.DateTimeField(
            blank=True, null=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PLANNED,
    )       

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    #def approved_comments(self):
    #    return self.comments.filter(approved_comment=True)

   

# Create your models here.
class Comment(models.Model):
    task = models.ForeignKey('Task', related_name='comments',default=1,on_delete=models.SET_DEFAULT)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    #approved_comment = models.BooleanField(default=False)
    '''
    def approve(self):
        self.approved_comment = True
        self.save()
    '''    

    def __str__(self):
        return self.text
# Create your models here.
 