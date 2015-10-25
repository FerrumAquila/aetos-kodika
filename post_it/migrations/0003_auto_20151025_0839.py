# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post_it', '0002_auto_20151025_0739'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(unique=True, max_length=50)),
                ('gender', models.CharField(max_length=2)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('data', models.TextField(blank=True)),
                ('following', models.ManyToManyField(related_name='_following_+', to='post_it.Profile')),
                ('user', models.ForeignKey(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='profiledetails',
            name='following',
        ),
        migrations.RemoveField(
            model_name='profiledetails',
            name='user',
        ),
        migrations.AlterField(
            model_name='sticky',
            name='author',
            field=models.ForeignKey(related_name='stickies', to='post_it.Profile'),
        ),
        migrations.AlterField(
            model_name='sticky',
            name='tags',
            field=models.ManyToManyField(related_name='tagged_in', to='post_it.Profile'),
        ),
        migrations.DeleteModel(
            name='ProfileDetails',
        ),
    ]
