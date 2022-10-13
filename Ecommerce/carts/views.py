from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse


# Create your views here.
def get_cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product_variation = []
    product = Product.objects.get(id=product_id)  # get the product
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(
                    product=product, variation_category__iexact=key, variation_value__iexact=value
                ) # __iexact - точное совпадение без учета регистра
                product_variation.append(variation)
            except:
                pass

    try:
        cart = Cart.objects.get(cart_id=get_cart_id(request))  # получить корзину используемую в текущей сессии
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=get_cart_id(request))
        cart.save()

    is_cart_item_exist = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exist:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        # existing_variations --> Database
        # current variations --> product_variations
        # item_id --> Database
        id_list = []
        existing_variation_list = []
        for item in cart_item:
            existing_variation = item.variations.all()
            existing_variation_list.append(list(existing_variation))
            id_list.append(item.id)

        if product_variation in existing_variation_list:
            # increase the cart item quantity
            index = existing_variation_list.index(product_variation) # list method index
            item_id = id_list[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            # create a new cart item
            item = CartItem.objects.create(product=product, cart=cart, quantity=1)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()

    return redirect('carts:cart-view')


def reduce_quantity_view(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)  # get the product
    cart = Cart.objects.get(cart_id=get_cart_id(request))  # получить корзину используемую в текущей сессии
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('carts:cart-view')


def delete_cart_item_view(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=get_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        cart_item.delete()
    except:
        pass
    return redirect('carts:cart-view')


def cart_view(request, total=0, quantity=0, tax=0, total_plus_tax=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=get_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (4 * total)/100
        total_plus_tax = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'total_plus_tax':total_plus_tax,
    }
    return render(request, 'store/cart.html', context=context)
