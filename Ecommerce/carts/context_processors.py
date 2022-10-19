from .models import Cart, CartItem
from .views import get_cart_id

def counter(request):
    """Counts the goods in the cart
    """
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=get_cart_id(request))
            if request.user.is_authenticated: # https://docs.djangoproject.com/en/4.1/ref/contrib/auth/
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)
