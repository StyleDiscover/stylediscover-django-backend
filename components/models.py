from django.db import models
from PIL import Image

from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import uuid


def component_pic_dest(instance, filename):
    return 'component_pictures/{filename}'.format(filename=filename)


class SiteRecord(models.Model):
    hostname = models.CharField(max_length=150, unique=True)
    xpath = models.CharField(max_length=1000)
    shop_site = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sd_site_records'


class ComponentPost(models.Model):
    site_records = models.ForeignKey(SiteRecord, on_delete=models.CASCADE, related_name="site_records")
    media_url = models.ImageField(upload_to=component_pic_dest, blank=True, max_length=1000)
    page_url = models.URLField(max_length=1000)
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     im = Image.open(self.media_url)
    #     output = BytesIO()

    #     if im.height > 500 or im.width > 500:
    #         new_size = (500,500)
    #         im.thumbnail(new_size)
    #     if im.mode in ("RGBA", "P"): im = im.convert("RGB")

    #     im.save(output, format='JPEG', quality=95)
    #     output.seek(0)
    #     self.media_url = InMemoryUploadedFile(output, 'ImageField', f"{self.media_url.name.split('.')[0]}_{str(uuid.uuid4())}.jpg", 'image/jpeg', sys.getsizeof(output), None)
    #     super(ComponentPost, self).save(*args, **kwargs)


    class Meta:
        db_table = 'sd_component_posts'