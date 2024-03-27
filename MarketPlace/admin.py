from django.contrib import admin
from .models import *

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['id', 'name', 'category', 'shop']

@admin.register(ProductCategory)
class ProductCategoryModelAdmin(admin.ModelAdmin):
    model = ProductCategory
    list_display = ['id', 'name']

@admin.register(CategoryThumbnailImage)
class ProductImageModelAdmin(admin.ModelAdmin):
    model = CategoryThumbnailImage
    list_display = ['url']     

@admin.register(ProductSubCategory)
class ProductSubCategoryModelAdmin(admin.ModelAdmin):
    model = ProductSubCategory
    list_display = ['id', 'name']

@admin.register(ProductImage)
class ProductImageModelAdmin(admin.ModelAdmin):
    model = ProductImage
    list_display = ['url', 'product']     

@admin.register(UserProductRating)
class UserProductRatingModelAdmin(admin.ModelAdmin):
    model = UserProductRating
