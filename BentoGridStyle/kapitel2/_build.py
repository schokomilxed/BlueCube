"""Baut die eigenständigen Dateien (alles eingebettet, offline lauffähig):
   ../BlauerKubus_Kapitel2_Fahrdynamik.html  (nur Film)
   ../BlauerKubus_Kapitel2_Wand.html         (Wand A·B·C + Licht + Film)
Aufruf:  python3 _build.py   (lädt die Schrift Barlow einmalig von Google Fonts)"""
import re, base64, json, os, urllib.request
os.chdir(os.path.dirname(os.path.abspath(__file__)))
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36'}

def fonts(html):
    href = re.search(r'<link href="(https://fonts.googleapis.com/[^"]+)"', html).group(1).replace('&amp;', '&')
    css = urllib.request.urlopen(urllib.request.Request(href, headers=UA)).read().decode()
    out = []
    for sub, block in re.findall(r'/\* (\S+) \*/\s*(@font-face\s*{[^}]*})', css):
        if sub != 'latin': continue
        url = re.search(r'url\((https://[^)]+)\)', block).group(1)
        data = base64.b64encode(urllib.request.urlopen(urllib.request.Request(url, headers=UA)).read()).decode()
        out.append(block.replace(url, 'data:font/woff2;base64,' + data))
    return re.sub(r'<link rel="preconnect"[^>]*>\s*<link href="https://fonts.googleapis.com[^>]*>',
                  lambda m: '<style>\n' + '\n'.join(out) + '\n</style>', html)

def assets_used():
    film = open('film.js').read()
    used = sorted(set(re.findall(r"'([\w.-]+\.(?:jpg|mp4))'", film)))
    missing = [f for f in used if not os.path.exists('assets/' + f)]
    assert not missing, missing
    return {f: ('data:video/mp4' if f.endswith('.mp4') else 'data:image/jpeg') + ';base64,' +
               base64.b64encode(open('assets/' + f, 'rb').read()).decode() for f in used}

def build(src, dst, assets):
    html = fonts(open(src).read())
    html = html.replace('<link rel="stylesheet" href="film.css">', '<style>\n' + open('film.css').read() + '</style>')
    for js in ['choreo.js', 'wand-data.js']:
        html = html.replace(f'<script src="{js}"></script>', '<script>\n' + open(js).read() + '\n</script>')
    html = html.replace('<script src="film.js"></script>',
                        '<script>window.ASSETS=' + json.dumps(assets) + ';</script>\n<script>\n' + open('film.js').read() + '\n</script>')
    for bad in ['href="film.css"', 'src="choreo.js"', 'src="film.js"', 'src="wand-data.js"', 'fonts.googleapis']:
        assert bad not in html, bad
    open(dst, 'w').write(html)
    print(f'{dst}: {len(html)/1e6:.2f} MB')

A = assets_used()
print(len(A), 'Assets:', ', '.join(A))
# Exponatbilder aus Airtable (assets/exponate/<Fach-ID>.jpg) nur für die Wand-Datei
EXP = {'exponate/' + f: 'data:image/jpeg;base64,' + base64.b64encode(open('assets/exponate/' + f, 'rb').read()).decode()
       for f in sorted(os.listdir('assets/exponate')) if f.endswith('.jpg')}
print(len(EXP), 'Exponatbilder')
build('index.html', '../BlauerKubus_Kapitel2_Fahrdynamik.html', A)
build('wand.html', '../BlauerKubus_Kapitel2_Wand.html', {**A, **EXP})
