from django.urls import path
from .views import (cart_view, add_cart, reduce_quantity_view, delete_cart_item_view, checkout_view)

app_name = 'carts'
urlpatterns = [
    path('', cart_view, name='cart-view'),
    path('add_cart/<int:product_id>/', add_cart, name='add-cart'),
    path(
        'reduce_quantity_view/<int:product_id>/<int:cart_item_id>/', reduce_quantity_view, name='reduce-quantity-view'
    ),
    path(
        'delete_cart_item_view/<int:product_id>/<int:cart_item_id>/', delete_cart_item_view,
        name='delete-cart-item-view'
    ),
    path('checkout/', checkout_view, name='checkout-view')
]
