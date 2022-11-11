from django.shortcuts import render, get_object_or_404, redirect, Http404
from .models import Product, ReviewRating, ProductGallery
from .forms import ReviewRatingForm
from category.models import Category
from carts.views import get_cart_id
from carts.models import CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib import messages
from orders.models import OrderProduct
from accounts.models import UserProfile
import logging, traceback

logger = logging.getLogger(__name__)

# Create your views here.
def store_view(request, category_slug=None):
    categorys = None
    products = None

    # store/models/Product/slug
    if category_slug != None:
        categorys = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categorys, is_available=True).order_by('-popularity')
        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('-popularity')
        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()

    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': paged_products,
        'products_count': products_count,
    }

    return render(request, 'store/store.html', context=context)


def product_detail_view(request, category_slug, product_slug):
    user = request.user
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        if user.is_authenticated:
            in_cart = CartItem.objects.filter(product=single_product, user=user).exists()
        else:
            in_cart = None
        # __ (underscore underscore) указывает на
        # поле cart = models.ForeignKey внешний ключ который указывает на поле cart_id в таблице Cart
        # возвращает True or False есть ли товар в корзине

    except Exception:
        raise Exception(logger.exception('category or product getting error'), traceback)

    # for review
    if user.is_authenticated:
        orderproduct = OrderProduct.objects.filter(user=user, product_id=single_product.id).exists()
    else:
        orderproduct = None

    # get the review
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
    # get user avatar
    if user.is_authenticated:
        user_profile = UserProfile.objects.get(user=user)
    else:
        user_profile = None

    # get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
        'user_profile': user_profile,
    }

    return render(request, 'store/product_detail.html', context=context)


def search_view(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('create_date').filter(Q(description__icontains=keyword)
                                                                      | Q(product_name__icontains=keyword)
                                                                      )
            products_count = products.count()

    context = {
        "products": products,
        "products_count": products_count,
    }
    return render(request, 'store/store.html', context=context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        if len(request.POST.get('subject')) < 128 and len(request.POST.get('review')) < 512:
            try:
                reviews = ReviewRating.objects.get(user_id=request.user.id, product_id=product_id)
                # __ in user__id & product__id потому что ссылается на ForeignKey
                form = ReviewRatingForm(request.POST, instance=reviews)
                form.save()
                messages.success(request, 'Thank you! Your review has been updated.')
                return redirect(url)
            except ReviewRating.DoesNotExist:
                form = ReviewRatingForm(request.POST)
                if form.is_valid():
                    data = ReviewRating()
                    data.subject = form.cleaned_data['subject']
                    data.rating = form.cleaned_data['rating']
                    data.review = form.cleaned_data['review']
                    data.ip = request.META.get('REMOTE_ADDR')
                    data.product_id = product_id
                    data.user_id = request.user.id
                    data.save()
                    messages.success(request, 'Thank you! Your review has been submitted.')
                    return redirect(url)
        else:
            messages.info(request, 'Too long')
            return redirect(url)
    else:
        return render(request, 'store/store.html')
