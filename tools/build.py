"""Builds the website into public/ from the templates and data here.
Run: python3 tools/build.py  (from the repo root)

Pages it writes:
  public/index.html            home page (from index.template.html)
  public/zones/<slug>/index.html  one page per show-floor zone (from zones.py)
  public/about/index.html      about BCS Shropshire and BCS
  public/privacy/index.html    privacy notice for the sign-up forms
"""
import json, html, os, hashlib, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(REPO, 'public')  # the published website
sys.path.insert(0, os.path.join(REPO, 'tools'))
from zones import ZONES, FORM_KEY, CONTACT
E = html.escape

photos = json.load(open(os.path.join(REPO, 'tools', 'photos.json')))
cap = dict(photos)

def ver(*p):
    return hashlib.sha256(open(os.path.join(ROOT, *p), 'rb').read()).hexdigest()[:10]
V_CSS, V_JS = ver('assets', 'css', 'site.css'), ver('assets', 'js', 'site.js')

def img(pid, alt=None, thumb=True, cls=None):
    a = E(cap[pid] if alt is None else alt)
    c = f' class="{cls}"' if cls else ''
    src = f'/assets/img/gallery/{pid}{"-t" if thumb else ""}.jpg'
    return f'<img{c} src="{src}" alt="{a}" loading="lazy" decoding="async" width="640" height="440">'

def tile(pid, hidden=False):
    return f'<div class="tile">{img(pid, "" if hidden else None)}</div>'

# ---------------------------------------------------------------- shared parts
def head(title, desc, og_img='p65'):
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:type" content="website">
<meta property="og:image" content="/assets/img/gallery/{og_img}.jpg">
<meta name="theme-color" content="#000000">
<link rel="preload" href="/assets/fonts/barlow-condensed-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/css/site.css?v={V_CSS}">
<script src="/assets/js/site.js?v={V_JS}" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''

def header(active=''):
    links = [('/#floor', 'cd /floor', 'floor'), ('/#sponsor', 'sponsor', 'sponsor'), ('/about/', 'whoami', 'about')]
    nav = '\n'.join(f'<a href="{h}"{" aria-current=\"page\"" if k == active else ""}>{t}</a>' for h, t, k in links)
    return f'''<header class="site-head">
<div class="wrap">
<a class="lockup" href="/" aria-label="BCS Shropshire Makers &amp; Tech Showcase 2027, home">
<img src="/assets/img/bcs-logo-green.png" alt="BCS, The Chartered Institute for IT" width="191" height="240">
<span class="lockup-text" aria-hidden="true"><b>BCS Shropshire</b><span>Makers &amp; Tech</span><span>Showcase</span><span>2027</span></span>
</a>
<button type="button" class="menu-btn" aria-expanded="false" aria-controls="mainnav" aria-label="Menu"><i></i><i></i><i></i></button>
<nav class="nav" id="mainnav" aria-label="Main">
{nav}
</nav>
<a class="btn btn-green" href="#f-register" data-form>Register interest</a>
</div>
</header>
'''

FOOTER = '''<footer>
<div class="wrap">
<div>BCS Shropshire Branch · © 2026 BCS, The Chartered Institute for IT · Registered charity: England &amp; Wales 292786, Scotland SC051487.</div>
<div class="mono foot-links"><a href="/about/">./about</a> <a href="/privacy/">./privacy</a></div>
</div>
</footer>'''

# ---------------------------------------------------------------- sign-up forms
def field(name, label, typ='text', req=True, ph='', auto=''):
    r = ' required' if req else ''
    star = ' <span class="req" aria-hidden="true">*</span>' if req else ' <span class="opt">(optional)</span>'
    ac = f' autocomplete="{auto}"' if auto else ''
    return f'<label><span class="lbl">{label}{star}</span><input type="{typ}" name="{name}" placeholder="{E(ph)}"{ac}{r}></label>'

def area(name, label, ph='', req=False):
    star = ' <span class="req" aria-hidden="true">*</span>' if req else ' <span class="opt">(optional)</span>'
    return f'<label><span class="lbl">{label}{star}</span><textarea name="{name}" rows="3" placeholder="{E(ph)}"{" required" if req else ""}></textarea></label>'

def select(name, label, opts, req=True):
    o = ''.join(f'<option value="{E(v)}">{E(v)}</option>' for v in opts)
    return f'<label><span class="lbl">{label} <span class="req" aria-hidden="true">*</span></span><select name="{name}"{" required" if req else ""}><option value="">Choose…</option>{o}</select></label>'

ZONE_NAMES = [z['slug'] for z in ZONES] + ['not sure yet']

def form(fid, path, title, intro, subject, body, cmd):
    return f'''<div id="{fid}" class="modal form-modal" role="dialog" aria-modal="true" aria-labelledby="{fid}-h">
<div class="form-win">
<div class="win-bar"><span class="mono">{path}</span><a class="x" href="#close" aria-label="Close form"><svg width="18" height="18" viewBox="0 0 20 20" aria-hidden="true"><path d="M3 3l14 14M17 3L3 17" stroke="#000" stroke-width="3"/></svg></a></div>
<form class="signup" action="https://api.web3forms.com/submit" method="POST">
<h2 id="{fid}-h">{title}</h2>
<p class="form-intro">{intro}</p>
<input type="hidden" name="access_key" value="{FORM_KEY}">
<input type="hidden" name="subject" value="{E(subject)}">
<input type="hidden" name="from_name" value="Makers &amp; Tech Showcase website">
<input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="fields">{body}</div>
<label class="consent"><input type="checkbox" name="consent" value="yes" required><span>I agree BCS Shropshire can use these details to contact me about the showcase. <a href="/privacy/">Privacy notice</a></span></label>
<button type="submit" class="btn btn-lime send">{cmd}</button>
<p class="status mono" role="status" aria-live="polite"></p>
</form>
<div class="sent" hidden><p class="mono ok">$ sent ✓</p><p>Thanks. Your message is on its way to the BCS Shropshire team. We'll be in touch soon.</p><a class="btn btn-ghost x" href="#close">Close</a></div>
</div>
</div>'''

FORMS = '\n'.join([
 form('f-register', '~/forms/register-interest', 'Register interest',
      "We'll email you when the date and venue are confirmed.", 'Showcase: register interest',
      field('name', 'Name', ph='Your name', auto='name') + field('email', 'Email', 'email', ph='you@example.com', auto='email')
      + select('coming_as', 'Coming as', ['Family / with kids', 'Individual', 'Student', 'School or college group', 'Tech professional'])
      + field('group_size', 'How many of you?', 'number', req=False, ph='e.g. 4')
      + area('interests', "Anything you're keen to see?", 'Robots, retro, slot cars…'), '$ ./register --send'),
 form('f-exhibit', '~/forms/book-a-table', 'Book a table',
      'Free table, power and Wi-Fi. Tell us about your build.', 'Showcase: table request',
      field('name', 'Name', ph='Your name', auto='name') + field('email', 'Email', 'email', ph='you@example.com', auto='email')
      + field('organisation', 'Group, school or company', req=False, ph='', auto='organization')
      + select('zone', 'Zone', ZONE_NAMES)
      + area('bringing', 'What will you bring?', 'One or two lines', req=True)
      + select('power', 'Power needed', ['None', '1–2 sockets', '3–4 sockets', 'More (tell us below)'])
      + area('notes', 'Anything else?', 'Space, under-18s on your stand, accessibility…'), '$ ./book-table --send'),
 form('f-sponsor', '~/forms/sponsor-pack', 'Sponsor pack',
      "We'll send the pack and have a chat about what suits you.", 'Showcase: sponsor pack request',
      field('name', 'Name', ph='Your name', auto='name') + field('email', 'Email', 'email', ph='you@company.com', auto='email')
      + field('company', 'Company', ph='Company name', auto='organization') + field('phone', 'Phone', 'tel', req=False, auto='tel')
      + select('interest', 'Interested in', ['Headline partner', 'Zone sponsor', 'Kit & prizes', 'Venue partner', 'Not sure yet'])
      + area('message', 'Message'), '$ ./sponsor --request-pack'),
 form('f-contact', '~/forms/contact', 'Get in touch',
      "Questions about the showcase or BCS Shropshire? Send us a message.", 'Showcase: general enquiry',
      field('name', 'Name', ph='Your name', auto='name') + field('email', 'Email', 'email', ph='you@example.com', auto='email')
      + area('message', 'Message', req=True), '$ ./contact --send'),
])

def page(path, html_doc):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w').write(html_doc)

def tail():
    return f'{FOOTER}\n{FORMS}\n</body>\n</html>\n'

# ---------------------------------------------------------------- home page
n = len(photos)
order = [photos[i][0] for i in sorted(range(n), key=lambda i: (i * 37) % n)]
half = (n + 1) // 2
def track(row, rev=False):
    a = '\n'.join(tile(p) for p in row)
    b = '\n'.join(tile(p, hidden=True) for p in row)
    return f'<div class="strip"><div class="track{" rev" if rev else ""}">\n{a}\n<span class="dup" aria-hidden="true">\n{b}\n</span></div></div>'

zones_html = '\n'.join(
    f'<a class="zone" href="/zones/{z["slug"]}/">{tile(z["card"])}<div class="zone-body"><div class="perm">drwxr-xr-x {z["num"]}</div>'
    f'<h3>{z["slug"]}/</h3><p>{E(z["short"])}</p><span class="go mono">cd {z["slug"]}/ →</span></div></a>' for z in ZONES)

HIST = [('b0','1041 ./cyber-plus-ai --hybrid'),('b1','1042 obs --stream live --crew bcs'),('b3','1043 ./fireside --audience full'),
        ('b4','1044 cal --next-events'),('h1','1045 ./shaping-the-future --venue telford-college'),('h2','1046 ./fireside-chat --stream live')]
hist = '\n'.join(f'<figure>{tile(pid)}<figcaption>{E(line)}</figcaption></figure>' for pid, line in HIST)

tpl = open(os.path.join(REPO, 'tools', 'index.template.html')).read()
out = (tpl.replace('{{ROW_A}}', track(order[:half])).replace('{{ROW_B}}', track(order[half:], rev=True))
          .replace('{{ZONES}}', zones_html).replace('{{HIST}}', hist).replace('{{COUNT}}', str(n))
          .replace('{{FOOTER}}', FOOTER).replace('{{FORMS}}', FORMS)
          .replace('{{V_CSS}}', V_CSS).replace('{{V_JS}}', V_JS))
page('index.html', out)

# ---------------------------------------------------------------- zone pages
def linklist(items):
    return '<ul class="links">' + ''.join(f'<li><a href="{E(u)}">{E(t)}</a></li>' for t, u in items) + '</ul>'

for i, z in enumerate(ZONES):
    prev, nxt = ZONES[i - 1], ZONES[(i + 1) % len(ZONES)]
    cards = '\n'.join(f'<article class="card">{img(pid, alt)}<div><p class="file mono">{E(f)}</p><h3>{E(t)}</h3><p>{E(d)}</p></div></article>'
                      for pid, alt, f, t, d in z['cards'])
    ideas = '\n'.join(f'<li><span class="mono">[{k+1}]</span> {E(t)}</li>' for k, t in enumerate(z['ideas']))
    title = z['title']
    doc = head(f'{title} | Makers & Tech Showcase 2027 | BCS Shropshire', z['intro'], z['hero']) + header('floor') + f'''
<main id="main">
<section class="zone-hero grid-bg">
<div class="wrap">
<div class="zh-copy">
<p class="prompt"><span class="u">maker@bcs-shropshire</span>:<span class="p">~</span>$ cd /show-floor/{z["slug"]}</p>
<h1 class="zh-title">{E(title)}<span>/</span></h1>
<p class="intro">{E(z["intro"])}</p>
<p class="tags mono"><span>ages: all</span><span class="on">exhibitor sign-up: open</span><span>zone: {z["num"]}/{len(ZONES):02d}</span></p>
</div>
<div class="zh-img">{img(z["hero"], thumb=False)}</div>
</div>
</section>

<section class="section light" aria-labelledby="about-h">
<div class="wrap">
<p class="cmd">$ cat ./README.md</p>
<h2 id="about-h" class="h2">What this zone is all about</h2>
<p class="lead">{E(z["about"])}</p>
<div class="cards">
{cards}
</div>
</div>
</section>

<section class="section grid-bg" aria-labelledby="ideas-h">
<div class="wrap two-col">
<div>
<p class="cmd">$ ./have-a-go --list</p>
<h2 id="ideas-h" class="h2">Hands-on ideas</h2>
<ol class="ideas">
{ideas}
</ol>
</div>
<div class="exhibit-box">
<p class="cmd">$ ./exhibit --zone {z["slug"]}</p>
<h3>{E(z["exhibit"])}</h3>
<p>Free table, power and Wi-Fi. Clubs, schools, colleges, companies and lone builders all welcome.</p>
<a class="btn btn-lime" href="#f-exhibit" data-form data-zone="{z["slug"]}">Exhibit in {z["slug"]}</a>
</div>
</div>
</section>

<section class="section light" aria-labelledby="more-h">
<div class="wrap two-col">
<div>
<p class="cmd">$ cat get-started.txt</p>
<h2 id="more-h" class="h2">Get started at home</h2>
{linklist(z["home"])}
<p class="cmd more-cmd">$ curl bcs.org/{z["slug"]}</p>
<h3 class="more-h3">Read more from BCS</h3>
{linklist(z["bcs"])}
</div>
<div class="sponsor-box">
<p class="cmd">zone-sponsor/</p>
<h3>{E(title)}, presented by [you]</h3>
<p>This zone is available to sponsor. Your name on the zone, this page and the day.</p>
<a class="btn btn-ghost" href="#f-sponsor" data-form>Request a sponsor pack</a>
</div>
</div>
</section>

<nav class="zone-nav mono wrap" aria-label="Zones">
<a href="/zones/{prev["slug"]}/">← cd ../{prev["slug"]}</a>
<a href="/#floor">cd ../ (all zones)</a>
<a href="/zones/{nxt["slug"]}/">cd ../{nxt["slug"]} →</a>
</nav>
</main>
''' + tail()
    page(f'zones/{z["slug"]}/index.html', doc)

# ---------------------------------------------------------------- about page
OFFERS = [
 ('join.md', 'Become a member', 'Professional membership, networking and career tools.', 'https://www.bcs.org/membership-and-registrations/become-a-member/'),
 ('students.md', 'Students & academics', 'Membership for students, apprentices and educators.', 'https://www.bcs.org/membership-and-registrations/academic-membership/'),
 ('citp.md', 'Chartered IT Professional', 'CITP, the standard for IT professionals.', 'https://www.bcs.org/membership-and-registrations/get-registered/chartered-it-professional/'),
 ('certs.md', 'Certifications', 'Industry certifications, from AI to testing.', 'https://www.bcs.org/qualifications-and-certifications/certifications-for-professionals/'),
 ('careers.md', 'Careers & apprenticeships', 'Routes into tech for school leavers and career changers.', 'https://www.bcs.org/it-careers/'),
 ('teach.md', 'For schools & colleges', 'Qualifications and support for teachers.', 'https://www.bcs.org/deliver-and-teach-qualifications/teachers-schools-and-colleges/'),
 ('groups.md', 'Specialist groups', '50+ groups, from retro computing to green IT.', 'https://www.bcs.org/membership-and-registrations/member-communities/'),
 ('volunteer.md', 'Volunteer', 'Help run branches, events and outreach.', 'https://www.bcs.org/membership-and-registrations/member-communities/volunteering-with-bcs/'),
]
offers = '\n'.join(f'<a class="offer" href="{u}"><span class="file mono">{f}</span><h3>{E(t)} <span aria-hidden="true">→</span></h3><p>{E(d)}</p></a>' for f, t, d, u in OFFERS)
page('about/index.html', head('About | Makers & Tech Showcase 2027 | BCS Shropshire',
     'About BCS Shropshire and BCS, The Chartered Institute for IT, who run the Makers & Tech Showcase.', 'h1') + header('about') + f'''
<main id="main">
<section class="zone-hero grid-bg">
<div class="wrap"><div class="zh-copy">
<p class="prompt"><span class="u">maker@bcs-shropshire</span>:<span class="p">~</span>$ whoami</p>
<h1 class="zh-title">About us<span>/</span></h1>
<p class="intro">The Makers &amp; Tech Showcase is run by volunteers from BCS Shropshire, the local branch of BCS, The Chartered Institute for IT.</p>
</div></div>
</section>

<section class="section light">
<div class="wrap two-col">
<div>
<p class="cmd">$ cat shropshire.md</p>
<h2 class="h2">BCS Shropshire</h2>
<p>We bring together people across Shropshire and Telford who work with, study or just love technology. We run talks, round tables and fireside chats on topics from AI and quantum computing to cyber security.</p>
<p>Everyone is welcome, members and non-members alike, and most of our events are free.</p>
<p class="btns"><a class="btn btn-green" href="https://www.bcs.org/membership-and-registrations/member-communities/shropshire-branch/">Branch page</a> <a class="btn btn-outline" href="https://www.bcs.org/membership-and-registrations/member-communities/shropshire-branch/past-events">Past events</a></p>
</div>
<div>
<p class="cmd">$ cat bcs.md</p>
<h2 class="h2">BCS</h2>
<p>BCS, The Chartered Institute for IT, is the UK's professional body for IT. Founded in 1957, it's a charity with a Royal Charter and over 70,000 members in 150 countries.</p>
<p>Its mission is to make sure everyone's experience with technology is positive, by raising standards across the profession.</p>
<p class="btns"><a class="btn btn-green" href="https://www.bcs.org/">Visit bcs.org</a> <a class="btn btn-outline" href="https://www.bcs.org/about-us/">About BCS</a></p>
</div>
</div>
</section>

<section class="section light rule">
<div class="wrap">
<p class="cmd">$ ls bcs.org/</p>
<h2 class="h2">What BCS offers</h2>
<div class="offers">
{offers}
</div>
<p class="also">Plus free <a href="https://www.bcs.org/articles-opinion-and-research/">articles and research</a> and a UK-wide <a href="https://www.bcs.org/events-calendar/">events calendar</a>.</p>
<p class="credits mono">credits: stock photos and video from <a href="https://www.pexels.com/">Pexels</a> &amp; <a href="https://pixabay.com/">Pixabay</a> · "How To Hack Time" by <a href="https://www.youtube.com/@LaserUnicorns">LaserUnicorns</a> · fonts: Barlow &amp; JetBrains Mono (SIL Open Font Licence)</p>
</div>
</section>

<section class="section grid-bg">
<div class="wrap get-involved">
<div><p class="cmd">$ ./get-involved</p><h3>Get in touch to find out more</h3></div>
<a class="btn btn-lime" href="#f-contact" data-form>Get in touch</a>
</div>
</section>
</main>
''' + tail())

# ---------------------------------------------------------------- privacy notice
page('privacy/index.html', head('Privacy notice | Makers & Tech Showcase 2027 | BCS Shropshire',
     'How BCS Shropshire uses the details you send through the showcase website forms.') + header() + f'''
<main id="main">
<section class="section light prose">
<div class="wrap">
<p class="cmd">$ man privacy</p>
<h1 class="h2">Privacy notice</h1>
<p>This notice covers the forms on this website: register interest, book a table, sponsor pack and get in touch.</p>
<h2>Who we are</h2>
<p>The Makers &amp; Tech Showcase is run by volunteers from the Shropshire Branch of BCS, The Chartered Institute for IT. BCS is a registered charity (England &amp; Wales 292786, Scotland SC051487), registered office 3 Newbridge Square, Swindon SN1 1BY. BCS's own privacy policy is at <a href="https://www.bcs.org/">bcs.org</a>.</p>
<h2>What we collect and why</h2>
<p>Only what you type into a form: usually your name, email address and your message, plus anything else the form asks for (such as the zone and power you need, or your company). We use it to reply to you and to organise the showcase. The legal basis is your consent, which you give by ticking the box on the form.</p>
<h2>How it reaches us</h2>
<p>When you press send, your details go through <a href="https://web3forms.com/">Web3Forms</a>, a form service that turns them into an email to the organising team at {CONTACT}. We don't add you to any mailing list, sell your details or share them outside the organising team.</p>
<h2>How long we keep it</h2>
<p>Until the showcase is over and any follow-up is done, and no later than 31 December 2027, unless you ask us to keep in touch about future events.</p>
<h2>Your rights</h2>
<p>You can ask to see, correct or delete your details, or withdraw consent, at any time. Email {CONTACT}. If you're unhappy with how we've handled your data you can complain to the <a href="https://ico.org.uk/">Information Commissioner's Office</a>.</p>
<h2>Cookies</h2>
<p>This site sets no cookies and uses no analytics. The retro TV video only loads from YouTube (privacy-enhanced mode) when you press play.</p>
<p class="mono small">Last updated: November 2026</p>
</div>
</section>
</main>
''' + tail())

print('built home,', len(ZONES), 'zone pages, about, privacy;', n, 'photos')

# keep the 404 page's stylesheet link in step with the current CSS
import re
p404 = os.path.join(ROOT, '404.html')
s404 = open(p404).read()
open(p404, 'w').write(re.sub(r'site\.css\?v=[\w]+', f'site.css?v={V_CSS}', s404))
