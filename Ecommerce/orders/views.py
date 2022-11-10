from django.shortcuts import render, redirect
from carts.models import CartItem
from store.models import Product
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
import datetime
from decimal import Decimal
from django.contrib import messages
# email
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

import logging, traceback

logger = logging.getLogger(__name__)


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
            payment_db_data.amount_paid = order.order_total
            payment_db_data.payment_method = 'PayPal'
            payment_db_data.status = 'COMPLETED'
            payment_db_data.save()

            payment = Payment.objects.get(user=request.user, payment_id=payment_db_data.payment_id)

            order.payment = payment
            order.is_ordered = True
            order.save()
            # end of a gag code

            # move the cart items to order product table
            cart_items = CartItem.objects.filter(user=request.user)

            for item in cart_items:
                product = Product.objects.get(id=item.product_id)
                if product.stock >= item.quantity:
                    order_product = OrderProduct()
                    order_product.order_id = order.id
                    order_product.payment = payment
                    order_product.user_id = request.user.id
                    order_product.product_id = item.product_id
                    order_product.quantity = item.quantity
                    order_product.product_price = item.product.price
                    order_product.ordered = True
                    order_product.save()

                    cart_item = CartItem.objects.get(id=item.id)
                    product_variation = cart_item.variations.all()
                    order_product = OrderProduct.objects.get(id=order_product.id)
                    order_product.variations.set(product_variation) #   https://docs.djangoproject.com/en/4.1/ref/models/relations/

                # reduce the quantity of sold products
                    product.stock -= item.quantity
                    product.popularity += 1
                    product.save()
                else:
                    ordered_order = Order.objects.get(
                        user=request.user,
                        is_ordered=True,
                        order_number=request.POST.get('payment_id')
                    )
                    ordered_order.is_ordered = False
                    messages.error(
                        request, 'We\'re sorry, but there are fewer items in stock than you\'d like to purchase.'
                    )

                    return redirect('orders:payments-view')

            # clear cart
            CartItem.objects.filter(user=request.user).delete()

            # Send order received email to customer
            ordered_products = OrderProduct.objects.filter(
                user=request.user,
                order__order_number=order.order_number
            )
            products_names = []
            for p in ordered_products:
                p_name = p.product.product_name
                products_names.append(p_name)
            if 'Developer' in products_names:
                mail_subject = 'Спасибо что посетили мой сайт!'
                message = render_to_string('orders/order_developer_email.html', {
                    'user': request.user,
                    'order': order,
                })
                to_email = request.user.email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()

                # Sending when paypal is not available, otherwise this code should be in order_complete_view
                order_number = request.POST.get('order_number')
                try:
                    order = Order.objects.get(order_number=order_number, is_ordered=True)
                    ordered_products = OrderProduct.objects.filter(order_id=order.id)
                    payment = order.payment
                    subtotal = order.order_total - order.tax

                    context = {
                        'order': order,
                        'ordered_products': ordered_products,
                        'payment': payment,
                        'subtotal': subtotal,
                    }
                    return render(request, 'orders/order_complete.html', context=context)

                except (Payment.DoesNotExist, Order.DoesNotExist):
                    messages.error(request, 'Order or payment data is not available')
                    return render(request, 'orders/order_complete.html')
                    logger.exception('Payment error'), traceback

            else:
                mail_subject = 'Thank you for your order!'
                message = render_to_string('orders/order_received_email.html', {
                    'user': request.user,
                    'order': order,
                })
                to_email = request.user.email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()

                # Sending when paypal is not available, otherwise this code should be in order_complete_view
                order_number = request.POST.get('order_number')
                try:
                    order = Order.objects.get(order_number=order_number, is_ordered=True)
                    ordered_products = OrderProduct.objects.filter(order_id=order.id)
                    payment = order.payment
                    subtotal = order.order_total - order.tax

                    context = {
                        'order': order,
                        'ordered_products': ordered_products,
                        'payment': payment,
                        'subtotal': subtotal,
                    }
                    return render(request, 'orders/order_complete.html', context=context)

                except (Payment.DoesNotExist, Order.DoesNotExist):
                    messages.error(request, 'Order or payment data is not available')
                    return render(request, 'orders/order_complete.html')
                    logger.exception('Payment error'), traceback

        except:
            pass
    else:
        return render(request, 'orders/payments.html')

    return render(request, 'orders/payments.html')


def order_complete_view(request):
    return render(request, 'orders/order_complete.html')

