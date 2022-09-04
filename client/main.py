import hashlib
import os

import requests
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth(username='qqq', password='qqq')

file = 'BioShock - Trailer.mp4'

size = os.path.getsize(file)

hash_md5 = hashlib.md5()

CHUNK_SIZE = 2097152

with open(file, 'rb') as f:
    url = 'http://localhost:8000/toserver/'
    offset = 0
    for chunk in iter(lambda: f.read(CHUNK_SIZE), b''):
        hash_md5.update(chunk)
        res = requests.put(
            url,
            data={'filename': file},
            files={'file': chunk},
            headers={
                'Content-Range': f'bytes {offset}-{offset + len(chunk) -1}/{size}'
            },
            auth=auth
        )
        print(res)
        offset = int(res.json().get('offset'))
        url = res.json().get('url')
    finalize = requests.post(
        url,
        data={'md5': hash_md5.hexdigest()},
        auth=auth
    )
    print(finalize.status_code)
    print(finalize.json())