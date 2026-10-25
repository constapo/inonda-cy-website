"""Notify participating search engines after a meaningful deployment.

Run python tools/submit_indexnow.py site|org|homes only after the public
deployment is ready. No paid services, Google indexing claims or repeated pings.
The protocol's ownership token is deliberately served as a public text file.
"""
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

HOSTS = {k: 'www.inonda.' + k for k in ['site', 'org', 'homes']}


def payload(site):
    host = HOSTS[site]
    root = 'https://' + host
    config = json.loads(Path(__file__).with_name('search-config.json').read_text())
    key = config['indexnow'][site]
    location = root + '/indexnow-key.txt'
    with urlopen(location, timeout=25) as response:
        assert response.status == 200 and response.read().decode().strip() == key, 'Deployed key mismatch'
    with urlopen(root + '/sitemap.xml', timeout=25) as response:
        tree = ET.fromstring(response.read())
    urls = list(dict.fromkeys(node.text for node in tree.findall('{*}url/{*}loc')))
    assert urls and len(urls) <= 10000
    assert all(urlsplit(url).scheme == 'https' and urlsplit(url).netloc == host for url in urls)
    return {'host': host, 'key': key, 'keyLocation': location, 'urlList': urls}


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in HOSTS:
        raise SystemExit('Usage: python tools/submit_indexnow.py site|org|homes')
    data = payload(sys.argv[1])
    request = Request('https://api.indexnow.org/indexnow', data=json.dumps(data).encode(), headers={'Content-Type': 'application/json; charset=utf-8'}, method='POST')
    with urlopen(request, timeout=35) as response:
        print(json.dumps({'host': data['host'], 'submitted_urls': len(data['urlList']), 'status': response.status, 'meaning': 'Received; crawling, indexing and ranking are not guaranteed.'}))
