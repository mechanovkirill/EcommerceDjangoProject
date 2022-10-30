from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register_view, name='register-view'),
    path('login/', views.login_view, name='login-view'),
    path('logout/', views.logout_view, name='logout-view'),
    path('activate/<uidb64>/<token>/', views.activate_view, name='activate-view'),
    path('dashboard/', views.dashboard_view, name='dashboard-view'),
    path('', views.dashboard_view, name='dashboard-view'),
    path('forgot_password/', views.forgot_password_view, name='forgot-password-view'),
    path('resetpassword/<uidb64>/<token>/', views.password_validate_view, name='password-validate-view'),
    path('reset_password/', views.reset_password_view, name='reset-password-view'),
    path('my_orders/', views.my_orders_view, name='my-orders-view'),
    path('edit_profile/', views.edit_profile_view, name='edit-profile-view'),
    path('change_password/', views.change_password_view, name='change-password-view'),
    path('order_detail/<int:order_id>/', views.order_detail_view, name='order-detail-view'),

    ]
