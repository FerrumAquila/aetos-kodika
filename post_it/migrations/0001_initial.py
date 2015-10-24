# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedTweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('order', models.PositiveSmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FollowUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NewsFeed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProfileDetails',
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
                ('user', models.ForeignKey(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Timeline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('tweeter', models.ForeignKey(related_name='timeline', to='post_it.ProfileDetails')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TimelineTweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('order', models.PositiveSmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(max_length=1000)),
                ('author', models.ForeignKey(related_name='tweets', to='post_it.ProfileDetails')),
                ('tags', models.ManyToManyField(related_name='tagged_in', to='post_it.ProfileDetails')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TweetLike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('liked_by', models.ForeignKey(related_name='liked_tweets', to='post_it.ProfileDetails')),
                ('tweet', models.ForeignKey(related_name='liked_by_profiles', to='post_it.Tweet')),
            ],
        ),
        migrations.CreateModel(
            name='TweetReply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('parent_tweet', models.ForeignKey(related_name='parent_to', to='post_it.Tweet')),
                ('reply_tweet', models.ForeignKey(related_name='replies_to', to='post_it.Tweet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='timelinetweet',
            name='tweet',
            field=models.ForeignKey(related_name='timeline_item', to='post_it.Tweet'),
        ),
        migrations.AddField(
            model_name='timeline',
            name='tweets',
            field=models.ManyToManyField(related_name='timelines', to='post_it.TimelineTweet'),
        ),
        migrations.AddField(
            model_name='newsfeed',
            name='listener',
            field=models.ForeignKey(related_name='news_feed', to='post_it.ProfileDetails'),
        ),
        migrations.AddField(
            model_name='newsfeed',
            name='tweets',
            field=models.ManyToManyField(related_name='news_feeds', to='post_it.FeedTweet'),
        ),
        migrations.AddField(
            model_name='followuser',
            name='follower',
            field=models.ForeignKey(related_name='follows', to='post_it.ProfileDetails'),
        ),
        migrations.AddField(
            model_name='followuser',
            name='following',
            field=models.ForeignKey(related_name='followers', to='post_it.ProfileDetails'),
        ),
        migrations.AddField(
            model_name='feedtweet',
            name='tweet',
            field=models.ForeignKey(related_name='news_feed_item', to='post_it.Tweet'),
        ),
        migrations.AlterUniqueTogether(
            name='tweetlike',
            unique_together=set([('tweet', 'liked_by')]),
        ),
    ]
