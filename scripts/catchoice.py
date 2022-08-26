from mainposts.models import MainPost

def run(*args):
    choices = MainPost._meta.get_field('category').choices
    print(choices)