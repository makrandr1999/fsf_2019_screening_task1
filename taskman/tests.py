from django.test import RequestFactory, TestCase
from .models import Task,Team,Comment
from django.contrib.auth.models import User
from django.urls import reverse
from .views import teams

# Create your tests here.
usera = User(pk=10,username='tomisbest0', password='tom123456789')
usera.save()
userb = User(pk=11,username='zack0', password='zack')
userb.save()

class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user1 = User(pk=1,username='tomisbest', password='tom123456789')
        user1.save()
        user2 = User(pk=2,username='zack', password='zack')
        user2.save()
        team = Team(pk=1,name='Team 1',creator=user1.username)
        team.save()
        team.members.set(User.objects.all())
        team.save() 
        task=Task(pk=1,creator=user1,title='test title',text='test title description',team=team,status='Planned')
        task.save()
        task.assignee.set(User.objects.filter(id=1))
        task.save()
        

    def test_tasks_data_check(self):
        task = Task.objects.get(pk=1)
        assignees=task.assignee.get(username='tomisbest')
        self.assertEqual(assignees.username,'tomisbest')
        self.assertEqual(task.creator.username, 'tomisbest')
        self.assertEqual(task.title, 'test title')
        self.assertEqual(task.text, 'test title description')
        self.assertEqual(task.status, 'Planned')
        self.assertEqual(task.team.name, 'Team 1')
    

    
    def test_title_max_length(self):
        task = Task.objects.get(pk=1)
        max_length = task._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)
    '''
    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEquals(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(author.get_absolute_url(), '/catalog/author/1')
    '''
    
class TeamModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User(pk=3,username='tomisworst', password='tom123456789')
        user1.save()
        user2 = User(pk=4,username='zackisbest', password='zack')
        user2.save()
        team = Team(pk=1,name='Team abc',creator=user1.username)
        team.save()
        team.members.set(User.objects.all())
        team.save() 

    def test_team_data_check(self):
        team = Team.objects.get(pk=1)
        self.assertEqual(team.name,'Team abc')
        self.assertEqual(team.creator, 'tomisworst')
        self.assertEqual(team.members.all()[0].username,'tomisworst')
        self.assertEqual(team.members.all()[1].username,'zackisbest')

    def test_name_max_length(self):
        team = Team.objects.get(pk=1)
        max_length = team._meta.get_field('name').max_length
        self.assertEquals(max_length, 64)    

class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User(pk=1,username='tomisbest', password='tom123456789')
        user1.save()
        user2 = User(pk=2,username='zack', password='zack')
        user2.save()
        team = Team(pk=1,name='Team 1',creator=user1.username)
        team.save()
        team.members.set(User.objects.all())
        team.save() 
        task=Task(pk=1,creator=user1,title='test title',text='test title description',team=team,status='Planned')
        task.save()
        task.assignee.set(User.objects.filter(id=1))
        task.save()
        comment=Comment(pk=1,task=task,author=user1.username,text='Awesome work')
        comment.save()

    def test_comment_data_check(self):
        comment = Comment.objects.get(pk=1)
        self.assertEqual(comment.task.title,'test title')
        self.assertEqual(comment.author, 'tomisbest')
        self.assertEqual(comment.text,'Awesome work')

    
    def test_name_max_length(self):
        team = Team.objects.get(pk=1)
        max_length = team._meta.get_field('name').max_length
        self.assertEquals(max_length, 64) 
         
def create_team(name,members,creator):
    return Team.objects.create(name=name,members=members,creator=creator)

class TeamIndexViewTests(TestCase):

    def test_no_teams(self):
        User.objects.create_user(username='tomisbest10', password='tom123456789')
        login = self.client.login(username='tomisbest10', password='tom123456789') 
        self.assertTrue(login)
        #response = self.client.get(reverse('taskman:teams'))
        #self.client.login(username='tomisbest0', password='tom123456789')
        response = self.client.get('/teams/', follow=True)
        #response = self.client.get(reverse('taskman:teams'), {'user_id': 'tomisbest0'},follow=True)
        #self.client.force_login(self.user)
        #print('hello')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You aren't a part of any team")
        #self.assertQuerysetEqual(response.context['teams'], [])    
class DashBoardIndexViewTests(TestCase):

    def test_no_tasks(self):
        User.objects.create_user(username='tomisbest10', password='tom123456789')
        login = self.client.login(username='tomisbest10', password='tom123456789') 
        self.assertTrue(login)
        response = self.client.get('/dashboard/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no tasks assigned")      



