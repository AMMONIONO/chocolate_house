from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.place_order, name='place_order'),
    path('order_history/', views.order_history, name='order_history'),
    path('refill/', views.refill_page, name='refill_ingredient'),
    path('', views.home, name='home'),
]
