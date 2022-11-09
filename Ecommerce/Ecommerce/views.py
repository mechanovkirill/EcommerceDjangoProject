from django.views.generic import TemplateView
from store.models import Product, ReviewRating
from django.shortcuts import render
from django.core.paginator import Paginator


def home_view(request):
    products = Product.objects.all().filter(is_available=True).order_by('-popularity')
    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    # get the review
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': paged_products,
        'reviews': reviews,
    }


    return render(request, 'home.html', context=context)
    # путь прописан в settings.py, templates DIR ('templates')
