from django.urls import path, include
from . import views
app_name = 'account'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('verify_token/', views.verify_email, name='verify_token'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('detail/', views.detail, name='detail'),
    path('complete-information/', views.complete_detail_account, name='complete-information'),
    path('forget-password/', views.forget_password, name='forget-password'),
    path('confirm-password-change/', views.verifi_token_forget_password, name='confirm-password-change'),
    path('forget-master-password/', views.forget_master_password, name='forget-master-master'),
]