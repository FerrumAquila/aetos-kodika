# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_it', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sticky',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(max_length=1000)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StickyOnSticky',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('reply_sticky', models.ForeignKey(related_name='posted_on', to='post_it.Sticky')),
                ('top_sticky', models.ForeignKey(related_name='posted_for', to='post_it.Sticky')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='feedtweet',
            name='tweet',
        ),
        migrations.RemoveField(
            model_name='followuser',
            name='follower',
        ),
        migrations.RemoveField(
            model_name='followuser',
            name='following',
        ),
        migrations.RemoveField(
            model_name='newsfeed',
            name='listener',
        ),
        migrations.RemoveField(
            model_name='newsfeed',
            name='tweets',
        ),
        migrations.RemoveField(
            model_name='timeline',
            name='tweeter',
        ),
        migrations.RemoveField(
            model_name='timeline',
            name='tweets',
        ),
        migrations.RemoveField(
            model_name='timelinetweet',
            name='tweet',
        ),
        migrations.RemoveField(
            model_name='tweet',
            name='author',
        ),
        migrations.RemoveField(
            model_name='tweet',
            name='tags',
        ),
        migrations.AlterUniqueTogether(
            name='tweetlike',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='tweetlike',
            name='liked_by',
        ),
        migrations.RemoveField(
            model_name='tweetlike',
            name='tweet',
        ),
        migrations.RemoveField(
            model_name='tweetreply',
            name='parent_tweet',
        ),
        migrations.RemoveField(
            model_name='tweetreply',
            name='reply_tweet',
        ),
        migrations.AddField(
            model_name='profiledetails',
            name='following',
            field=models.ManyToManyField(related_name='_following_+', to='post_it.ProfileDetails'),
        ),
        migrations.DeleteModel(
            name='FeedTweet',
        ),
        migrations.DeleteModel(
            name='FollowUser',
        ),
        migrations.DeleteModel(
            name='NewsFeed',
        ),
        migrations.DeleteModel(
            name='Timeline',
        ),
        migrations.DeleteModel(
            name='TimelineTweet',
        ),
        migrations.DeleteModel(
            name='Tweet',
        ),
        migrations.DeleteModel(
            name='TweetLike',
        ),
        migrations.DeleteModel(
            name='TweetReply',
        ),
        migrations.AddField(
            model_name='sticky',
            name='author',
            field=models.ForeignKey(related_name='stickies', to='post_it.ProfileDetails'),
        ),
        migrations.AddField(
            model_name='sticky',
            name='tags',
            field=models.ManyToManyField(related_name='tagged_in', to='post_it.ProfileDetails'),
        ),
    ]
