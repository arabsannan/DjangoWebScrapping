from django import forms
from django.core.exceptions import ValidationError


class TweetGeoCount(forms.Form):
    count = forms.IntegerField()
    country_name = forms.CharField(max_length=150)

    def clean(self):
        cleaned_data = super().clean()
        count = cleaned_data.get('count')
        if count is not None and (count < 10 or count > 100):
            raise ValidationError('Enter a count between 10 and 100')
        return cleaned_data
  

