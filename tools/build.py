"""Builds public/index.html from the template and photos.json.
Run: python3 tools/build.py  (from the repo root)"""
import json, html, os
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(REPO, 'public')  # the published website
photos = json.load(open(os.path.join(REPO, 'tools', 'photos.json')))
idx = {pid: i for i, (pid, cap) in enumerate(photos)}
cap = dict(photos)
E = html.escape

def tile(pid, hidden=False, cls='tile'):
    alt = '' if hidden else E(cap[pid])
    return (f'<div class="{cls}"><img src="assets/img/gallery/{pid}-t.jpg" alt="{alt}" '
            f'loading="lazy" decoding="async" width="640" height="440"></div>')

n = len(photos)
order = [photos[(k * 37) % n][0] for k in range(n)]
order = sorted(range(n), key=lambda i: (i * 37) % n)
order = [photos[i][0] for i in order]
half = (n + 1) // 2
rowA, rowB = order[:half], order[half:]
def track(row, rev=False):
    a = '\n'.join(tile(p) for p in row)
    b = '\n'.join(tile(p, hidden=True) for p in row)
    return f'<div class="strip"><div class="track{" rev" if rev else ""}">\n{a}\n<span class="dup" aria-hidden="true">\n{b}\n</span></div></div>'

ZONES = [
 ('01','robotics','p48','Humanoids, rovers and battle-bots you can drive.'),
 ('02','retro-computing','p03','Amigas, 8-bit micros and the machines that started it all.'),
 ('03','arcade','p71','Cabinets, joysticks and home-built arcade rigs.'),
 ('04','slot-car-racing','p58','Scalextric tracks, custom cars and timed races.'),
 ('05','ai-in-action','p50','Robot arms, vision, voice and surprising uses of AI.'),
 ('06','3d-printing','d1','Printers, laser cutters and the things they make.'),
 ('07','microcontrollers','p68','Raspberry Pi, Arduino and ESP32 builds that blink and beep.'),
 ('08','radio','p27','Amateur radio, SDR and restored sets.'),
 ('09','solder','p44','Build a badge to take home. Beginners welcome.'),
 ('10','upcycling','p19','Scrap, old tech and junk given a brilliant second life.'),
 ('11','drones','p66','Home-built drones and flight controllers.'),
 ('12','schools','p53','STEM clubs, coursework and student prototypes.'),
]
zones = '\n'.join(f'''<article class="zone">{tile(pid)}<div class="zone-body"><div class="perm">drwxr-xr-x {num}</div><h3>{name}/</h3><p>{E(desc)}</p></div></article>''' for num, name, pid, desc in ZONES)

HIST = [('b0','1041 ./cyber-plus-ai --hybrid'),('b1','1042 obs --stream live --crew bcs'),('b3','1043 ./fireside --audience full'),
        ('b4','1044 cal --next-events'),('h1','1045 ./shaping-the-future --venue telford-college'),('h2','1046 ./fireside-chat --stream live')]
hist = '\n'.join(f'<figure>{tile(pid)}<figcaption>{E(line)}</figcaption></figure>' for pid, line in HIST)

tpl = open(os.path.join(REPO, 'tools', 'index.template.html')).read()
out = (tpl.replace('{{ROW_A}}', track(rowA)).replace('{{ROW_B}}', track(rowB, rev=True))
          .replace('{{ZONES}}', zones).replace('{{HIST}}', hist).replace('{{COUNT}}', str(n)))
import hashlib
def ver(*p):
    return hashlib.sha256(open(os.path.join(ROOT, *p), 'rb').read()).hexdigest()[:10]
# cache-busting: assets are cached for a week, so each file's URL changes when its content does
out = (out.replace('{{V_CSS}}', ver('assets', 'css', 'site.css'))
          .replace('{{V_JS}}', ver('assets', 'js', 'site.js')))
open(os.path.join(ROOT, 'index.html'), 'w').write(out)
print('built index.html with', n, 'photos')
