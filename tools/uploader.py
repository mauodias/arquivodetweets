import json
import requests

class Uploader:

    CLIENT_ID = ''
    IMGUR_URL = 'https://api.imgur.com/3/image'

    def __init__(self, client_id):
        self.CLIENT_ID = client_id

    def upload(self, image_file, base64=False):
        if base64:
            contents = image_file
        else:
            contents = open(image_file, 'rb').read()
        payload = {'image': image_file}
        files = {}
        headers = {'Authorization': 'Client-ID {}'.format(self.CLIENT_ID)}
        response = json.loads(requests.post(self.IMGUR_URL, files=files, data=payload, headers=headers).text)
        result = {}
        result['status'] = response['status']
        if response['status'] is 200:
            result['image_id'] = response['data']['id']
            result['delete_hash'] = response['data']['deletehash']
            result['url'] = f'https://imgur.com/{response["data"]["id"]}'
        return result

    def delete(self, delete_hash):
        delete_url = '{}/{}'.format(self.IMGUR_URL, delete_hash)
        headers = {'Authorization': 'Client-ID {}'.format(self.CLIENT_ID)}
        response = json.loads(requests.delete(delete_url, headers=headers).text)
        return response['success']
