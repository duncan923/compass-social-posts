import json, html, os, datetime as dt
WEEK=os.environ['CS_WEEK']; w=json.load(open(os.path.join(WEEK,'out','week.json'))); e=html.escape
TITLE=os.environ.get('CS_TITLE','Compass Week Posts')
TYPE={'T1':'Listing','T5':'Proof: under offer','CTA':'Seller','REVIEW':'Review','STAT':'Proof: price and speed','REVIEW2':'Review','SELLER':'Seller'}
cards=[]
for p in sorted(w,key=lambda x:x['slot']):
    d=dt.datetime.fromisoformat(p['slot'])
    flag=f'<div class="flag"><strong>Needs you:</strong> {e(p["check"])}</div>' if p['check'] else ''
    cards.append(f'''<article class="post" id="p{p['id']}">
<div class="meta"><span class="num">{p['id']}</span><span class="when">{d.strftime('%a %-d %b')} &middot; {d.strftime('%H:%M')}</span><span class="pill {'seller' if p['kind']=='seller' else 'listing'}">{TYPE[p['tpl']]}</span></div>
<div class="body"><img src="posts/post-{p['id']}.jpg" alt="Post {p['id']} graphic" loading="lazy" width="1080" height="1350">
<div class="copy">{flag}<h3>Facebook caption</h3><pre>{e(p['fb'])}</pre><details><summary>Instagram caption</summary><pre>{e(p['ig'])}</pre></details></div></div></article>''')
need=sum(1 for p in w if p['check'])
page=f'''<title>{TITLE}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=Instrument+Sans:wght@400;600;700&display=swap">
<style>
/* Layout: one column of post cards, graphic left and caption right, stacking on phones */
:root{{--bg:#F2F3F0;--surface:#FFFFFF;--fg:#363C52;--muted:#6B7280;--line:rgba(54,60,82,.12);--gold:#E0B940;--goldtext:#97781F;--warnbg:#FAF0D2;--warnfg:#6B5416;
--display:'Ivar Soft','Cormorant Garamond',Georgia,serif;--body:'Instrument Sans',Arial,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1D2130;--surface:#252A3A;--fg:#F2F3F0;--muted:#A6ABBA;--line:rgba(242,243,240,.12);--goldtext:#ECCD6E;--warnbg:#3A3220;--warnfg:#F4E1A3;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#1D2130;--surface:#252A3A;--fg:#F2F3F0;--muted:#A6ABBA;--line:rgba(242,243,240,.12);--goldtext:#ECCD6E;--warnbg:#3A3220;--warnfg:#F4E1A3;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font-family:var(--body);font-size:15px;line-height:1.55}}
.wrap{{max-width:1080px;margin:0 auto;padding-block:32px 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:flex;flex-direction:column;gap:24px}}
.eyebrow{{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--goldtext);display:flex;align-items:center;gap:12px}}
.eyebrow::before{{content:"";width:40px;height:2px;background:var(--gold)}}
h1{{font-family:var(--display);font-weight:600;font-size:clamp(30px,5vw,44px);line-height:1.1;margin:8px 0 6px;text-wrap:balance}}
.lede{{color:var(--muted);max-width:65ch;margin:0}}
.summary{{display:flex;flex-wrap:wrap;gap:8px 20px;font-size:14px;color:var(--muted)}} .summary b{{color:var(--fg)}}
.approve{{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:16px 18px;max-width:72ch}}
.approve code{{font-family:var(--body);font-weight:700;color:var(--goldtext)}}
.post{{background:var(--surface);border:1px solid var(--line);border-radius:6px;overflow:hidden}}
.meta{{display:flex;align-items:center;gap:12px;padding:12px 18px;border-bottom:1px solid var(--line);flex-wrap:wrap}}
.num{{font-family:var(--display);font-size:22px;font-variant-numeric:tabular-nums;color:var(--goldtext)}}
.when{{font-weight:600}}
.pill{{font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;border:1px solid var(--line);border-radius:999px;padding:3px 10px;color:var(--muted)}}
.pill.seller{{color:var(--goldtext);border-color:var(--gold)}}
.body{{display:grid;grid-template-columns:minmax(0,340px) minmax(0,1fr);gap:20px;padding:18px}}
.body img{{width:100%;height:auto;border-radius:3px;display:block}}
.copy{{min-width:0;display:flex;flex-direction:column;gap:10px}}
h3{{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:0}}
pre{{white-space:pre-wrap;font-family:var(--body);font-size:14px;margin:0}}
details summary{{cursor:pointer;font-size:13px;font-weight:600;color:var(--goldtext)}}
.flag{{background:var(--warnbg);color:var(--warnfg);border-radius:3px;padding:10px 12px;font-size:14px}}
@media (max-width:700px){{.body{{grid-template-columns:1fr}}}}
</style>
<div class="wrap">
<header><div class="eyebrow">Tuesday 27 October to Monday 2 November</div><h1>This week's 14 posts</h1>
<p class="lede">Everything below is built and waiting. Nothing is scheduled until you approve. Facebook at 08:00 and 13:00 every day, with an Instagram copy of each post.</p></header>
<div class="summary"><span><b>8</b> listing posts</span><span><b>6</b> seller posts</span><span>Every hook checked against posts since 30 July</span><span><b>{need}</b> need something from you</span></div>
<div class="approve">To approve, reply in the chat with <code>approved</code>, or <code>approved except 7, 9</code> to hold some back. Corrections go in the same reply, for example <code>6: 6 days</code>.</div>
{''.join(cards)}
</div>'''
os.makedirs(os.path.join(WEEK,'site'),exist_ok=True); open(os.path.join(WEEK,'site','index.html'),'w').write(page)
