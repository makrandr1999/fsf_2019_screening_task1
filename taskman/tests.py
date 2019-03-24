from django.test import TestCase
from .models import Task,Team,Comment
from django.contrib.auth.models import User

# Create your tests here.

'''
user2 = User(pk=2,username='zack', password='zack')
user2.save()
'''

class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        #user=User.objects.get(id=11)
        user1 = User(pk=1,username='tomisbest', password='tom123456789')
        user1.save()
        team = Team(pk=1,name='Team 1',creator=user1.username)
        team.save()
        team.members.set(User.objects.all())
        team.save() 
        task=Task(pk=1,creator=user1,title='test title',text='test title description',team=team,status='Planned')
        task.save()
        task.assignee.set(User.objects.filter(id=1))
        task.save()
        

    def test_data_test(self):
        task = Task.objects.get(pk=1)
        assignees=task.assignee.get(username='tomisbest')
        self.assertEquals(assignees.username,'tomisbest')
        self.assertEqual(task.creator.username, 'tomisbest')
        self.assertEqual(task.title, 'test title')
        self.assertEqual(task.text, 'test title description')
        self.assertEquals(task.status, 'Planned')
        self.assertEquals(task.team.name, 'Team 1')
    '''
    def test_date_of_death_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label, 'died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEquals(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(author.get_absolute_url(), '/catalog/author/1')
    '''