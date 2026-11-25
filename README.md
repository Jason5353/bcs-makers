# BCS Shropshire · Maker & Tech Showcase 2027

The static website for the BCS Shropshire Branch Maker & Tech Showcase.
Plain HTML, CSS and JavaScript: no frameworks, no build step needed to deploy.

## What's in here

```
index.html                 the page (generated, see "Editing" below)
404.html                   "Wrong timeline" not-found page
_headers                   security headers for Cloudflare Pages
favicon.svg, robots.txt
assets/css/site.css        all styling (BCS palette only)
assets/js/site.js          typed headline, photo viewer, strip pause, retro TV
assets/js/photos.js        photo list for the viewer (generated)
assets/fonts/              self-hosted Barlow + JetBrains Mono (SIL OFL, licences included)
assets/img/gallery/        85 photos: <id>.jpg (full) and <id>-t.jpg (thumbnail)
tools/build.py             rebuilds index.html and photos.js
tools/index.template.html  the page template you edit
tools/photos.json          photo ids and captions
```

## Deploy: GitHub + Cloudflare (Workers static assets)

The repo is connected to a Cloudflare Worker called **bcs-makers**. Every push to `main` runs `npx wrangler deploy`, which publishes the files listed by `wrangler.jsonc` (everything except what `.assetsignore` leaves out: README, tools, config). `_headers` and `404.html` work the same as on Pages.

### Original Pages instructions (if you ever move back to Pages)

1. **Create the repo.** On GitHub, create a new repository, e.g. `bcs-shropshire/maker-showcase` (public or private both work).
2. **Push the files.** From this folder:
   ```bash
   git init
   git add .
   git commit -m "Maker & Tech Showcase site"
   git branch -M main
   git remote add origin git@github.com:<your-org>/maker-showcase.git
   git push -u origin main
   ```
3. **Connect Cloudflare Pages.** Cloudflare dashboard → Workers & Pages → Create → Pages → Connect to Git → pick the repo.
   - Framework preset: **None**
   - Build command: *(leave empty)*
   - Build output directory: **/**
4. **Deploy.** You get a `*.pages.dev` address straight away. Every push to `main` redeploys automatically; other branches get preview URLs.
5. **Custom domain (optional).** Pages project → Custom domains → add e.g. `showcase.bcs-shropshire.org`. If the domain's DNS is on Cloudflare it's one click; otherwise add the CNAME it shows you at your DNS host.

## Editing

Edit `tools/index.template.html` (page text), `tools/photos.json` (photos and captions), or the zone list in `tools/build.py`, then run:

```bash
python3 tools/build.py
```

That regenerates `index.html` and `assets/js/photos.js`. Commit and push.
Quick text fixes can also be made straight in `index.html`, but they'll be overwritten next time the build runs.

### Before going live: placeholders to fill

- [ ] **Date and venue:** search for `[DD Month]`, `[Venue]` and `[Telford / Shrewsbury]`.
- [x] **BCS logo:** the official green logo with the event name lock-up is in the header (`assets/img/bcs-logo-green.png`). If BCS asks for the newer black logo instead, swap the image file and keep the lock-up text.
- [ ] **Partner logos:** replace the `[Headline partner]` etc. boxes once sponsors have agreed. Don't add company names or logos before they've said yes.
- [ ] **Sign-up links:** "Register interest", "Book a table" and "Request a sponsor pack" currently open an email to jason.lewis@bcs-shropshire.org. Swap them for a Microsoft Form / Google Form / Tally link when you have one (search for `mailto:`). If the form is on another domain, nothing in `_headers` needs changing because these are plain links.
- [ ] **Typeface:** the site uses Barlow as a free stand-in for DIN Next Pro. If BCS can supply a web licence for DIN Next Pro, add the files to `assets/fonts/` with `@font-face` rules; the CSS already lists "DIN Next Pro" first.
- [ ] **Command-line font:** command lines use JetBrains Mono. If BCS wants the brand font only, change `--mono` in `site.css` to `var(--sans)`.

## The retro TV (Hackerman's tutorial)

- Clicking the TV loads Laser Unicorns' official upload of **Hackerman's Hacking Tutorials: How To Hack Time** (`KEkrWRHCDQU`) from `youtube-nocookie.com`. Nothing is downloaded or re-hosted.
- No YouTube cookies or requests happen until someone clicks play.
- Without JavaScript the TV is a plain link to the video on YouTube.
- If the player ever says "Video unavailable", the uploader has changed the embed settings; the "Watch on YouTube" link still works.
- Showing it **on a screen at the event** is a public screening and isn't covered by embedding. Ask Laser Unicorns (via kungfury.com) first.

## Security headers (`_headers`)

Cloudflare Pages applies these automatically:

- Strict Content-Security-Policy: everything from this site only, plus frames from `www.youtube-nocookie.com`. No inline scripts or styles, no third-party trackers, fonts self-hosted.
- HSTS, `nosniff`, strict referrer policy, permissions policy (camera/mic/location off), `frame-ancestors 'none'`.

If you add analytics, a form embed or another third party, update the CSP or it will be blocked. Check the browser console after deploying.

## Accessibility

- Typed headline is announced in full to screen readers (`aria-label`); visitors with "reduce motion" set get the static headline, no scrolling strips and no blinking cursor.
- Strips pause on hover/focus and have a pause button.
- Photo viewer: keyboard arrows, Escape to close, focus kept inside the dialog and returned afterwards.
- All photos have captions used as alt text.

## Photo credits and consent

- Stock photos are from **Pexels** and **Pixabay** (free licences). Some show brands (e.g. arcade games, consoles). Fine in the gallery, but avoid them on posters or as the main hero image.
- BCS event photos: audience faces have been blurred. If anyone asks for a photo to be removed, delete it from `tools/photos.json` and `assets/img/gallery/`, then rebuild.
- 3D printing photos: QR code blurred.
- Fonts: Barlow and JetBrains Mono, SIL Open Font License 1.1 (see `assets/fonts/`).

## Caching

`_headers` tells browsers to cache everything in `/assets/` for a week. `tools/build.py` adds a version (`?v=…`) to the CSS and JavaScript links, worked out from each file's contents, so visitors get new styles as soon as you deploy. **Always run `python3 tools/build.py` after editing CSS or JS.** New or changed images should get a new file name.
