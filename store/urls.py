from django.urls import path
from . import views
app_name = 'store'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('products-by-category/<int:category_id>/<slug:slug>/', views.product_by_category, name='product_by_category'),
    path('product-detail/<int:product_id>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('add-to-favorite/<int:id>/', views.add_to_favorite, name='add_to-favorite'),
    path('list-favorites/', views.list_favorite, name='list_favorite'),
    path('remove-favorite/<int:id>/', views.remove_favorite, name='remove_favorite'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('add-email/', views.emails, name='add_email'),

]


