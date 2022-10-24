from django.shortcuts import render, redirect
from carts.models import CartItem
from .forms import OrderForm, PaymentForm
from .models import Order, Payment
import datetime
from decimal import Decimal
from random import randint


# Create your views here.

def place_order_view(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store:store-view')

    total_plus_tax = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (4 * total) / 100
    total_plus_tax = total + tax
    form = OrderForm(request.POST)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # store all billing info inside Order DB
            order_db_data = Order()  # TODO: authomatic get data from account
            order_db_data.user = current_user
            order_db_data.first_name = form.cleaned_data['first_name']
            order_db_data.last_name = form.cleaned_data['last_name']
            order_db_data.email = form.cleaned_data['email']
            order_db_data.phone = form.cleaned_data['phone']
            order_db_data.address = form.cleaned_data['address']
            order_db_data.country = form.cleaned_data['country']
            order_db_data.city = form.cleaned_data['city']
            order_db_data.state = form.cleaned_data['state']
            order_db_data.order_note = form.cleaned_data['order_note']
            order_db_data.order_total = Decimal(total_plus_tax)
            order_db_data.tax = Decimal(tax)
            order_db_data.ip = request.META.get('REMOTE_ADDR')  # get user's ip
            # https://docs.djangoproject.com/en/4.1/ref/request-response/
            order_db_data.save()

            year = int(datetime.date.today().strftime('%Y'))
            date = int(datetime.date.today().strftime('%d'))
            month = int(datetime.date.today().strftime('%m'))
            d = datetime.date(year, month, date)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(order_db_data.id)
            order_db_data.order_number = order_number
            order_db_data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'cart_items': cart_items,
                'order': order,
                'total': total,
                'tax': tax,
                'total_plus_tax': total_plus_tax,
            }
            return render(request, 'orders/payments.html/', context=context)

    else:
        return render(request, 'store/checkout.html')


def payments_view(request):
    ''' Instead of Paypal, here is a gag code (a citizen of Russia cannot register Paypal)
    '''
    if request.method == 'POST':
        order = Order.objects.get(user=request.user, is_ordered=False, order_number=request.POST['payment_id'])
        try:
            payment_db_data = Payment()
            payment_db_data.user = request.user
            payment_db_data.payment_id = order.order_number + datetime.datetime.now().strftime('%H%M')
            print(type(order.order_number))
            payment_db_data.amount_paid = order.order_total
            payment_db_data.payment_method = 'PayPal'
            payment_db_data.status = 'COMPLETED'
            payment_db_data.save()

            payment = Payment.objects.get(user=request.user, payment_id=payment_db_data.payment_id)

            order.payment = payment
            order.is_ordered = True
            order.save()
            # end of a gag code
            return redirect('orders:payments-view')
        except:
            pass
        # move the cart items to order product table

        # reduce the quantity of sold products

        # clear cart

        # Send order received email to customer

        # send order number and transaction id back to js
    else:
        return render(request, 'orders/payments.html')

    return render(request, 'orders/payments.html')
