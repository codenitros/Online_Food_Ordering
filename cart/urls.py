from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:recipe_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:recipe_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout')
]
