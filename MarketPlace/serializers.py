from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import Product, ProductImage, ProductCategory, ProductSubCategory, CategoryThumbnailImage
from Shop.models import Shop

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['url']

class ShopSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name']

class ProductSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSubCategory
        fields = ['id', 'name']

class CategoryThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryThumbnailImage
        fields = ['id', 'url']        

class ProductCategorySerializer(serializers.ModelSerializer):
    thumbnail = CategoryThumbnailSerializer(many=False, read_only=True)

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'thumbnail']

    def to_representation(self, instance):
        thumbnails = CategoryThumbnailImage.objects.filter(category=instance)
        thumbnails_data = CategoryThumbnailSerializer(thumbnails, many=True).data
        representation = super().to_representation(instance)
        representation['thumbnails'] = thumbnails_data
        return representation                         

class ProductSerializer(serializers.ModelSerializer):
    shop = ShopSerializer1(many=False, read_only=True)
    #image = AllProductImageSerializer(many=False, read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    category = ProductCategorySerializer(many=False, read_only=True)
    sub_category = ProductSubCategorySerializer(many=False, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'shop', 'name', 'description', 'quantity', 'status', 'category', 'sub_category', 'price', 'images', 'discount_price', 'tax', 'admin_status', 'is_deleted', 'is_published', 'currency', 'updated_at', 'created_at']

    def get_images(self, obj):
        product_images = ProductImage.objects.filter(product=obj)
        return ProductImageSerializer(product_images, many=True, context=self.context).data
