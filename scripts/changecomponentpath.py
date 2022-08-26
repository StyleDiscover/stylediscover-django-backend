from components.models import ComponentPost
import os

def run(*args):
    mp_list = ComponentPost.objects.all().values()
    if 'imagepath':
        for list in mp_list:
            list_item = ComponentPost.objects.get(id=list['id'])
            image_name = os.path.split(list_item.media_url.name)[1]
            image_name = image_name.split('.')[:-1]
            image_name = '.'.join(image_name)
            image_name = image_name + '.jpg'
            new_path = f"component_pictures/converted/{image_name}"
            list_item.media_url = new_path
            list_item.save()