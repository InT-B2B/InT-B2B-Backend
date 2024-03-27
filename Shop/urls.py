from django.urls import path
from . import views

urlpatterns = [
    path('shops/', views.ShopListView.as_view(), name='Shops list'),
    path('shops/company/<int:company_id>/', views.CompanyShopListView.as_view(), name='Company Shops list'),
    path('shops/<int:shop_id>/products/', views.ShopProductListView.as_view(), name='Shop Product list'),
    path('shops/<int:shop_id>/', views.ShopDetailView.as_view(), name='Shop Detail'),
]