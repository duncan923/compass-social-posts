import os, sys, html, asyncio, importlib.util
from pathlib import Path
# Paths come from env vars so the same script runs anywhere.
# CS_WEEK: folder holding posts.py (output goes to CS_WEEK/out)
# CS_DS: design system project folder (assets/, fonts/IvarSoft-Medium.otf)
# CS_FONTS: folder with fontsource-instrument-sans-5.1.0 and fontsource-cormorant-garamond-5.1.0
# CS_PHOTOS: folder with per-property photo subfolders (relative photo keys resolve here)
WEEK = Path(os.environ['CS_WEEK'])
DS = Path(os.environ['CS_DS'])
PH = Path(os.environ.get('CS_PHOTOS', WEEK/'photos'))
FONTS = Path(os.environ['CS_FONTS'])
OUT = WEEK/'out'; OUT.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('posts', WEEK/'posts.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

IS = FONTS/'fontsource-instrument-sans-5.1.0'/'files'
CG = FONTS/'fontsource-cormorant-garamond-5.1.0'/'files'
CSS = f"""
@font-face{{font-family:'Ivar Soft';src:url('file://{DS}/fonts/IvarSoft-Medium.otf');font-weight:400 700}}
@font-face{{font-family:'Instrument Sans';src:url('file://{IS}/instrument-sans-latin-400-normal.woff2');font-weight:400}}
@font-face{{font-family:'Instrument Sans';src:url('file://{IS}/instrument-sans-latin-600-normal.woff2');font-weight:600}}
@font-face{{font-family:'Instrument Sans';src:url('file://{IS}/instrument-sans-latin-700-normal.woff2');font-weight:700}}
@font-face{{font-family:'Cormorant Garamond';src:url('file://{CG}/cormorant-garamond-latin-600-italic.woff2');font-weight:600;font-style:italic}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{font-family:'Instrument Sans',Arial,sans-serif}}
section{{position:relative;width:1080px;height:1350px;overflow:hidden;background:#252A3A}}
.serif{{font-family:'Ivar Soft','Cormorant Garamond',Georgia,serif;font-weight:600}}
"""
LOGO_W = f"file://{DS}/assets/logo-white.png"; LOGO_N = f"file://{DS}/assets/logo-navy.png"
RAYS = f"file://{DS}/assets/bg-rays-navy.png"; SYM = f"file://{DS}/assets/symbol-gold.png"
e = html.escape

def photo(p, h=810):
    if p and p.startswith('/'):
        return f'<img src="file://{p}" style="position:absolute;top:0;left:0;width:1080px;height:{h}px;object-fit:cover">'
    if p and 'PLACEHOLDER' not in p and (PH/p).exists():
        return f'<img src="file://{PH/p}" style="position:absolute;top:0;left:0;width:1080px;height:{h}px;object-fit:cover">'
    return f'<div style="position:absolute;top:0;left:0;width:1080px;height:{h}px;background:#4A5168;display:flex;align-items:center;justify-content:center;color:#E0B940;font-weight:700;font-size:40px;letter-spacing:.12em">PHOTO NEEDED</div>'

FADE = '<div style="position:absolute;top:690px;left:0;right:0;height:120px;background:linear-gradient(180deg,rgba(37,42,58,0),#252A3A)"></div>'
def badge(t): return f'<div style="position:absolute;top:64px;left:64px;background:rgba(37,42,58,.9);border-left:4px solid #E0B940;border-radius:3px;color:#fff;font-weight:600;font-size:24px;letter-spacing:.12em;padding:14px 20px">{e(t)}</div>' if t else ''
def eyebrow(t, col='#E0B940'): return f'<div style="display:flex;align-items:center;gap:16px"><div style="width:48px;height:2px;background:#E0B940"></div><div style="color:{col};font-weight:600;font-size:22px;letter-spacing:.12em">{e(t)}</div></div>'
SELLER_FOOT = f'<div style="position:absolute;left:64px;right:64px;bottom:64px;display:flex;justify-content:space-between;align-items:flex-end"><div style="font-size:22px;line-height:1.4;color:rgba(255,255,255,.8)">Selling? See what yours is worth at<br><span style="color:#E0B940">duncanure.co.uk/valuation</span></div><img src="{LOGO_W}" style="height:70px"></div>'

def t1(p):
    hl = p['headline']; fs = 78 if len(hl) <= 26 else 64
    spec = ''.join(f'<div style="flex:1;{"padding-right:24px" if i==0 else "padding:0 24px;border-left:1px solid rgba(224,185,64,.6)"}"><div class="serif" style="font-size:48px;line-height:1;color:#fff">{e(a)}</div><div style="font-weight:600;font-size:16px;letter-spacing:.12em;color:rgba(255,255,255,.7);margin-top:10px">{e(b)}</div></div>' for i,(a,b) in enumerate(p['spec']))
    cgi = '<div style="position:absolute;top:64px;right:64px;background:rgba(37,42,58,.85);color:#fff;font-size:20px;padding:10px 16px;border-radius:3px">CGI of the planned kitchen</div>' if p.get('cgi') else ''
    return f'''{photo(p['photo'])}{FADE}{badge(p.get('badge'))}{cgi}
<div style="position:absolute;top:795px;left:64px;right:64px">{eyebrow(p["town"])}<div class="serif" style="font-size:{fs}px;line-height:1.05;color:#fff;margin-top:16px">{e(hl)}</div></div>
<div style="position:absolute;top:990px;left:64px;right:64px;display:flex">{spec}</div>
<div style="position:absolute;top:1105px;left:64px"><div style="font-weight:600;font-size:18px;letter-spacing:.12em;color:rgba(255,255,255,.7)">OFFERS OVER</div><div class="serif" style="font-size:72px;line-height:1.05;color:#E0B940">{e(p['price'])}</div></div>
<div style="position:absolute;right:64px;top:1125px;background:#E0B940;color:#363C52;border-radius:3px;font-weight:700;font-size:20px;letter-spacing:.06em;padding:20px 26px">DM ME TO BOOK A VIEWING</div>
{SELLER_FOOT}'''

def t5(p):
    return f'''{photo(p['photo'])}{FADE}{badge(p.get('badge'))}
<div style="position:absolute;top:830px;left:64px;right:64px">{eyebrow(p['town'])}<div class="serif" style="font-size:78px;line-height:1.05;color:#fff;margin-top:18px">{e(p['headline'])}</div><div style="font-weight:600;font-size:44px;line-height:1.25;color:#fff;margin-top:26px">{p['result_html']}</div></div>
<div style="position:absolute;left:64px;right:64px;top:1180px;height:1px;background:rgba(255,255,255,.14)"></div>
<div style="position:absolute;left:64px;bottom:64px;font-size:22px;line-height:1.4;color:rgba(255,255,255,.8)">Thinking of selling?<br><span style="color:#E0B940">duncanure.co.uk/valuation</span></div><img src="{LOGO_W}" style="position:absolute;right:64px;bottom:64px;height:70px">'''

def cta(p):
    return f'''<div style="position:absolute;inset:0;background:url({RAYS}) center/150% no-repeat;opacity:.4"></div><img src="{SYM}" style="position:absolute;top:72px;left:64px;width:72px;height:72px;object-fit:contain">
<div style="position:absolute;top:300px;left:64px;right:64px">{eyebrow(p['eyebrow'])}<div class="serif" style="font-size:80px;line-height:1.06;color:#fff;margin-top:22px">{e(p['headline'])}</div><p style="font-size:26px;line-height:1.55;color:rgba(255,255,255,.78);margin-top:28px">{e(p['sub'])}</p></div>
<div style="position:absolute;left:64px;right:64px;bottom:64px;border-top:1px solid rgba(255,255,255,.14);padding-top:30px"><div style="font-weight:600;font-size:20px;letter-spacing:.12em;color:#E0B940">BOOK YOUR FREE VALUATION</div><div class="serif" style="font-size:52px;color:#E0B940;margin-top:8px">duncanure.co.uk/valuation</div></div><img src="{LOGO_W}" style="position:absolute;right:64px;bottom:64px;height:70px">'''

def review(p):
    return f'''<div style="position:absolute;inset:0;background:url({RAYS}) center/150% no-repeat;opacity:.4"></div><img src="{SYM}" style="position:absolute;top:72px;left:64px;width:72px;height:72px;object-fit:contain">
<div style="position:absolute;top:250px;left:64px;right:64px">{eyebrow(p['stars'])}<div class="serif" style="font-size:240px;line-height:.8;color:rgba(224,185,64,.35);margin-top:30px">&ldquo;</div><div style="font-family:'Cormorant Garamond',Georgia,serif;font-style:italic;font-weight:600;font-size:66px;line-height:1.15;color:#fff;margin-top:-40px">{e(p['quote'])}</div><div style="font-weight:600;font-size:28px;color:#fff;margin-top:40px">{e(p['who'])}</div></div>
<div style="position:absolute;left:64px;bottom:64px;font-size:22px;line-height:1.4;color:rgba(255,255,255,.8)">Thinking of selling?<br><span style="color:#E0B940">duncanure.co.uk/valuation</span></div><img src="{LOGO_W}" style="position:absolute;right:64px;bottom:64px;height:70px">'''

def stat(p):
    cards = ''.join(f'<div style="flex:1;background:#363C52;border-radius:6px;padding:30px"><div class="serif" style="font-size:84px;line-height:1;color:#E0B940">{e(a)}</div><div style="font-weight:600;font-size:26px;color:#fff;margin-top:16px">{e(b)}</div></div>' for a,b in p['stats'])
    return f'''<div style="position:absolute;inset:0;background:#F2F3F0"></div><div style="position:absolute;top:80px;left:64px;right:64px">{eyebrow(p['eyebrow'],'#363C52')}<div style="display:flex;gap:24px;margin-top:30px">{cards}</div></div>
<img src="file://{PH/p['photo']}" style="position:absolute;top:470px;left:0;width:1080px;height:880px;object-fit:cover"><div style="position:absolute;top:880px;left:0;right:0;bottom:0;background:linear-gradient(180deg,rgba(37,42,58,0),rgba(37,42,58,.9))"></div>
<div class="serif" style="position:absolute;left:64px;bottom:170px;font-size:62px;line-height:1.08;color:#fff">{e(p['closing'])}</div>
<div style="position:absolute;left:64px;bottom:64px;font-size:22px;color:rgba(255,255,255,.85)">Book a free valuation at <span style="color:#E0B940">duncanure.co.uk/valuation</span></div><img src="{LOGO_W}" style="position:absolute;right:64px;bottom:64px;height:70px">'''


SP2 = Path(os.environ.get('CS_STOCK', PH/'_stock'))  # generic seller photos
def sphoto(name, pos='center'):
    return f'<img src="file://{SP2/name}" style="position:absolute;top:0;left:0;width:1080px;height:760px;object-fit:cover;object-position:{pos}"><div style="position:absolute;top:620px;left:0;right:0;height:140px;background:linear-gradient(180deg,rgba(37,42,58,0),#252A3A)"></div>'
def seller(p):
    cols = ''.join(f'<div style="flex:1;min-width:0;{"padding-right:22px" if i==0 else "padding:0 22px;border-left:1px solid rgba(224,185,64,.6)"}"><div class="serif" style="font-size:{p.get("strip_fs",46)}px;line-height:1.05;color:#E0B940">{e(a)}</div><div style="font-size:19px;line-height:1.35;color:rgba(255,255,255,.82);margin-top:10px">{e(b)}</div></div>' for i,(a,b) in enumerate(p['strip']))
    return f'''{sphoto(p['sphoto'], p.get('pos','center'))}
<div style="position:absolute;top:735px;left:64px;right:64px">{eyebrow(p['eyebrow'])}<div class="serif" style="font-size:66px;line-height:1.06;color:#fff;margin-top:16px">{e(p['headline'])}</div></div>
<div style="position:absolute;top:1000px;left:64px;right:64px;display:flex">{cols}</div>
<div style="position:absolute;left:64px;right:64px;bottom:64px;border-top:1px solid rgba(255,255,255,.14);padding-top:22px;display:flex;justify-content:space-between;align-items:flex-end"><div><div style="font-weight:600;font-size:18px;letter-spacing:.12em;color:#E0B940">{p.get('foot_label','BOOK YOUR FREE VALUATION')}</div><div class="serif" style="font-size:40px;color:#E0B940;margin-top:4px">{p.get('foot_url','duncanure.co.uk/valuation')}</div></div><img src="{LOGO_W}" style="height:70px"></div>'''
def review2(p):
    return f'''{sphoto(p['sphoto'], p.get('pos','center'))}
<div style="position:absolute;top:735px;left:64px;right:64px">{eyebrow(p['stars'])}<div style="font-family:'Cormorant Garamond',Georgia,serif;font-style:italic;font-weight:600;font-size:52px;line-height:1.16;color:#fff;margin-top:20px">&ldquo;{e(p['quote'])}&rdquo;</div><div style="font-weight:600;font-size:26px;color:#fff;margin-top:24px">{e(p['who'])}</div></div>
<div style="position:absolute;top:1035px;left:64px;right:64px;display:flex">{''.join(f'<div style="flex:1;{"padding-right:22px" if i==0 else "padding:0 22px;border-left:1px solid rgba(224,185,64,.6)"}"><div class="serif" style="font-size:46px;line-height:1.05;color:#E0B940">{e(a)}</div><div style="font-size:19px;color:rgba(255,255,255,.82);margin-top:8px">{e(b)}</div></div>' for i,(a,b) in enumerate(p['strip']))}</div>
<div style="position:absolute;left:64px;right:64px;bottom:64px;border-top:1px solid rgba(255,255,255,.14);padding-top:22px;display:flex;justify-content:space-between;align-items:flex-end"><div><div style="font-weight:600;font-size:18px;letter-spacing:.12em;color:#E0B940">BOOK YOUR FREE VALUATION</div><div class="serif" style="font-size:40px;color:#E0B940;margin-top:4px">duncanure.co.uk/valuation</div></div><img src="{LOGO_W}" style="height:70px"></div>'''

R = dict(SELLER=seller, REVIEW2=review2, T1=t1, T5=t5, CTA=cta, REVIEW=review, STAT=stat)

async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); pg = await b.new_page(viewport={'width':1080,'height':1350})
        for p in m.POSTS:
            doc = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><section>{R[p["tpl"]](p)}</section></body></html>'
            f = OUT/f'post-{p["id"]}.html'; f.write_text(doc)
            await pg.goto(f'file://{f}'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT/f'post-{p["id"]}.png'), clip=dict(x=0,y=0,width=1080,height=1350))
            print('rendered', p['id'])
        await b.close()
asyncio.run(main())
