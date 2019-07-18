import requests
import archiveis
import json

class Archiver():


    @staticmethod
    def archive_wayback(url):
        if url[:-1] is not '/':
            url = url+'/'
        WAYBACK_API_URL = 'https://pragma.archivelab.org/'
        WAYBACK_ARCHIVED_URL = 'https://web.archive.org'

        data = {'url': url}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(WAYBACK_API_URL, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            wayback_url = json.loads(response.text)['wayback_id']
            return '{}{}'.format(WAYBACK_ARCHIVED_URL, wayback_url)
        else:
            return response.status_code

    @staticmethod
    def archive_is(url):
        return archiveis.capture(url)
