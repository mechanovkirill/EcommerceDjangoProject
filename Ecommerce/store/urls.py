from django.urls import path
from .views import store_view

app_name = 'store'
urlpatterns = [
    path('', store_view, name='store-view'),
    # store/models/Product/slug
    path('<slug:category_slug>/', store_view, name='products_by_category'),
]
