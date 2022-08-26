from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import uuid

#for file
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core import files

#import component posts
from components.models import ComponentPost

#import users
from users.models import UserAccount


def main_post_media_dest(instance, filename):
    return 'main_post_media/{username}/{filename}'.format(username=instance.user.username, filename=filename)


# account_type choices class
class Categories(models.TextChoices):
    OTD = 'OTD', _('OOTD')
    SEO = 'SEO', _('Special Event Outfit')
    HOM = 'HOM', _('Home')
    BAG = 'BAG', _('Bag')
    BSH = 'BSH', _('Bookshelf')
    TLD = 'TLD', _('Travel Diaries')
    RSP = 'RSP', _('Restaurant Picks')
    MFG = 'MFG', _('Favorite Gadgets')
    MFA = 'MFA', _('Favorite Apps')
    MFM = 'MFM', _('Favorite Movies')
    SCR = 'SCR', _('Skincare Routine')

class MainPost(models.Model):
    # account_type choices class
    class MediaType(models.TextChoices):
        IMAGE = 'IM', _('Image')
        VIDEO = 'VD', _('Video')

        __empty__ = _('(Unknown)')

    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='main_posts')
    component_posts = models.ManyToManyField(ComponentPost, related_name='mainpost_components', through="MainpostComponent")
    media_url = models.FileField(upload_to=main_post_media_dest, blank=True, max_length=1000)
    media_type = models.CharField(max_length=2, choices=MediaType.choices, blank=True)
    caption = models.CharField(max_length=2000, blank=True)
    source = models.CharField(max_length=200, blank=True)
    photo_of = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='photo_of', blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    category = models.CharField(max_length=3, choices=Categories.choices, blank=True, default=Categories.OTD)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     if(self.media_type == 'IM'):
    #         im = Image.open(self.media_url)

    #         output = BytesIO()

    #         if im.height > 1024 or im.width > 1024:
    #             new_size = (1024,1024)
    #             im.thumbnail(new_size)
    #         if im.mode in ("RGBA", "P"): im = im.convert("RGB")

    #         im.save(output, format='JPEG', quality=95)
    #         output.seek(0)
    #         self.media_url = InMemoryUploadedFile(output, 'ImageField', f"{self.media_url.name.split('.')[0]}_{str(uuid.uuid4())}.jpg", 'image/jpeg', sys.getsizeof(output), None)
    #     super(MainPost, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        db_table = 'sd_main_posts'


class MainpostComponent(models.Model):
    component_post = models.ForeignKey(ComponentPost, on_delete=models.CASCADE, related_name="component_in_mainpost")
    mainpost = models.ForeignKey(MainPost, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sd_mainpost_components'
