import importlib.util, json, re, os
from pathlib import Path
B = Path(os.environ['CS_WEEK'])
spec = importlib.util.spec_from_file_location('posts', B/'posts.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

BUYER = "DM me, or call or WhatsApp 07513 901 909, to book a viewing."
def build(p):
    if p['kind'] == 'listing':
        fb = [p['hook'], p['body'], BUYER, f"Full details and the video tour: {p['url']}", (f"Council tax band {p['ctax']}." if p.get('ctax') else p.get('rv','')), m.SELLER_FB, p['tags']]
        ig = [p['hook'], p['body'], BUYER, "Full details on compass-estates.co.uk", (f"Council tax band {p['ctax']}." if p.get('ctax') else p.get('rv','')), m.SELLER_IG, p['tags']]
    else:
        if p.get('refer'):
            fb = [p['hook'], p['body'].replace('duncanure.co.uk/refer','duncanure.co.uk/refer?utm_source=facebook'), "Thinking of selling yourself? Book a free valuation at " + m.VAL_FB, p['tags']]
            ig = [p['hook'], p['body'].replace('at duncanure.co.uk/refer','through the link in my bio'), p['tags']]
        else:
            fb = [p['hook'], p['body'], f"Book a free valuation at {m.VAL_FB}", p['tags']]
            ig = [p['hook'], p['body'], "Book a free valuation: link in bio.", p['tags']]
    return "\n\n".join(fb), "\n\n".join(ig)

BANNED = r"\b(stunning|must-see|must be seen|rarely available|dream home|immaculate|nestled|boasts?|boasting|charming|deceptively spacious|viewing highly recommended|actually|certainly|absolutely|of course|unlock|leverage|seamless|game-changer|robust|comprehensive|cutting-edge|transformative|innovative|genuinely|conveyancer|freehold|leasehold|stamp duty|exchange of contracts|gazumping|completion|asking price|D&G)\b"
def qc(t):
    issues = []
    if re.search(BANNED, t, re.I): issues.append("banned: " + ", ".join(set(x.lower() for x in re.findall(BANNED, t, re.I))))
    if re.search("[–—]", t) or " -- " in t: issues.append("dash")
    if "!" in t: issues.append("exclamation")
    if re.search("[\U0001F300-\U0001FAFF☀-➿]", t): issues.append("emoji")
    if len(re.findall(r"#\w+", t)) > 3: issues.append("hashtags>3")
    if "Dumfries & Galloway" not in t and "Galloway" in t and "#DumfriesandGalloway" not in t: pass
    return issues

out = []
for p in m.POSTS:
    fb, ig = build(p)
    out.append(dict(id=p['id'], slot=p['slot'], kind=p['kind'], tpl=p['tpl'], fb=fb, ig=ig, check=p.get('check'), qc=qc(fb)+qc(ig)))
(B/'out').mkdir(parents=True, exist_ok=True); (B/'out'/'week.json').write_text(json.dumps(out, indent=1, ensure_ascii=False))
for o in out: print(o['id'], o['slot'][:16], len(o['fb']), o['qc'] or 'ok', '| CHECK' if o['check'] else '')
