from users.models import InstagramToken
import requests

LIMIT = 1

def get_last_media(access_token, limit):
    insta_media = requests.get(f'https://graph.instagram.com/me/media?fields=id,media_url&access_token={access_token}&limit={limit}')

    media_json = insta_media.json()
    data = media_json['data']
    
    return data
        
def check_last_post(token, last_post_id):
    if token.last_post == '' or token.last_post != last_post_id:
        InstagramToken.objects.filter(id=token.id).update(last_post=last_post_id)
        return True
    else:
        return False

def run():
    insta_token = InstagramToken.objects.all()
    response = ''
    for token in insta_token:
        media_data = get_last_media(access_token=token.access_token, limit=LIMIT)
        last_post_id = media_data[0]['id']
        last_post_media_url = media_data[0]['media_url']
        response = check_last_post(token=token, last_post_id=last_post_id)
        if response == True:
            print(last_post_media_url)
    return response