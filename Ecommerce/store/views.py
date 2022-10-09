from django.shortcuts import render, get_object_or_404, Http404
from .models import Product
from category.models import Category
from carts.views import get_cart_id
from carts.models import CartItem

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

def product_detail_view(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=get_cart_id(request), product=single_product).exists() # __ (underscore underscore) указывает на
            # поле cart = models.ForeignKey внешний ключ который указывает на поле cart_id в таблице Cart
            # возвращает True & False есть ли товар в корзине

    except Exception:
        raise Exception
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context=context)

# def single_product():
