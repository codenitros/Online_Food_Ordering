from django.urls import path, re_path
from . import views

from django.contrib.auth.views import LoginView, LogoutView

app_name = 'food'

urlpatterns = [

    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='main/index.html'), name='logout'),
    path('index/', views.index, name='index'),
    path('', views.home, name='home'),
    path('me/', views.profile, name='profile'),
    path('restaurants/', views.restaurants_view, name='res_list'),
    path('menu/<parameter>/', views.menu, name='menu'),
    path('contact/', views.contact, name='contact'),
    re_path(r'^search/$', views.search, name='search'),
    path('offers/', views.offers, name='offer'),
    path('place/<parameter>/', views.place, name='place'),
    path('pay/<parameter>/', views.pay, name='pay'),
    path('fav/<parameter>/', views.fav_add, name='fav_add'),
    path('favdel/<parameter>/', views.fav_del, name='fav_del'),

]

