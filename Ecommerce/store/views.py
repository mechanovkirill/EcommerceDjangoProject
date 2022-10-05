from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category


# Create your views here.
def store_view(request, category_slug=None):
    categorys = None
    products = None

    # store/models/Product/slug
    if category_slug != None:
        categorys = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categorys, is_available=True)
        products_count = products.count()
    else:
        products = Product.objects.all().order_by('product_name').filter(is_available=True)
        products_count = products.count()

    context = {
        'products': products,
        'products_count': products_count

    }

    return render(request, 'store/store.html', context=context)
