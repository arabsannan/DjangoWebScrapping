from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
import tweepy
from .forms import TweetGeoCount
import os
import json
import pprint
from pathlib import Path

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from django.db.models.fields.files import ImageFieldFile
from django.forms import model_to_dict

api_key = 'UalRAOtxgNemAKjlhRsE1KoVc'
api_secret_key = '971DKlrk0n1I4LS3XxxL8urTu6izMFAYEXiDOetp1QyJP6CluD'
access_token = '1328734801747173376-T6O51qLNFUBWpSJv1ciGkivxmYnTIO'
access_token_secret = 'Ye3nc7GKqIjGANcrDFJGyBjNTIuaUGw86JD9l9r4oMF67'

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


def home_view(request):
    if request.method == 'POST':
        form = TweetGeoCount(request.POST or None)
        if form.is_valid():
            count = form.cleaned_data['count']
            country_name = form.cleaned_data['country_name']

            print(form.cleaned_data)

            print(f'Capturing tweets from {country_name}...')

            the_dict_list = []
            extra_count = 5 * count

            for tweet in tweepy.Cursor(api.search, q=country_name).items(extra_count):
                if 'RT' in tweet.text:  # my update
                    pass
                else:
                    t_timestamp = tweet.created_at
                    t_text = tweet.text
                    t_user = tweet.user.name

                    the_dict_list.append({'time': t_timestamp, 'user': t_user, 'tweet': t_text})
                    # if the captured tweets are equal to the count specified continue
                    if len(the_dict_list) == count:
                        print(len(the_dict_list))
                        break

            __dir = "./Tweets"
            if os.path.exists(__dir):
                pass
            else:
                os.mkdir(__dir)  # creates Tweets directory

            json_file = open(f'{__dir}/{country_name}.json', 'w')

            j = json.dumps(the_dict_list, indent=4, cls=ExtendedEncoderAllFields, ensure_ascii=True)
            json_file.write(j)

            request.session['country_name'] = request.POST['country_name']
            print('Done!')
            # return HttpResponseRedirect(reverse('home'))
            return redirect('read/')
        context = {'form': form}
    return render(request, 'capture/capture_home.html')


BASE_DIR = Path(__file__).resolve().parent.parent


def read_view(request):
    # country_name = request.POST.get('country_name')
    url = request.session.get('country_name')
    with open(f'./Tweets/{url}.json', 'r') as file:
        data = json.load(file)
    context = {'d': data, 'url': url}
    return render(request, 'capture/capture_read.html', context, content_type='text/html')
    # content_type='application' downloads page
