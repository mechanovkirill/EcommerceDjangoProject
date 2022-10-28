from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.utils.html import format_html


# Register your models here.

# available use Tuple or List
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'is_active', 'date_joined',)
    list_display_links = ('email', 'first_name', 'last_name',)  # можно переходить к аккаунту
    readonly_fields = ('last_login', 'date_joined',)
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class UserProfileAdmin(admin.ModelAdmin):
    """thumbnail - встроенный в django пакет для создания миниатюр изображений
    format_html создает элемент html"""
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" height=30 style="border-radius:50%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country', 'address')


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)