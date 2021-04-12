from django import forms
from django.core.exceptions import ValidationError


# def clean_count(count):
#     if count < 10 or count > 100:
#         raise forms.ValidationError('Enter a count between 10 and 100')


class TweetGeoCount(forms.Form):
    count = forms.IntegerField()
    country_name = forms.CharField(max_length=150)

    def clean_count(self):
        count = self.cleaned_data['count']
        if count < 10 or count > 100:
            raise ValidationError('Enter a count between 10 and 100')
        return count
    # clean_count(count)

