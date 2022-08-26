from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from components.models import ComponentPost
from django.utils.translation import gettext_lazy as _
from PIL import Image
from django.db.models.signals import post_save
from allauth.socialaccount.models import SocialAccount

from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import uuid

#for instagram token expire date
from datetime import datetime, timedelta
from django.utils import timezone

#for profile picture social login
import urllib3
import requests
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from django.dispatch import receiver


def pro_pic_dest(instance, filename):
    return 'profile_pictures/{user}/{filename}'.format(user=instance.username, filename=filename)


class UserManager(BaseUserManager):
    def create_user(self, username, email, name, password=None, **extra_fields):
        if not username:
            raise ValueError('Username required')

        if not email:
            raise ValueError('Email required')

        email = self.normalize_email(email)
        username = username.lower()
        user = self.model(username=username, email=email, name=name, **extra_fields)

        user.set_password(password)
        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    # account_type choices class
    class AccountType(models.TextChoices):
        PERSONAL = 'PR', _('Personal')
        GENERAL_INFLUENCER = 'GI', _('Influencer')
        LIFESTYLE_INFLUENCER = 'LI', _('Lifestyle Influencer')
        FASHION_INFLUENCER = 'FI', _('Fashion Influencer')
        TRAVEL_INFLUENCER = 'TI', _('Travel Influencer')
        BRAND = 'BR', _('Brand')
        ADMIN = 'AD', _('Admin')
        CELEB = 'CL', _('Celeb')
        HOME_INFLUENCER = 'HI', _('Home Influencer')

        __empty__ = _('(Unknown)')
    
    # provider type
    class ProviderType(models.TextChoices):
        EMAIL = 'email', _('Email')
        FACEBOOK = 'facebook', _('Facebook')

        __empty__ = _('(Unknown)')

    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    account_type = models.CharField(max_length=2, choices=AccountType.choices, default=AccountType.PERSONAL)
    provider = models.CharField(max_length=10, choices=ProviderType.choices, default=ProviderType.EMAIL)
    modified_username = models.BooleanField(default=False, blank=True)
    profile_picture = models.ImageField(upload_to=pro_pic_dest, blank=True, max_length=1000)
    user_bio = models.CharField(max_length=500, blank=True, default='')
    user_website = models.URLField(max_length=2000, blank=True, default='')
    is_premium = models.BooleanField(default=False)
    sent_insta_email = models.BooleanField(default=False, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    wishlist = models.ManyToManyField(ComponentPost, related_name='wishlist', through="Wishlist")

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    
    # def save(self, *args, **kwargs):
    #     if(self.profile_picture):
    #         im = Image.open(self.profile_picture)
    #         output = BytesIO()

    #         if im.height > 300 or im.width > 300:
    #             new_size = (300,300)
    #             im.thumbnail(new_size)
    #         if im.mode in ("RGBA", "P"): im = im.convert("RGB")

    #         im.save(output, format='JPEG', quality=95)
    #         output.seek(0)
    #         self.profile_picture = InMemoryUploadedFile(output, 'ImageField', f"{self.profile_picture.name.split('.')[0]}_{str(uuid.uuid4())}.jpg", 'image/jpeg', sys.getsizeof(output), None)
    #     super(UserAccount, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'sd_users'
    



def name_from_url(url):
    try:
        from urllib.parse import urlparse
    except ImportError:
        from urlparse import urlparse
    p = urlparse(url)
    for base in (p.path.split('/')[-1],
                 p.path,
                 p.netloc):
        name = ".".join(filter(lambda s: s,
                               map(slugify, base.split("."))))
        if name:
            return name+'.jpg'


def save_profile(sender, instance, **kwargs):
    if instance.provider == "facebook" :
        instance.user.name = instance.extra_data['name']
        instance.user.email = instance.extra_data['email']
        instance.user.provider = instance.provider
        uid = instance.extra_data['id']
        url = instance.get_avatar_url()
        if url:
            try:
                http = urllib3.PoolManager()
                content = requests.get(url)
                name = name_from_url(url)
                instance.user.profile_picture.save(instance.extra_data['id']+'.jpg', ContentFile(content.content))

            except IOError:
                print('smething went wrong')

        else:
            instance.user.save()
    elif instance.provider == 'instagram':
        instance.user.name = instance.extra_data['username']
        instance.user.provider = instance.provider
        uid = instance.extra_data['id']
        instance.user.save()

post_save.connect(save_profile, sender=SocialAccount)


class Wishlist(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="wishlist_user")
    wishlist_item = models.ForeignKey(ComponentPost, on_delete=models.CASCADE, related_name="wishlist_item")
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sd_wishlists'

def get_expire_date():
    return timezone.now()+timedelta(days=60)

class InstagramToken(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="insta_user")
    insta_id = models.CharField(max_length=50)
    access_token = models.CharField(max_length=250)
    last_post = models.CharField(max_length=100, blank=True, default='')
    expires_on = models.DateTimeField(default=get_expire_date)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sd_insta_tokens'