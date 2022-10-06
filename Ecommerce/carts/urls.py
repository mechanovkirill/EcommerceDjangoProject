from django.urls import path
from .views import cart_view

app_name = 'carts'

urlpatterns = [
    path('', cart_view, name='cart-view'),
]
