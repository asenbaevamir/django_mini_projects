from django.urls import path

from . import views

urlpatterns = [
    path('', views.lots_list, name='lots_list'),
    path('lots/create/', views.lot_create, name='lot_create'),
    path('lots/<int:pk>/', views.lot_detail, name='lot_detail'),
    path('lots/<int:pk>/bid/', views.place_bid, name='place_bid'),
    path('lots/<int:pk>/buy-now/', views.buy_now, name='buy_now'),
]
