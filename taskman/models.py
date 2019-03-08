from django.db import models
from django.utils import timezone


class Task(models.Model):
    PLANNED='Planned'
    INPROGRESS='InProgress'
    DONE='Done'
    STATUS_CHOICES = (
        (PLANNED, 'Planned'),
        (INPROGRESS, 'InProgress'),
        (DONE, 'Done'),
    )
    assignee = models.ForeignKey('auth.User',verbose_name="Assignee",default=1,on_delete=models.SET_DEFAULT)
    title = models.CharField(max_length=200)
    text = models.TextField()
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
'''
# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey('Task', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
# Create your models here.
 '''