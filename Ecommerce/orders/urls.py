from django.urls import path
from .views import place_order_view, payments_view, order_complete_view

app_name = 'orders'
urlpatterns = [
    path('place_order/', place_order_view, name='place-order-view'),
    path('payments/', payments_view, name='payments-view'),
    path('order_complete/', order_complete_view, name='order-complete-view'),
]