from django.contrib import admin
from .models import Payment, Order, OrderProduct


# Register your models here.
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0    # delete adding fields from panel

# available use Tuple or List
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'status', 'is_ordered', 'created_at'
    )
    list_filter = ('status', 'is_ordered')
    search_fields = ('order_number', 'first_name', 'last_name', 'phone', 'email')
    list_per_page = 20
    inlines = (OrderProductInline, )   # add OrderProduct to Order admin panel


admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
