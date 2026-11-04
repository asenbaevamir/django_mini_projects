from django.urls import path

from . import views

urlpatterns = [
    path('', views.lots_list, name='lots_list'),
    path('lots/<int:pk>/', views.lot_detail, name='lot_detail'),
]
