"""Fetch public-domain / CC0 museum images for a documentary long-form (Nov 19, 2026).
python3 doc_fetch.py <dir> aic:name=id ... cma:name=id ... met:name=id ...  -> <dir>/img/<name>.jpg + meta.json (merged)
AIC = Art Institute of Chicago (IIIF ,1686), CMA = Cleveland Museum of Art (CC0 API), MET = The Met Open Access."""
import json, urllib.request, os, sys
H = {'User-Agent': 'Mozilla/5.0 GNF', 'AIC-User-Agent': 'GNF (angacebiz-dev)'}
def g(u, j=True):
    r = urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=120).read(); return json.loads(r) if j else r
D = sys.argv[1] + '/img'; os.makedirs(D, exist_ok=True)
mp = f'{D}/meta.json'; meta = json.load(open(mp)) if os.path.exists(mp) else {}
for arg in sys.argv[2:]:
    src, rest = arg.split(':'); name, i = rest.split('=')
    try:
        if src == 'aic':
            o = g(f'https://api.artic.edu/api/v1/artworks/{i}?fields=id,title,artist_display,date_display,image_id,is_public_domain,medium_display')['data']
            assert o['is_public_domain'], 'not PD'
            img = g(f"https://www.artic.edu/iiif/2/{o['image_id']}/full/,1686/0/default.jpg", False)
            m = dict(src='Art Institute of Chicago', title=o['title'], artist=o['artist_display'], date=o['date_display'], medium=o.get('medium_display'))
        elif src == 'cma':
            o = g(f'https://openaccess-api.clevelandart.org/api/artworks/{i}')['data']
            assert o.get('share_license_status') == 'CC0', 'not CC0'
            img = g((o['images'].get('print') or o['images'].get('web'))['url'], False)
            m = dict(src='Cleveland Museum of Art', title=o['title'], artist=((o.get('creators') or [{}])[0].get('description') or ''), date=o.get('creation_date'), culture=o.get('culture'))
        else:
            o = g(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{i}')
            assert o['isPublicDomain'], 'not PD'
            img = g(o['primaryImage'], False)
            m = dict(src='The Met', title=o['title'], artist=o['artistDisplayName'], date=o['objectDate'], medium=o.get('medium'), culture=o.get('culture'))
        open(f'{D}/{name}.jpg', 'wb').write(img); meta[name] = m; print(name, len(img), m['title'][:60], '|', m['date'])
    except Exception as e: print('FAIL', name, e)
json.dump(meta, open(mp, 'w'), indent=1)
