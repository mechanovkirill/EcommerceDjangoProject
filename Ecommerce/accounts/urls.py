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

    ]
