from users.models import InstagramToken
import requests

LIMIT = 100

def get_insta_media(access_token, limit):
    after = ''
    data = []

    while True:
        insta_media = requests.get(f'https://graph.instagram.com/me/media?fields=id,media_url&access_token={access_token}&limit={limit}&after={after}')

        media_json = insta_media.json()
        data = [*data, *media_json['data']]
        
        try:
            after = media_json['paging']['cursors']['after']
        except:
            break

    return data
        

def run():
    insta_token = InstagramToken.objects.all()
    for token in insta_token:
        media_data = get_insta_media(access_token=token.access_token, limit=LIMIT)
        for data in media_data:
            print(data['media_url'])
        