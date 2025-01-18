from django import forms
from .models import BlogComment


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['first_name', 'email', 'content']

    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 6,
            'cols': 30,
            'class': 'form-control mb-4',
            'placeholder': 'دیدگاه شما *',
            'id': 'reply-message',
        }),
        label="نظر"
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'نام و نام خانوادگی *',
            'class': 'form-control',
            'id': 'reply-name',
            'name': 'reply-name'
        }),
        label="نام و نام خانوادگی"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'آدرس ایمیل *',
            'class': 'form-control text-left',
            'id': 'reply-email',
            'name': 'reply-email'
        }),
        label="آدرس ایمیل"
    )

