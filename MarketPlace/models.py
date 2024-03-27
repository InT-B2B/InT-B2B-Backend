from django.db import models

from helpers.models import TimestampsModel
from Accounts.models import CustomUser, Company;
from Shop.models import Shop;

class ProductStatus(models.TextChoices):
    inStoke = 'inStoke'
    lowStoke = 'lowStoke'
    outOfStoke = 'outOfStoke'

class ProductAdminStatus(models.TextChoices):
    approved = 'approved' 
    notApproved = 'notApproved'

class Product(TimestampsModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=25, choices=ProductStatus.choices)
    quantity = models.BigIntegerField()
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)
    sub_category = models.ForeignKey('ProductSubCategory', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    has_discount = models.BooleanField()
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    admin_status = models.TextField(choices=ProductAdminStatus.choices, blank=True, null=True)
    is_published = models.BooleanField()
    is_deleted = models.BooleanField(default=False)
    currency = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

class LastViewedProduct(TimestampsModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField()

class ProductCategory(TimestampsModel):
    name = models.CharField(max_length=225)
    description = models.CharField(max_length=255, blank=True,)

    def __str__(self) -> str:
        return self.name
    
class CategoryThumbnailImage(TimestampsModel):
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)
    url = models.CharField(max_length=255)    

class ProductSubCategory(TimestampsModel):
    name = models.CharField(max_length=225, blank=True, null=True)
    description = models.CharField(max_length=255)
    parent_category = models.ForeignKey('ProductCategory', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class ProductImage(TimestampsModel):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    url = models.CharField(max_length=255)

class ProductReview(TimestampsModel):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    reply = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

class UserProductRating(TimestampsModel):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField()

class Cart(TimestampsModel):
    user = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', blank=True, null=True, on_delete=models.CASCADE)        

class PromoProduct(TimestampsModel):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    promo = models.ForeignKey('Promotion', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Promotion(TimestampsModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    code = models.CharField(max_length=255)
    promotion_type = models.CharField(max_length=255)
    discount_type = models.TextField(blank=True, null=True)
    quantity = models.BigIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    maximum_discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

class Order(TimestampsModel):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vat = models.DecimalField(db_column='VAT', max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.TextField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)


class OrderItem(TimestampsModel):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    merchant = models.ForeignKey(CustomUser, related_name='orderItem_merchant', on_delete=models.CASCADE)
    order_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_vat = models.DecimalField(db_column='order_VAT', max_digits=10, decimal_places=2)
    order_discount = models.DecimalField(max_digits=10, decimal_places=2)
    promo = models.ForeignKey('Promotion', blank=True, null=True, on_delete=models.CASCADE)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)        

class Wishlist(TimestampsModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)                                                      