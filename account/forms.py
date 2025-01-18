from django import forms
from .models import NightUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'رمزعبور خود را وارد کنید'}),
        min_length=8,
        help_text='رمز عبور باید حداقل 8 رفم باشد.',
    )

    class Meta:
        model = NightUser
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'id': 'username',
                'placeholder': 'ایمیل خود را وارد کنید'
            })
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if NightUser.objects.filter(email=email).exists():
            raise forms.ValidationError('این ایمیل از قبل وجود دارد.')
        return email


class VerifyEmail(forms.Form):
    token = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'id': 'email', 'placeholder': 'کد تایید را '
                                                                                                      'وارد کنید'}))


class NightUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = NightUser
        fields = '__all__'
        # widgets = {}

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.instance.pk:
            if NightUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('email already exists!')
        else:
            if NightUser.objects.filter(email=email).exists():
                raise forms.ValidationError('email already exists!')

        return email


class NightUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = NightUser
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.instance.pk:
            if NightUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('این ایمیل قبلاً ثبت شده است!')
        else:
            if NightUser.objects.filter(email=email).exists():
                raise forms.ValidationError('این ایمیل قبلاً ثبت شده است!')
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'}))


class NewEmailForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = NightUser
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data['email']

        if self.instance.pk:
            if NightUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('این ایمیل قبلاً ثبت شده است!')
        else:
            if NightUser.objects.filter(email=email).exists():
                raise forms.ValidationError('این ایمیل قبلاً ثبت شده است!')
        return email


class DetailAccountForm(forms.ModelForm):
    class Meta:
        model = NightUser
        fields = [
            'first_name',
            'last_name',
            'email'
        ]

    first_name = forms.CharField(
        widget=forms.Textarea(attrs={

            'class': 'form-control mb-4',
            'type': 'text'
        }),
        label="نام"
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',

        }),
        label="نام خانوادگی"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control text-left',
            'placeholder': 'ایمیل'
        }),
        label="آدرس ایمیل"
    )


class ForgetForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}))


class ConfirmCodeForgetPasswordForm(forms.Form):
    token = forms.CharField(label="کد تأیید", max_length=6, widget=forms.TextInput(attrs={
        'class': 'form-control text-left ltr',
        'placeholder': 'کد تأیید را وارد کنید'
    }))
    new_password = forms.CharField(label="رمز عبور جدید", widget=forms.PasswordInput(attrs={
        'class': 'form-control text-left ltr',
        'placeholder': 'رمز عبور جدید'
    }))
    confirm_password = forms.CharField(label="تکرار رمز عبور جدید", widget=forms.PasswordInput(attrs={
        'class': 'form-control text-left ltr',
        'placeholder': 'تکرار رمز عبور جدید'
    }))