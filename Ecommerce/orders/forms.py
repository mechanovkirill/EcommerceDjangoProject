from django import forms
from .models import Order, Payment

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'country', 'city', 'state', 'order_note']

class PaymentForm(forms.Form):
    class Meta:
        model = Payment
        fields = ['payment_id', 'amount_paid']
