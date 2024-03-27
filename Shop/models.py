from django.db import models
from cloudinary.models import CloudinaryField

from helpers.fields import ValidatedImageField
from helpers.models import TimestampsModel
from Accounts.models import CustomUser, Company

class ShopOwner(TimestampsModel):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='shop_owner')
    is_approved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return 'Shop Owner: ' + self.company.__str__()

class Shop(TimestampsModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    merchant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    logo = CloudinaryField(null=True, blank=True)
    cover_image = CloudinaryField(null=True, blank=True)
    is_deleted = models.TextField(default=False)

    def __str__(self) -> str:
        return self.name.__str__()