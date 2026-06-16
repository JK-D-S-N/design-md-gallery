import os, re, json, glob

ROOT = os.path.dirname(os.path.abspath(__file__))

def prettify(slug):
    s = slug.replace('.app','').replace('.ai','').replace('-',' ').replace('.',' ')
    fixes = {'runwayml':'Runway ML','clickhouse':'ClickHouse','hashicorp':'HashiCorp',
        'openai':'OpenAI','hp':'HP','ibm':'IBM','minimax':'MiniMax','theverge':'The Verge',
        'bmw':'BMW','bmw-m':'BMW M','cal':'Cal.com','linear.app':'Linear','mistral.ai':'Mistral AI',
        'together.ai':'Together AI','opencode.ai':'OpenCode','x.ai':'xAI','posthog':'PostHog',
        'elevenlabs':'ElevenLabs','playstation':'PlayStation','dell-1996':'Dell (1996)',
        'nintendo-2001':'Nintendo (2001)','nvidia':'NVIDIA','spacex':'SpaceX','voltagent':'VoltAgent',
        'sap':'SAP','gitlab':'GitLab','mcdonalds':"McDonald's",'oneplus':'OnePlus','asus':'ASUS',
        'crowdstrike':'CrowdStrike','aiven':'Aiven','confluent':'Confluent','kaggle':'Kaggle'}
    return fixes.get(slug, ' '.join(w.capitalize() for w in s.split()))

def lum(h):
    h=h.lstrip('#')
    if len(h)==3: h=''.join(c*2 for c in h)
    if len(h)<6: return 128
    r,g,b=int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    return 0.299*r+0.587*g+0.114*b

def sat(h):
    h=h.lstrip('#')
    if len(h)==3: h=''.join(c*2 for c in h)
    if len(h)<6: return 0
    r,g,b=[int(h[i:i+2],16) for i in (0,2,4)]
    return max(r,g,b)-min(r,g,b)

HEX=re.compile(r'#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b')

def _lin(c):
    c=c/255
    return c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
def rel_lum(h):
    h=h.lstrip('#')
    if len(h)==3: h=''.join(x*2 for x in h)
    if len(h)<6: return .5
    r,g,b=[int(h[i:i+2],16) for i in (0,2,4)]
    return 0.2126*_lin(r)+0.7152*_lin(g)+0.0722*_lin(b)
def contrast(a,b):
    la,lb=rel_lum(a),rel_lum(b)
    return (max(la,lb)+.05)/(min(la,lb)+.05)
def fix_ink(ink,bg):
    if not ink.startswith('#'): return ink
    if contrast(ink,bg) >= 4.5: return ink
    return '#0a0a0c' if rel_lum(bg) > 0.4 else '#ffffff'

def btn_radius(text):
    for ln in text.splitlines():
        if 'button' in ln.lower():
            if 'pill' in ln.lower() or '999' in ln: return '999px'
            mm=re.search(r'(\d+)\s*px', ln)
            if mm: return f'{max(2,min(16,int(mm.group(1))))}px'
    low=text.lower()
    if 'pill' in low or '999px' in low or 'rounded-full' in low: return '999px'
    return '8px'

def display_type(text):
    m=re.search(r'display-(?:xl|lg|xxl):\s*\n(.*?)(?=\n\s{2}\w|\n\S)', text, re.S)
    blk=m.group(1) if m else ''
    w=re.search(r'fontWeight:\s*(\d+)', blk)
    ls=re.search(r'letterSpacing:\s*(-?[\d.]+)px', blk)
    return (w.group(1) if w else '600'), (ls.group(1)+'px' if ls else '-0.02em')

# ---------- format A: YAML frontmatter with a colors: block ----------
def parse_yaml(text):
    m=re.search(r'^---\s*\n(.*?)\n---', text, re.S)
    if not m: return None
    block=m.group(1)
    cm=re.search(r'^colors:\s*\n(.*?)(?=^\S)', block+"\nZZZ:", re.S|re.M)
    if not cm: return None
    colors={}
    for ln in cm.group(1).splitlines():
        mm=re.match(r'\s+([a-z0-9-]+):\s*"?(#[0-9a-fA-F]{3,8})"?', ln)
        if mm: colors[mm.group(1)]=mm.group(2)
    if not colors: return None
    desc=re.search(r'^description:\s*(.+)$', block, re.M)
    ff=re.search(r'fontFamily:\s*"?([^"\n]+)"?', block)
    return {
        'colors':colors,
        'description':(desc.group(1).strip().strip('"').strip("'") if desc else ''),
        'displayFont':(ff.group(1).strip() if ff else 'system-ui'),
        'bg':colors.get('canvas') or colors.get('canvas-soft') or colors.get('surface-soft') or '',
        'ink':colors.get('ink') or colors.get('body-strong') or '',
        'accent':colors.get('primary') or colors.get('accent') or '',
        'hairline':colors.get('hairline') or colors.get('hairline-soft') or '',
        'swatches':[v for v in colors.values()][:6],
    }

# ---------- format B: prose with Token | Hex | Role tables ----------
def parse_prose(text):
    pairs=[]
    for ln in text.splitlines():
        if ln.count('|')>=2 and HEX.search(ln):
            hx=HEX.search(ln).group(0)
            cells=[c.strip(' `') for c in ln.split('|')]
            role=cells[-1].lower() if cells else ''
            if 'hex' in role: continue
            pairs.append((hx, role))
    if not pairs: return None
    def pick(keys, exclude=()):
        for hx,role in pairs:
            if hx in exclude: continue
            if any(k in role for k in keys): return hx
        return ''
    bg = pick(['canvas','main background','page background','base background']) or pick(['background']) \
         or max((p[0] for p in pairs), key=lum)
    ink = pick(['body text','primary text','default text','text and','heading']) or pick(['text']) \
          or min((p[0] for p in pairs), key=lum)
    accent = pick(['signature','brand background','brand core','primary cta','cta','accent','interactive','primary action','link'], exclude=(bg,ink))
    if not accent:
        cand=[p[0] for p in pairs if p[0] not in (bg,ink) and sat(p[0])>40]
        accent=cand[0] if cand else pairs[0][0]
    bq=re.search(r'^>\s*(.+)$', text, re.M)
    seen=[]
    for hx,_ in pairs:
        if hx not in seen: seen.append(hx)
    return {
        'colors':{f'c{i}':hx for i,hx in enumerate(seen)},
        'description':(bq.group(1).strip() if bq else ''),
        'displayFont':'system-ui',
        'bg':bg,'ink':ink,'accent':accent,'hairline':'',
        'swatches':seen[:6],
    }

# ---------- objective completeness metric, computed from the DESIGN.md ----------
def raw_metrics(text):
    low=text.lower()
    hexes=len(set(HEX.findall(text)))
    sections=len(re.findall(r'^#{2,3}\s', text, re.M))
    words=len(text.split())
    feats=sum(k in low for k in ['typograph','font','component','guardrail',"don't",'responsive','breakpoint','spacing','radius','shadow','motion','accessib'])
    return {'hexes':hexes,'sections':sections,'words':words,'feats':feats}

entries=[]
for d in sorted(glob.glob(os.path.join(ROOT,'design-md','*'))):
    md=os.path.join(d,'DESIGN.md')
    if not os.path.isfile(md): continue
    slug=os.path.basename(d)
    text=open(md,encoding='utf-8').read()
    parsed=parse_yaml(text) or parse_prose(text)
    if not parsed: continue
    bg=parsed['bg'] or '#0e0e10'
    ink=parsed['ink'] or ('#111' if lum(bg)>150 else '#f4f4f5')
    ink=fix_ink(ink,bg)
    accent=parsed['accent'] or '#888'
    dw,dt=display_type(text)
    entries.append({
        'slug':slug, 'name':prettify(slug),
        'description':parsed['description'][:240],
        'colors':parsed['colors'],
        'displayFont':parsed['displayFont'],
        'displayWeight':dw, 'displayTracking':dt,
        'btnRadius':btn_radius(text),
        'bg':bg, 'ink':ink,
        'accent':accent,
        'muted':parsed['colors'].get('muted','') or '',
        'hairline':parsed['hairline'] or ('rgba(0,0,0,.14)' if lum(bg)>150 else 'rgba(255,255,255,.16)'),
        'swatches':[s for s in parsed['swatches'] if s][:6],
        '_m':raw_metrics(text),
    })

# normalise each metric across the corpus, weight, → 0-100 score + 1-5 stars
def norm(vals):
    lo,hi=min(vals),max(vals)
    return (lambda v: 0.0 if hi==lo else (v-lo)/(hi-lo))
W={'hexes':.30,'sections':.30,'words':.20,'feats':.20}
norms={k:norm([e['_m'][k] for e in entries]) for k in W}
for e in entries:
    score=sum(W[k]*norms[k](e['_m'][k]) for k in W)*100
    e['score']=round(score)
    e['stars']=max(1,min(5,round(score/20*2)/2))   # 1–5, half-steps
    del e['_m']

json.dump(entries, open(os.path.join(ROOT,'data.json'),'w'), indent=1)
nopal=sum(1 for e in entries if not e['swatches'])
top=sorted(entries,key=lambda e:-e['score'])[:5]
print(f"wrote data.json — {len(entries)} systems; {nopal} with no palette")
print("top by completeness:", ", ".join(f"{e['name']} {e['score']}" for e in top))
for s in ('klarna','discord','amazon','apple','claude','mcdonalds'):
    e=next((x for x in entries if x['slug']==s),None)
    if e: print(' ',s,'| bg',e['bg'],'| accent',e['accent'],'| sw',len(e['swatches']),'|',e['description'][:38])
