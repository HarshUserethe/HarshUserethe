"""Generates light/dark glassmorphism SVG assets for the GitHub profile README.
Run:  python3 generate_assets.py   (needs icons.json from dump.mjs)
"""
import json, html

ICONS = json.load(open("icons.json"))
FONT = "Inter, 'SF Pro Display', 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"

THEMES = {
  "light": dict(
    text="#1F2328", muted="#57606A", accent="#5B3FD0", accent2="#0A6CA8",
    bg1="#F6F3FF", bg2="#EAF4FF", blob1="#8B6CFF", blob2="#3BB6F0", blob_op=.32,
    glass_top="#FFFFFF", glass_top_op=.78, glass_bot="#FFFFFF", glass_bot_op=.42,
    glass_stroke="#FFFFFF", glass_stroke_op=.95, edge="#5B3FD0", edge_op=.20,
    shadow="#3B2A8C", shadow_op=.12, icon_min_lum=None, icon_max_lum=.55),
  "dark": dict(
    text="#F0F6FC", muted="#B4BFCC", accent="#B6A4FF", accent2="#7CC7FF",
    bg1="#0D1117", bg2="#141A2B", blob1="#7C5CFF", blob2="#1FA8E8", blob_op=.38,
    glass_top="#FFFFFF", glass_top_op=.16, glass_bot="#FFFFFF", glass_bot_op=.05,
    glass_stroke="#FFFFFF", glass_stroke_op=.28, edge="#FFFFFF", edge_op=.10,
    shadow="#000000", shadow_op=.35, icon_min_lum=.35, icon_max_lum=None),
}

def lum(hexc):
    r,g,b=[int(hexc[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c: c/12.92 if c<=.03928 else ((c+.055)/1.055)**2.4
    return .2126*f(r)+.7152*f(g)+.0722*f(b)

def mix(hexc, target, t):
    a=[int(hexc[i:i+2],16) for i in (0,2,4)]; b=[int(target[i:i+2],16) for i in (0,2,4)]
    return "".join(f"{round(x+(y-x)*t):02x}" for x,y in zip(a,b))

def icon_color(hexc, th):
    c=hexc
    if th["icon_min_lum"] is not None:           # dark mode: lift too-dark brand colours
        t=0
        while lum(c)<th["icon_min_lum"] and t<1:
            t+=.1; c=mix(hexc,"FFFFFF",t)
    if th["icon_max_lum"] is not None:           # light mode: deepen too-light brand colours
        t=0
        while lum(c)>th["icon_max_lum"] and t<1:
            t+=.1; c=mix(hexc,"000000",t)
    return "#"+c

def glyph(key, x, y, size, th, fallback_letter="•", fallback_hex="888888"):
    """Brand icon from simple-icons, else a rounded letter tile."""
    if key in ICONS:
        d=ICONS[key]; col=icon_color(d["hex"],th); s=size/24
        return f'<path transform="translate({x} {y}) scale({s})" d="{d["path"]}" fill="{col}"/>'
    col=icon_color(fallback_hex,th)
    return (f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="4" fill="{col}" fill-opacity=".18" stroke="{col}" stroke-opacity=".6"/>'
            f'<text x="{x+size/2}" y="{y+size*.73}" text-anchor="middle" font-family="{FONT}" font-size="{size*.62}" font-weight="700" fill="{col}">{fallback_letter}</text>')

def defs(th, uid):
    return f'''<defs>
  <linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{th['bg1']}"/><stop offset="1" stop-color="{th['bg2']}"/></linearGradient>
  <linearGradient id="glass{uid}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{th['glass_top']}" stop-opacity="{th['glass_top_op']}"/>
    <stop offset="1" stop-color="{th['glass_bot']}" stop-opacity="{th['glass_bot_op']}"/></linearGradient>
  <linearGradient id="rim{uid}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{th['glass_stroke']}" stop-opacity="{th['glass_stroke_op']}"/>
    <stop offset="1" stop-color="{th['edge']}" stop-opacity="{th['edge_op']}"/></linearGradient>
  <filter id="blur{uid}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="46"/></filter>
  <filter id="sh{uid}" x="-20%" y="-30%" width="140%" height="190%"><feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="{th['shadow']}" flood-opacity="{th['shadow_op']}"/></filter>
</defs>'''

def blobs(th, uid, w, h):
    return (f'<g filter="url(#blur{uid})" opacity="{th["blob_op"]}">'
            f'<circle cx="{w*.12}" cy="{h*.2}" r="{min(w,h)*.30}" fill="{th["blob1"]}"/>'
            f'<circle cx="{w*.88}" cy="{h*.85}" r="{min(w,h)*.32}" fill="{th["blob2"]}"/></g>')

def glass_rect(x,y,w,h,r,uid):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#glass{uid})" filter="url(#sh{uid})"/>'
            f'<rect x="{x+.5}" y="{y+.5}" width="{w-1}" height="{h-1}" rx="{r}" fill="none" stroke="url(#rim{uid})" stroke-width="1.2"/>')

def svg(w,h,body,title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(title)}">'
            f'<title>{html.escape(title)}</title>{body}</svg>')

# ───────────────────────── Hero ─────────────────────────
def hero(name):
    th=THEMES[name]; W,H=1000,280; u="h"
    b=defs(th,u)+f'<rect width="{W}" height="{H}" rx="28" fill="url(#bg{u})"/>'+blobs(th,u,W,H)
    b+=glass_rect(24,24,W-48,H-48,22,u)
    b+=f'<text x="64" y="96" font-family="{FONT}" font-size="17" font-weight="500" fill="{th["muted"]}">Hi, I’m</text>'
    b+=f'<text x="62" y="156" font-family="{FONT}" font-size="58" font-weight="800" letter-spacing="-1.5" fill="{th["text"]}">Harsh Userethe</text>'
    b+=f'<text x="64" y="198" font-family="{FONT}" font-size="22" font-weight="600" fill="{th["accent"]}">Software Engineer</text>'
    b+=f'<text x="64" y="232" font-family="{FONT}" font-size="16" font-weight="400" fill="{th["muted"]}">Node.js · React · Next.js · AWS · Bhopal, India</text>'
    # decorative code-bracket mark on the right
    b+=(f'<g transform="translate(790 88)" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="10">'
        f'<path d="M44 20 L8 56 L44 92" stroke="{th["accent"]}"/><path d="M96 20 L132 56 L96 92" stroke="{th["accent2"]}"/>'
        f'<path d="M80 6 L60 106" stroke="{th["text"]}" stroke-opacity=".75"/></g>')
    return svg(W,H,b,"Harsh Userethe — Software Engineer")

# ───────────────────────── Footer ─────────────────────────
def footer(name):
    th=THEMES[name]; W,H=1000,110; u="f"
    b=defs(th,u)+f'<rect width="{W}" height="{H}" rx="24" fill="url(#bg{u})"/>'+blobs(th,u,W,H)
    b+=glass_rect(20,20,W-40,H-40,18,u)
    b+=f'<text x="{W/2}" y="62" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="600" fill="{th["text"]}">Thanks for stopping by.</text>'
    b+=f'<text x="{W/2}" y="84" text-anchor="middle" font-family="{FONT}" font-size="14" fill="{th["muted"]}">Open to cloud and backend-heavy product engineering roles.</text>'
    return svg(W,H,b,"Footer")

# ───────────────────────── Social pills ─────────────────────────
SOCIAL=[("linkedin","LinkedIn","LinkedIn","L","0A66C2"),("github","GitHub","GitHub","G","FFFFFF"),
        ("x","X","X","X","000000"),("instagram","Instagram","Instagram","I","E4405F"),("email","Email","Gmail","M","EA4335")]
def social(name,slug,label,key,letter,hexc):
    th=THEMES[name]; w=int(54+len(label)*8.6+16); H=48; u="s"
    b=defs(th,u)+glass_rect(4,2,w-8,H-8,20,u)
    b+=glyph(key,24,13,20,th,letter,hexc)
    b+=f'<text x="54" y="29.5" font-family="{FONT}" font-size="14" font-weight="600" fill="{th["text"]}">{label}</text>'
    return svg(w,H,b,label)

# ───────────────────────── Skills panel ─────────────────────────
SKILLS=[
 ("Languages",[("JavaScript (ES6+)","JavaScript","J","F7DF1E"),("TypeScript","TypeScript","T","3178C6"),("Python (basics)","Python","P","3776AB"),
               ("SQL",None,"S","0EA5E9"),("HTML5","HTML5","H","E34F26"),("CSS3","CSS3","C","1572B6")]),
 ("Frontend",[("React","React","R","61DAFB"),("Next.js","Next","N","FFFFFF"),("Redux","Redux","R","764ABC"),
              ("Zustand","Zustand","Z","D97706"),("TanStack Query","TanStack","T","FF4154"),("Tailwind CSS","Tailwind","T","06B6D4")]),
 ("Backend",[("Node.js","Node","N","5FA04E"),("Express.js","Express","E","FFFFFF"),("REST APIs",None,"R","10B981"),
             ("JWT","JWT","J","D63AFF"),("OAuth","OAuth","O","EB5424"),("Mongoose","Mongoose","M","880000"),("Jest","Jest","J","C21325")]),
 ("Databases",[("PostgreSQL","PostgreSQL","P","4169E1"),("MySQL","MySQL","M","4479A1"),("MongoDB","MongoDB","M","47A248")]),
 ("Cloud & DevOps",[("AWS","AWS","A","FF9900"),("Docker","Docker","D","2496ED"),("Git","Git","G","F05032"),
                    ("GitHub","GitHub","G","FFFFFF"),("CI/CD","CICD","C","2088FF")]),
 ("Monitoring & Tools",[("Datadog","Datadog","D","632CA6"),("Postman","Postman","P","FF6C37"),("Power BI","PowerBI","P","F2C811"),
                        ("Jira","Jira","J","0052CC"),("Figma","Figma","F","F24E1E")]),
]
def db_icon(x,y,s,col):
    k=s/24
    return (f'<g transform="translate({x} {y}) scale({k})" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round">'
            f'<ellipse cx="12" cy="5.5" rx="8" ry="3"/><path d="M4 5.5v6.5c0 1.7 3.6 3 8 3s8-1.3 8-3V5.5M4 12v6.5c0 1.7 3.6 3 8 3s8-1.3 8-3V12"/></g>')
def api_icon(x,y,s,col):
    k=s/24
    return (f'<g transform="translate({x} {y}) scale({k})" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="M8 6l-6 6 6 6M16 6l6 6-6 6"/><path d="M13.5 4l-3 16"/></g>')

def skills(name):
    th=THEMES[name]; W=940; u="k"; PAD=28; LABEL_W=205; ROW_X=PAD+LABEL_W; AVAIL=W-PAD-ROW_X
    CH=38; GAP=10; ROWGAP=22
    y=PAD+6; chips=[]; labels=[]; sep=[]
    for ci,(cat,items) in enumerate(SKILLS):
        labels.append(f'<text x="{PAD+4}" y="{y+CH/2+5}" font-family="{FONT}" font-size="16" font-weight="700" fill="{th["text"]}">{html.escape(cat)}</text>')
        x=ROW_X; top=y
        for (label,key,letter,hexc) in items:
            cw=int(14+20+9+len(label)*8.4+20)
            if x+cw>ROW_X+AVAIL: x=ROW_X; y+=CH+GAP
            chips.append(glass_rect(x,y,cw,CH,14,u))
            ic=icon_color(hexc,th)
            if key is None:
                chips.append(db_icon(x+14,y+9,20,ic) if label=="SQL" else api_icon(x+14,y+9,20,ic))
            else:
                chips.append(glyph(key,x+14,y+9,20,th,letter,hexc))
            chips.append(f'<text x="{x+43}" y="{y+CH/2+4.8}" font-family="{FONT}" font-size="14" font-weight="600" fill="{th["text"]}">{html.escape(label)}</text>')
            x+=cw+GAP
        y+=CH+ROWGAP
        if ci<len(SKILLS)-1:
            sep.append(f'<line x1="{PAD}" x2="{W-PAD}" y1="{y-ROWGAP/2-1}" y2="{y-ROWGAP/2-1}" stroke="{th["muted"]}" stroke-opacity=".22"/>')
    H=int(y-ROWGAP+PAD+4)
    b=defs(th,u)+f'<rect width="{W}" height="{H}" rx="26" fill="url(#bg{u})"/>'+blobs(th,u,W,H)
    b+=f'<rect x="10" y="10" width="{W-20}" height="{H-20}" rx="20" fill="{th["glass_top"]}" fill-opacity="{.30 if name=="light" else .04}" stroke="url(#rim{u})"/>'
    b+="".join(sep)+"".join(labels)+"".join(chips)
    return svg(W,H,b,"Skills and tools")

# ───────────────────────── write ─────────────────────────
for n in THEMES:
    open(f"assets/hero-{n}.svg","w").write(hero(n))
    open(f"assets/footer-{n}.svg","w").write(footer(n))
    open(f"assets/skills-{n}.svg","w").write(skills(n))
    for slug,label,key,letter,hexc in SOCIAL:
        open(f"assets/social-{slug}-{n}.svg","w").write(social(n,slug,label,key,letter,hexc))
print("done")
