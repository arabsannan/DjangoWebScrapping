from django.http import FileResponse
from django.shortcuts import render, redirect
from .forms import TweetGeoCount
from pathlib import Path
import tweepy
import os
from dotenv import load_dotenv
import json

load_dotenv()  # Load environment variables from .env file

# API credentials
api_key = os.getenv('API_KEY')
api_secret_key = os.getenv('API_SECRET_KEY')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


def home(request):
    if request.method == 'POST':
        form = TweetGeoCount(request.POST or None)
        if form.is_valid():
            count = form.cleaned_data['count']
            country_name = form.cleaned_data['country_name']
            download_checkbox = request.POST.get('download_checkbox') == 'on'

            # initialize tweets list
            tweets = []

            for tweet in tweepy.Cursor(api.search_tweets, q='country_name -filter:retweets').items(count):
                tweets.append({
                    # format date
                    'time': tweet.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'user': tweet.user.name,
                    'tweet': tweet.text
                })

            directory = "./Tweets"
            if not os.path.exists(directory):
                # creates the Tweets directory if it doesn't exist
                os.mkdir(directory)

            # Create JSON file and dump contents of tweets list
            file_path = os.path.join(directory, f'{country_name}.json')
            with open(file_path, 'w') as json_file:
                json.dump(tweets, json_file, indent=4)

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
