from mainposts.models import MainPost

def run(*args):
    data = MainPost.objects.all()
    data.update(category='OTD')
