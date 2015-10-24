__author__ = 'ironeagle'

import json

from django.shortcuts import *
from django.http import *
from django.contrib.auth import login as auth_login
from django.http import Http404

from .models import *
from .utils import sign_up_or_login
from .app_settings import THICK_LINE, THIN_LINE 


# from IPython.frontend.terminal.embed import InteractiveShellEmbed
# InteractiveShellEmbed()()


def follow(request, username=None):
    response = {}

    print(THICK_LINE)
    print str(username) + " followed by " + str(request.user.username) + " initiated"

    if not username:
        print(THIN_LINE)
        print "username is None"
        response.update({
            "status": "error",
            "message": "please tell whom to follow",
        })
        response = (json.dumps(response))
        print(THIN_LINE)
        print response

    elif not request.user.is_authenticated():
        print(THIN_LINE)
        print "no user"
        response.update({
            "status": "error",
            "message": "please login before following",
        })
        response = (json.dumps(response))
        print(THIN_LINE)
        print response

    else:
        print(THIN_LINE)
        print "follow ok"
        follower = request.user.profile.all()[0]
        print(THIN_LINE)
        print "follower " + str(follower)
        following = ProfileDetails.objects.get(username=username)
        print(THIN_LINE)
        print "following " + str(following)
        follow_user = FollowUser(following=following, follower=follower)
        follow_user.save()
        print(THIN_LINE)
        print str(follow_user.following.username) + " followed by " + str(follow_user.follower.username)
        response.update({
            "status": "success",
            "message": "FollowUser ID " + str(follow_user.id) + " successful",
        })
        print(THIN_LINE)
        response = json.dumps(response)
        print response

    return HttpResponse(response)


def like_tweet(request, tweet_id=None):
    response = {}

    if not tweet_id:
        print(THIN_LINE)
        print "tweet_id is None"
        response.update({
            "status": "error",
            "message": "please tell which tweet to like",
        })
        response = (json.dumps(response))
        print(THIN_LINE)
        print response

    elif not request.user.is_authenticated():
        print(THIN_LINE)
        print "no user"
        response.update({
            "status": "error",
            "message": "please login before liking",
        })
        response = (json.dumps(response))
        print(THIN_LINE)
        print response

    else:
        print(THIN_LINE)
        print "like ok"
        liker = request.user.profile.all()[0]
        # non_likable_tweets = [tweet_like.tweet for tweet_like in liker.liked_tweets.all()]
        print(THIN_LINE)
        print "replier " + str(liker)
        liked_tweet = Tweet.objects.get(id=tweet_id)
        print(THIN_LINE)
        print "liking " + str(liked_tweet.id)
        instructions = liked_tweet.add_liked_by(liker)
        print(THIN_LINE)
        print str(instructions) + " likes"
        if instructions == "add":
            print(THIN_LINE)
            print "liked tweet ID " + str(liked_tweet.id) + " liked by " + str(
                liked_tweet.liked_by_profiles.all().order_by('-id')[0].liked_by.username) + " successfully"
            response.update({
                "status": "success",
                "message": "Tweet ID " + str(liked_tweet.id) + " successfully liked by " + str(
                    liked_tweet.liked_by_profiles.get(liked_by=liker).liked_by.username),
                "instructions": str(instructions),
            })
        else:
            response.update({
                "status": "success",
                "message": "Tweet ID " + str(liked_tweet.id) + " successfully unliked by " + str(liker.username),
                "instructions": str(instructions),
            })
        """
        except:
            print(THIN_LINE)
            print "liked tweet ID " + str(liked_tweet.id) + " cannot be liked by" + str(liker.username)
            response.update({
                "status": "error",
                "message": "Tweet ID " + str(liked_tweet.id) + " cannot be liked by " + str(liker.username)
            })"""

        print(THIN_LINE)
        response = json.dumps(response)
        print response

    return HttpResponse(response)


def reply_tweet(request, tweet_id=None):
    response = {}

    reply_tweet_text = request.POST["tweet_text"]
    print(THIN_LINE)
    print str(tweet_id) + " tweet got reply " + str(reply_tweet_text) + " by " + str(request.user.username)

    if not request.user.is_authenticated():
        print(THIN_LINE)
        print "no user"
        response.update({
            "status": "error",
            "message": "please login before tweeting",
        })
        response = (json.dumps(response))
        print(THIN_LINE)
        print response
        return HttpResponse(response)

    elif not tweet_id:
        print(THIN_LINE)
        print "tweet_id is None"
        response.update({
            "status": "error",
            "message": "please tell which tweet to reply",
        })
        response = (json.dumps(response))
        print(THIN_LINE)
        print response
        return HttpResponse(response)

    elif reply_tweet_text == "":
        print(THIN_LINE)
        print "no reply"
        response.update({
            "status": "error",
            "message": "please tell what to reply",
        })
        response = (json.dumps(response))
        print(THIN_LINE)
        print response
        return HttpResponse(response)

    else:
        tweeter_profile = request.user.profile.all()[0]
        print(THIN_LINE)
        print "tweeter's profile " + str(tweeter_profile)
        tweet_text = request.POST.get("tweet_text")
        print(THIN_LINE)
        print "tweeter's tweet " + str(tweet_text)
        tweet_author = tweeter_profile
        print(THIN_LINE)
        print "tweeter's author " + str(tweet_author)
        tweet_tags = request.POST.getlist("tweet_tags")
        if tweet_tags:
            print(THIN_LINE)
            print "tweeter's tags "
            for tweet_tag in tweet_tags:
                print tweet_tag

        reply_tweet_obj = Tweet(text=tweet_text, author=tweet_author)
        reply_tweet_obj.save()
        for tweet_tag in tweet_tags:
            reply_tweet_obj.tags.add(ProfileDetails.objects.get(username=tweet_tag))
        reply_tweet_obj.save()

        # Replying To Parent - Start
        parent_tweet = Tweet.objects.get(pk=tweet_id)
        print(THIN_LINE)
        print "replied to tweet " + str(parent_tweet.id)

        tweet_reply = TweetReply(parent_tweet=parent_tweet, reply_tweet=reply_tweet_obj)
        tweet_reply.save()
        # Replying To Parent - End

        response.update({
            "status": "success",
            "message": "Tweet ID " + str(tweet_reply.parent_tweet.id) + " successfully replied by Tweet ID " + str(
                tweet_reply.reply_tweet.id),
        })
        print(THIN_LINE)
        response = json.dumps(response)
        print response

    return HttpResponse(response)


def post_tweet(request):
    response = {}

    post_tweet_text = request.POST["tweet_text"]
    print(THIN_LINE)
    print "tweet " + str(post_tweet_text) + " by " + str(request.user.username)

    print(THIN_LINE)
    print "request.AJAX is " + str(request.is_ajax())

    if not request.user.is_authenticated():
        print(THIN_LINE)
        print "no user"
        response.update({
            "status": "error",
            "message": "please login before tweeting",
        })
        response = (json.dumps(response))
        print(THIN_LINE)
        print response
        return HttpResponse(response)

    elif post_tweet_text == "":
        print(THIN_LINE)
        print "no reply"
        response.update({
            "status": "error",
            "message": "please tell what to post",
        })
        response = (json.dumps(response))
        print(THIN_LINE)
        print response
        return HttpResponse(response)

    else:
        tweeter_profile = request.user.profile.all()[0]
        print(THIN_LINE)
        print "tweeter's profile " + str(tweeter_profile)
        tweet_text = request.POST.get("tweet_text")
        print(THIN_LINE)
        print "tweeter's tweet " + str(tweet_text)
        tweet_author = tweeter_profile
        print(THIN_LINE)
        print "tweeter's author " + str(tweet_author)
        tweet_tags = request.POST.getlist("tweet_tags")
        if tweet_tags:
            print(THIN_LINE)
            print "tweeter's tags "
            for tweet_tag in tweet_tags:
                print tweet_tag

        new_tweet = Tweet(text=tweet_text, author=tweet_author)
        new_tweet.save()
        for tweet_tag in tweet_tags:
            new_tweet.tags.add(ProfileDetails.objects.get(username=tweet_tag))
        new_tweet.save()

        response.update({
            "status": "success",
            "message": "Tweet ID " + str(new_tweet.id) + " by " + str(new_tweet.author.username),
        })
        print(THIN_LINE)
        response = json.dumps(response)
        print response

    if request.is_ajax():
        return HttpResponse(response)
    else:
        return redirect("tc_home")


def landing_page(request):
    context = {}
    print(THIN_LINE)
    print "landing page"

    return render(request, "post_it/tc-login.html", context)


def login(request):
    print(THIN_LINE)
    print "login"

    login_email = request.POST["login_email"]
    login_password = request.POST["login_password"]
    print(THIN_LINE)
    print str(login_email) + " " + str(login_password)

    user = sign_up_or_login(email=login_email, password=login_password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return redirect("tc_home")
        else:
            return HttpResponse("<strong>Error</strong> User account has not been activated.")
    else:
        return HttpResponse("<strong>Error</strong> Username or password was incorrect.")


def home(request):
    context = {}
    print(THIN_LINE)
    print "home"

    if request.user.is_authenticated():
        user_profile = request.user.profile.filter(username=str(request.user.username))
        if user_profile.count():
            print(THIN_LINE)
            print "Username '" + str(user_profile[0].username) + "' Found"
        else:
            new_profile = ProfileDetails(username=request.user.username, user=request.user, email=request.user.email,
                                         gender="U")
            new_profile.save()
            user_profile = [new_profile]

        user_profile = user_profile[0]
        context.update({
            "user_profile": user_profile,
        })

        feed = NewsFeed(listener=user_profile)
        feed.save()
        print(THIN_LINE)
        print "feed " + str(len(feed.populate_feed()))
        context.update({
            "feed": Tweet.objects.filter(id__in=feed.populate_feed()).order_by("-created_at"),
        })

        if user_profile.get_follow_suggestion().count() >= 6:
            follow_suggestions = user_profile.get_follow_suggestion()[0:6]
            print(THIN_LINE)
            print "suggestions " + str(user_profile.get_follow_suggestion().count())
            context.update({
                "follow_suggestions": follow_suggestions,
            })
        elif user_profile.get_follow_suggestion().count() < 6:
            follow_suggestions = user_profile.get_follow_suggestion()[:]
            print(THIN_LINE)
            print "suggestions " + str(user_profile.get_follow_suggestion().count())
            context.update({
                "follow_suggestions": follow_suggestions,
            })
        else:
            print(THIN_LINE)
            print "suggestions not found"

        if len(user_profile.get_taggable_profiles()):
            taggable_profiles = user_profile.get_taggable_profiles()
            print(THIN_LINE)
            print "taggable profiles " + str(len(taggable_profiles))
            context.update({
                "taggable_profiles": taggable_profiles,
            })
        else:
            print(THIN_LINE)
            print "taggable_profiles not found"

    else:
        return redirect("tc_landing_page")

    return render(request, "post_it/tc-home.html", context)


def timeline(request, username=None):
    context = {}

    if username:
        user_profile = ProfileDetails.objects.get(username=username)
        print(THIN_LINE)
        print "profile with username " + str(username)
    elif request.user.is_authenticated():
        user_profile = request.user.profile.get(username=str(request.user.username))
        print(THIN_LINE)
        print "logged in with username " + str(user_profile.username)
    else:
        raise Http404

    context.update({
        "user_profile": user_profile,
    })

    user_timeline = Timeline(tweeter=user_profile)
    user_timeline.save()
    print(THIN_LINE)
    print "timeline " + str(len(user_timeline.populate_timeline()))
    context.update({
        "timeline": Tweet.objects.filter(id__in=user_timeline.populate_timeline()).order_by("-created_at"),
    })

    return render(request, "post_it/tc-timeline.html", context)


def profile(request):
    context = {}

    if request.user.is_authenticated():
        user_profile = request.user.profile.get(username=str(request.user.username))
        print(THIN_LINE)
        print "logged in with username " + str(user_profile.username)
    else:
        raise Http404

    context.update({
        "user_profile": user_profile,
    })

    return render(request, "post_it/tc-profile.html", context)


def tweet(request, tweet_id=None):
    context = {}
    print(THIN_LINE)
    print "tweet feed " + str(tweet_id)

    if request.user.is_authenticated():
        user_profile = request.user.profile.get(username=str(request.user.username))
        print(THIN_LINE)
        print "logged in with username " + str(user_profile.username)
    else:
        raise Http404

    context.update({
        "user_profile": user_profile,
    })

    if not tweet_id:
        print(THIN_LINE)
        print "tweet_id is None"
    else:
        tweet_obj = Tweet.objects.get(id=tweet_id)

        print(THIN_LINE)
        print "tweet ID " + str(tweet_obj.id) + " found"
        context.update({
            "tweet": tweet_obj,
        })

        tweet_feed = tweet_obj.parent_to.all()
        print(THIN_LINE)
        print "tweet feed " + str(tweet_feed.count())
        context.update({
            "reply_tweet_feed": tweet_feed,
        })

    if request.user.is_authenticated():

        user_profile = request.user.profile.get(username=str(request.user.username))
        print(THIN_LINE)
        print "Username '" + str(user_profile.username) + "' Found"
        if len(user_profile.get_taggable_profiles()):
            taggable_profiles = user_profile.get_taggable_profiles()
            print(THIN_LINE)
            print "taggable profiles " + str(len(taggable_profiles))
            context.update({
                "taggable_profiles": taggable_profiles,
            })
        else:
            print(THIN_LINE)
            print "taggable_profiles not found"

    return render(request, "post_it/tc-tweet.html", context)
