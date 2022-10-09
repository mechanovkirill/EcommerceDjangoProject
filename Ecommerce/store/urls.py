from django.urls import path
from .views import store_view, product_detail_view, search_view


app_name = 'store'
urlpatterns = [
    # {% url 'store:store-view' %}
    path('', store_view, name='store-view'),

    # store/models/Product/slug
    path('category/<slug:category_slug>/', store_view, name='products-by-category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', product_detail_view, name='product-detail'),
    path('search/', search_view, name='search-view')
]
