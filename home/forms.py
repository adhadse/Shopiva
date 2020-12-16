from django.forms import ModelForm
from django import forms
from home.models import Ratings


class ReviewForm(ModelForm):
    subject = forms.CharField(label='', max_length=255,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': "What's most important to know"}))
    comment = forms.CharField(label='', max_length=2048,
                              widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'placeholder': 'What did you Like or dislike? What did you '
                                                                          'use this product for?',
                                                           'max_length': 2048}))

    class Meta:
        model = Ratings
        fields = ('subject', 'comment', 'ratings')
