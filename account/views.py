import random
import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserCreateForm, VerifyEmail, LoginForm, DetailAccountForm, ForgetForm, ConfirmCodeForgetPasswordForm
from .models import NightUser
from django.contrib import messages
from django.core.cache import cache
from method import sendMail
from django.contrib.auth import login, authenticate, logout
from cart.models import Order
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


# Create your views here.


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = get_user_model().objects.get(email=email)
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None


def register_user(request):
    if request.method == 'POST':

        form = UserCreateForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            if NightUser.objects.filter(email=email).exists():
                messages.error(request, 'شما قبلا ثبت نام کردید وارد شوید')
                return redirect('login')  # +++

            else:

                token = ''.join(random.choices('1234567890abcdefghijklmnopqrstuvwxyz', k=6))
                cache.set(email, token, timeout=300)
                sendMail(email, token)
                request.session['email'] = email
                password = form.cleaned_data['password']
                request.session['password'] = password
                messages.success(request, 'ایمیل خود را برسی کنید')
                print(token)  # check

                return redirect('account:verify_token')
    else:

        form = UserCreateForm()

    return render(request, 'forms/register.html', {'form': form})


def verify_email(request):
    if request.method == 'POST':
        form = VerifyEmail(request.POST)
        if form.is_valid():
            email = request.session.get('email')
            token = form.cleaned_data['token']
            cache_token = cache.get(email)

            if cache_token == token:
                password = request.session['password']
                user = NightUser.objects.create(email=email)
                user.set_password(password)
                user.save()
                login(request, user)
                messages.success(request, 'ثبت نام با موفقیت انجام شد')
                return redirect('store:index')
            else:
                messages.error(request, 'کد تایید اشتباه است')
    else:
        form = VerifyEmail()
    return render(request, 'forms/verify_token.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'شما وارد شدید')
                return redirect('store:index')
            else:
                messages.error(request, 'رمز عبور یا ایمیل اشتباه است')
        else:
            messages.error(request, 'اطلاعات وارد شده نامعتبر است')
    else:
        form = LoginForm()
    return render(request, 'forms/login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect("store:index")


@login_required
def detail(request):
    user = request.user
    orders = Order.objects.filter(buyer=user)

    return render(request, 'account/detail.html', {'orders': orders, 'user': user})


def complete_detail_account(request):
    if request.method == 'POST':
        form = DetailAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات با موفقیت تغییر یافت')
        else:
            messages.error(request, 'خطا در بروزرسانی اطلاعات')
    else:
        initial = {'first_name': request.user.first_name, 'last_name': request.user.last_name,
                   'email': request.user.email}
        form = DetailAccountForm(initial, instance=request.user)

    return render(request, 'account/detail.html', {'form': form})


def forget_password(request):
    if request.method == 'POST':
        form = ForgetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not NightUser.objects.filter(email=email).exists():
                messages.error(request, 'همیچین ایمیلی وجود ندارد')
            else:
                token = ''.join(random.choices('1234567890abcdefghijklmnopqrstuvwxy', k=6))
                cache.set(email, token, timeout=301)
                sendMail(email, token)
                request.session['email'] = email
                messages.success(request, 'ایمیل خود را برسی کنید')
                print(token)  # check
                return redirect('account:confirm-password-change')

        else:
            messages.error(request, 'فرم مشکل دارد!')
    else:
        form = ForgetForm()

    return render(request, 'account/detail.html', {'form': form})


def verifi_token_forget_password(request):
    email = request.session.get('email')
    if not email:
        messages.error(request, 'درخواست نامعتبر است.')
    if request.method == 'POST':
        form = ConfirmCodeForgetPasswordForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            newpassword = form.cleaned_data['new_password']
            confirm = form.cleaned_data['confirm_password']

            if newpassword != confirm:
                messages.error(request, 'رمز عبورها باهم مطابقت ندارد.')
            elif cache.get(email) != token:
                messages.error(request, 'کد نادرست است یا منقضی شده است')
            else:
                user = NightUser.objects.get(email=email)
                user.set_password(confirm)
                user.save()
                cache.delete(email)
                del request.session['email']
                user = authenticate(request, email=email, password=confirm)
                if user:
                    login(request, user)
                    messages.success(request, 'رمز عبور با موفقیت تغییر کرد')
                    return redirect('cart:order')
                else:
                    messages.error(request, 'مشکلی در ورود!')
    else:
        form = ConfirmCodeForgetPasswordForm()
    return render(request, 'account/confirm.html', {'form': form})


