from datetime import datetime
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from django.db.models.fields.files import ImageFieldFile
from django.forms import model_to_dict
from .forms import TweetGeoCount
from pathlib import Path
import tweepy
import os
from dotenv import load_dotenv
import json

load_dotenv()  # Load environment variables from .env file

# Auth
api_key = os.getenv('API_KEY')
api_secret_key = os.getenv('API_SECRET_KEY')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# setting up twitter APIs
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


class ExtendedEncoderAllFields(DjangoJSONEncoder):

    def default(self, o):
        if isinstance(o, ImageFieldFile):
            try:
                mypath = o.path
            except:
                return ''
            else:
                return mypath
        # this will either recursively return all attributes of the object or return just the id
        elif isinstance(o, Model):
            return model_to_dict(o)
            # return o.id

        return super().default(o)


def home(request):
    if request.method == 'POST':
        form = TweetGeoCount(request.POST or None)
        if form.is_valid():
            count = form.cleaned_data['count']
            country_name = form.cleaned_data['country_name']
            download_checkbox = request.POST.get('download_checkbox') == 'on'

            # initialize variables
            tweets = []
            COUNT_INCREMENT = 4
            increased_count = COUNT_INCREMENT * count

            for tweet in tweepy.Cursor(api.search_tweets, q=country_name).items(increased_count):
                # remove retweets
                if 'RT' in tweet.text:
                    pass
                else:
                    tweet_timestamp = tweet.created_at
                    tweet_text = tweet.text
                    tweet_user = tweet.user.name

                    # format time
                    tweet_timestamp = tweet_timestamp.strftime(
                        '%Y-%m-%d %H:%M:%S')

                    # if the items in the tweets list are not equal to the count specified continue
                    if len(tweets) != count:
                        tweets.append(
                            {'time': tweet_timestamp, 'user': tweet_user, 'tweet': tweet_text})

            __dir = "./Tweets"
            if not os.path.exists(__dir):
                os.mkdir(__dir)  # creates Tweets directory

            # create json file and dump contents in tweets list 
            json_file = open(f'{__dir}/{country_name}.json', 'w')
            j = json.dumps(tweets, indent=4,
                           cls=ExtendedEncoderAllFields, ensure_ascii=True)
            json_file.write(j)

            # set session values
            request.session['country_name'] = request.POST['country_name']
            request.session['download_checkbox'] = download_checkbox

            return redirect('read/')
        else:
            context = {'form': form}
    else:
        form = TweetGeoCount()
        context = {'form': form}
    return render(request, 'capture/home.html', context)


def read_tweets(request):
    country_name = request.session.get('country_name')
    download_checkbox = request.session.get('download_checkbox')
    with open(f'./Tweets/{country_name}.json', 'r') as file:
        data = json.load(file)
    context = {
        'tweets': data,
        'country_name': country_name,
        'download_checkbox': download_checkbox
    }
    return render(request, 'capture/read_tweets.html', context, content_type='text/html')


def download_tweets_file(request, country_name):
    # Generate the file path using the file's stored path
    file_path = f'./Tweets/{country_name}.json'

    # Open the file and create a response with appropriate headers
    file = open(file_path, 'rb')
    response = FileResponse(file)

    # Set the content type header based on the file's MIME type
    response['Content-Type'] = 'application/json'

    # Set the Content-Disposition header to force download
    response['Content-Disposition'] = f'attachment; filename="{country_name}.json"'

    return response
