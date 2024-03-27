from django.urls import path
from . import views

urlpatterns = [
    path('marketplace/products/', views.ProductListView.as_view(), name='Product-list'),
    path('marketplace/products/limited-offer/', views.LimitedOfferListView.as_view(), name='limited_offer'),
    path('marketplace/products/recommendations/', views.ProductRecommendationView.as_view(), name='recommendations'),
    path('marketplace/products/<int:product_id>/similar-products/', views.SimilarProductListView.as_view(), name='similar-products'), 
    path('marketplace/products/<int:product_id>/product-detail/', views.ProductDetailView.as_view(), name='product-detail'),
    
    path('marketplace/categories/',views.CategoryNameView.as_view(), name='category_name'),
    path('marketplace/categories/<int:category_id>/products/',views.CategoryProductListView.as_view(), name='category_products'),
    path('marketplace/categories/<int:category_id>/sub-category/',views.SubCategoryNameView.as_view(), name='sub_category_name'),
    path('marketplace/categories/<int:category_id>/sub-category/<int:subcategory_id>/products/',views.SubCategoryProductListView.as_view(), name='sub_category_products'),
]