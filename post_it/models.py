from django.db import models
from django.contrib.auth.models import User

# from IPython.frontend.terminal.embed import InteractiveShellEmbed
# InteractiveShellEmbed()()


class TrackingFields(models.Model):
    """
    Each model will have these fields
    """
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProfileDetails(TrackingFields):
    user = models.ForeignKey(User, related_name='profile')
    username = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=2)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    data = models.TextField(blank=True)

    def __unicode__(self):
        return self.username + "'s Profile"

    def create_profile_init(self, user=False, email="visheshbangotra@gmail.com", username="ironeagle"):
        if user:
            self.user = user
            self.username = username
            self.email = email
            # comment above line and uncomment Email Class below
            # line +1 and +2 if you want to have multiple emails with 1 account
            # email_id = EmailID(profile=self, name="Email", email=email)
            # email_id.save()
            self.save()
        else:
            return "Error!!\nUser not found"

    def get_follow_suggestion(self):
        following_users = FollowUser.objects.filter(follower=self)
        for following in following_users:
            print("---------------Followers-------------")
            print following.following.username
        suggestions = ProfileDetails.objects.all().exclude(
            id__in=[following.following.id for following in following_users]).exclude(id=self.id)
        return suggestions.order_by("-id")

    def get_taggable_profiles(self):
        taggable = self.follows.all()
        return [follow.following for follow in taggable]


"""
class EmailID(TrackingFields):
    profile = models.ForeignKey(Profile, related_name='email_ids')
    name = models.CharField(max_length=16, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __unicode__(self):
        return self.name + " : " + self.email
"""


class Tweet(TrackingFields):
    author = models.ForeignKey(ProfileDetails, related_name='tweets')
    text = models.TextField(max_length=1000)
    tags = models.ManyToManyField(ProfileDetails, related_name='tagged_in')

    def add_liked_by(self, user=None):
        liked_by_profile = ProfileDetails.objects.get(username=user.username)
        print "===============INSIDE MODELS==============="
        if TweetLike.objects.filter(tweet=self, liked_by=liked_by_profile):
            TweetLike.objects.filter(tweet=self, liked_by=liked_by_profile).delete()
            return "remove"
        else:
            tweet_like = TweetLike(tweet=self, liked_by=liked_by_profile)
            tweet_like.save()
            self.save()
            return "add"

    def get_liked_by(self):
        tweet_likes = TweetLike.objects.filter(tweet=self)
        response = []
        for tweet_like in tweet_likes:
            response.append(tweet_like.liked_by)
        return response

    def is_liked_by(self, user):
        liked_by = self.get_liked_by()
        for user_profile in liked_by:
            if user_profile.user == user:
                return True
        return False


class TweetLike(TrackingFields):
    tweet = models.ForeignKey(Tweet, related_name='liked_by_profiles')
    liked_by = models.ForeignKey(ProfileDetails, related_name='liked_tweets')

    class Meta:
        unique_together = ('tweet', 'liked_by')


# not sure of the reply to tweet model right now
class TweetReply(TrackingFields):
    parent_tweet = models.ForeignKey(Tweet, related_name='parent_to')
    reply_tweet = models.ForeignKey(Tweet, related_name='replies_to')

    def tweet_reply(self, parent_tweet=None, reply_tweet=None):
        if not parent_tweet:
            return "parent tweet not found"
        elif not reply_tweet:
            return "reply tweet not found"
        else:
            self.parent_tweet = parent_tweet
            self.reply_tweet = reply_tweet
            self.reply_tweet.tags.add(ProfileDetails.objects.get(username=str(self.parent_tweet.author.username)))
            self.save()


# not sure whether the related_names are correct or not
# we'll see after syncdb and few fake profiles
class FollowUser(TrackingFields):
    follower = models.ForeignKey(ProfileDetails, related_name='follows')
    following = models.ForeignKey(ProfileDetails, related_name='followers')

    def follow_user(self, follower, following):
        self.follower = follower
        self.following = following
        self.save()


class FeedTweet(TrackingFields):
    tweet = models.ForeignKey(Tweet, related_name='news_feed_item')
    order = models.PositiveSmallIntegerField()


class NewsFeed(TrackingFields):
    listener = models.ForeignKey(ProfileDetails, related_name='news_feed')
    tweets = models.ManyToManyField(FeedTweet, related_name='news_feeds')

    def populate_feed(self, return_tweets=10):
        listener = self.listener
        following = listener.follows.all()

        if following.count() != 0:
            per_author_tweets = int(int(return_tweets) / int(following.count()))
        else:
            return []

        if per_author_tweets:
            pass
        else:
            per_author_tweets = 1

        tweet_sets = [follow.following.tweets.all().order_by('-id')[0:per_author_tweets] for follow in following]
        feed_tweets_ids = []
        for tweet_set in tweet_sets:
            for tweet in tweet_set:
                feed_tweets_ids.append(tweet.id)
        return feed_tweets_ids


class TimelineTweet(TrackingFields):
    tweet = models.ForeignKey(Tweet, related_name='timeline_item')
    order = models.PositiveSmallIntegerField()


class Timeline(TrackingFields):
    tweeter = models.ForeignKey(ProfileDetails, related_name='timeline')
    tweets = models.ManyToManyField(TimelineTweet, related_name='timelines')

    def populate_timeline(self, return_tweets=10):
        tweeter = self.tweeter

        own_tweets = tweeter.tweets.all()
        tagged_tweets = tweeter.tagged_in.all()
        total_tweets = own_tweets | tagged_tweets
        total_tweets_ids = list(set([tweet.id for tweet in total_tweets.order_by("id")]))
        return total_tweets_ids[0:return_tweets]