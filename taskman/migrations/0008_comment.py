# Generated by Django 2.1.7 on 2019-03-15 13:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('taskman', '0007_auto_20190313_0941'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('task', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='comments', to='taskman.Task')),
            ],
        ),
    ]
