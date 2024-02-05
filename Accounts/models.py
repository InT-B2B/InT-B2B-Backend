from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from helpers.models import TimestampsModel
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class UserType(models.TextChoices):
    SELLER = 'Seller'
    BUYER = 'Buyer'

class CustomUser(AbstractBaseUser, PermissionsMixin, TimestampsModel):
    email = models.EmailField(_('email_address'), unique=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff_status'), default=False)
    is_verified = models.BooleanField(_('verified'), default=False)
    is_approved = models.BooleanField(_('approved'), default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'


class UserProfile(TimestampsModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    managerFirstName = models.CharField(_('first_name'), max_length=30)
    managerMiddleName = models.CharField(_('middle_name'), max_length=30)
    managerLastName = models.CharField(_('last_name'), max_length=30)
    managerCountry = models.CharField(_("managers_location_country"), max_length=50)
    managerRegion = models.CharField(_("managers_location_region"), max_length=50)
    managerZone = models.CharField(_("managers_location_zone"), max_length=50)
    managerWoreda = models.CharField(_("managers_location_woreda"), max_length=50)
    managerKebele = models.CharField(_("managers_location_kebele"), max_length=50)
    managerPhoneNumber = models.CharField(_('phone_number'), max_length=15, blank=True)
    userRole = models.CharField(_('user_type'), max_length=25, choices=UserType.choices)
    managerRenewedIDFront = models.ImageField(upload_to='user_IDs/')
    managerRenewedIDBack = models.ImageField(upload_to='user_IDs/')
    profilePic = models.ImageField(upload_to='user_profile_pics/', null=True, blank=True)


class Company(TimestampsModel):
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    companyName = models.CharField(_('company_name'), max_length=50)
    companyCountry = models.CharField(_("companys_location_country"), max_length=50)
    companyRegion = models.CharField(_("companys_location_region"), max_length=50)
    companyZone = models.CharField(_("companys_location_zone"), max_length=50)
    companyWoreda = models.CharField(_("companys_location_woreda"), max_length=50)
    companyKebele = models.CharField(_("companys_location_kebele"), max_length=50)
    companyHN = models.CharField(_('H_N'), max_length=25)
    companyTIN = models.CharField(_('TIN'), max_length=25)
    companyPhoneNumber = models.CharField(_('phone_number'), max_length=15, blank=True)
    companyLicense = models.ImageField(upload_to='company_licences/')
    companyLogo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
