from helpers.models import TimestampsModel
from django.db import models



class Cart(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cart'

class LastViewedProduct(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)
    viewed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'last_viewed_product'

class Order(models.Model):
    id = models.UUIDField(primary_key=True)
    customer = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    vat = models.DecimalField(db_column='VAT', max_digits=10, decimal_places=2)  # Field name made lowercase.
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.TextField()  # This field type is a guess.
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)
    customer = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    merchant = models.ForeignKey('User', models.DO_NOTHING, related_name='orderitem_merchant_set', blank=True, null=True)
    order_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_vat = models.DecimalField(db_column='order_VAT', max_digits=10, decimal_places=2)  # Field name made lowercase.
    order_discount = models.DecimalField(max_digits=10, decimal_places=2)
    promo = models.ForeignKey('Promotion', models.DO_NOTHING, blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'order_item'

class Product(models.Model):
    id = models.UUIDField(primary_key=True)
    shop = models.ForeignKey('Shop', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    quantity = models.BigIntegerField()
    category = models.ForeignKey('ProductCategory', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    admin_status = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    rating = models.ForeignKey('UserProductRating', models.DO_NOTHING, blank=True, null=True)
    is_published = models.BooleanField()
    currency = models.CharField(max_length=10)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    sub_category = models.ForeignKey('ProductSubCategory', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'


class ProductCategory(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=225, blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_category'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    url = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'product_image'

class ProductReview(models.Model):
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    reply = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_review'


class ProductSubCategory(models.Model):
    name = models.CharField(max_length=225, blank=True, null=True)
    parent_category = models.ForeignKey(ProductCategory, models.DO_NOTHING, blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_sub_category'

class PromoProduct(models.Model):
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    promo = models.ForeignKey('Promotion', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'promo_product'


class Promotion(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    code = models.CharField(max_length=255)
    promotion_type = models.CharField(max_length=255)
    discount_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    quantity = models.BigIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    maximum_discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'promotion'

class Wishlist(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wishlist'                                                        