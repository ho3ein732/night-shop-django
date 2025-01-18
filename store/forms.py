from  django import forms
from .models import Review, ContactUs, Emails


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment']


class SearchForm(forms.Form):
    query = forms.CharField(max_length=25)


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['content', 'name', 'email']


class EmailForm(forms.ModelForm):
    class Meta:
        model = Emails
        fields = ['email']
