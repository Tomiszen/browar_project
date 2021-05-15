from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('beers/', views.beer_list, name='beer_list'),
    path('beers/<str:beer>/',
         views.beer_detail,
         name='beer_detail'),
    path('stock/', views.stock_list, name='product_list'),
    path('stock/<int:id>/', views.product_detail, name='product_detail'),
]
