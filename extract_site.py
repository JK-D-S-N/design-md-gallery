#!/usr/bin/env python3
"""URL -> structured, observable facts for authoring a DESIGN.md.
Uses headless Chrome only (no untrusted deps). Reads the RENDERED DOM (so it
includes JS-rendered content and the footer), pulls colours/fonts from inline
styles + <style> + linked CSS, and saves screenshots for the gestalt pass.

Usage: python3 extract_site.py <url> <slug>
Outputs: /tmp/extract/<slug>/dom.html, shot.png, full.png, facts.txt
"""
import sys, os, re, subprocess, urllib.parse, urllib.request, collections, html

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
url=sys.argv[1]; slug=sys.argv[2] if len(sys.argv)>2 else "site"
out=f"/tmp/extract/{slug}"; os.makedirs(out, exist_ok=True)

def chrome(*args):
    subprocess.run([CHROME,"--headless","--disable-gpu","--hide-scrollbars",
        "--virtual-time-budget=8000",*args], capture_output=True, timeout=90)

# 1. rendered DOM
dom=subprocess.run([CHROME,"--headless","--disable-gpu","--virtual-time-budget=9000","--dump-dom",url],
    capture_output=True, text=True, timeout=90).stdout
open(f"{out}/dom.html","w").write(dom)
# 2. screenshots
chrome("--window-size=1440,900",f"--screenshot={out}/shot.png",url)
chrome("--window-size=1440,5200",f"--screenshot={out}/full.png",url)

def textof(tag, src):
    # crude: pull visible text inside the first <tag>...</tag>
    m=re.search(rf'<{tag}[^>]*>(.*?)</{tag}>', src, re.S|re.I)
    if not m: return []
    inner=m.group(1)
    parts=[html.unescape(re.sub('<[^>]+>','',p)).strip() for p in re.split(r'<[^>]+>', inner)]
    return [p for p in [t.strip() for t in parts] if 1<len(p)<40][:18]

# colours from DOM (inline + <style>) and linked CSS
css=dom
for href in re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)', dom)[:4]:
    full=urllib.parse.urljoin(url, href)
    try:
        css+=urllib.request.urlopen(urllib.request.Request(full,headers={'User-Agent':'Mozilla/5.0'}),timeout=15).read().decode('utf-8','ignore')
    except Exception: pass

hexes=collections.Counter(re.findall(r'#[0-9a-fA-F]{6}\b', css))
fonts=collections.Counter(re.findall(r'font-family:\s*([^;}{"\n]+)', css))
radii=collections.Counter(re.findall(r'border-radius:\s*([0-9.]+(?:px|rem|em)|9999px|999px|50%)', css))

# text content
h1=re.findall(r'<h1[^>]*>(.*?)</h1>', dom, re.S|re.I)
h1=[html.unescape(re.sub('<[^>]+>','',h)).strip() for h in h1][:3]
buttons=re.findall(r'<(?:button|a)[^>]*class="[^"]*(?:btn|button|cta)[^"]*"[^>]*>(.*?)</(?:button|a)>', dom, re.S|re.I)
buttons=[html.unescape(re.sub('<[^>]+>','',b)).strip() for b in buttons]
buttons=[b for b in buttons if 0<len(b)<30][:10]

with open(f"{out}/facts.txt","w") as f:
    f.write(f"URL: {url}\nSLUG: {slug}\n\n")
    f.write("== TOP COLOURS (hex, by frequency) ==\n")
    for c,n in hexes.most_common(22): f.write(f"  {c}  x{n}\n")
    f.write("\n== FONT FAMILIES ==\n")
    for c,n in fonts.most_common(10): f.write(f"  {c.strip()[:70]}  x{n}\n")
    f.write("\n== BORDER RADII ==\n")
    for c,n in radii.most_common(8): f.write(f"  {c}  x{n}\n")
    f.write("\n== H1 / headlines ==\n"); [f.write(f"  {t}\n") for t in h1]
    f.write("\n== NAV text ==\n"); [f.write(f"  {t}\n") for t in (textof('nav',dom) or textof('header',dom))]
    f.write("\n== FOOTER text ==\n"); [f.write(f"  {t}\n") for t in textof('footer',dom)]
    f.write("\n== BUTTON / CTA labels ==\n"); [f.write(f"  {t}\n") for t in buttons]

print(open(f"{out}/facts.txt").read())
print(f"\n[shots: {out}/shot.png , {out}/full.png ; dom: {out}/dom.html]")
