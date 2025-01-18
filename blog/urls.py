from django.urls import path
from . import views

app_name = 'blog'


urlpatterns = [
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blog-comments/<int:blog_id>/', views.add_comment, name='add_comment'),
]