
"""Static site generator: exercises.csv -> dist/ (HTML, sitemap.xml, robots.txt).
Usage: python3 build.py   (needs only Python 3, no installs)"""
import csv, os, re, json, html, shutil
from collections import defaultdict

SITE = "https://exercise-library-demo.jakubea.workers.dev"
OUT, MIN_FACET = "dist", 2     # facet pages with fewer exercises are skipped (thin content)
e = html.escape
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
EQ = {"dumbbell": "dumbbells", "barbell": "a barbell", "cable": "a cable machine",
      "machine": "machines", "kettlebell": "a kettlebell"}

rows = list(csv.DictReader(open("exercises.csv", encoding="utf-8")))
for r in rows:
    r["slug"], r["m"] = slug(r["name"]), slug(r["muscle"])
    r["steps"] = [s.strip() for s in r["steps"].split("|")]
    r["mistakes"] = [s.strip() for s in r["mistakes"].split("|")]
    r["sec"] = [s.strip() for s in r["secondary"].split(";") if s.strip()]
    r["url"] = f"/exercises/{r['m']}/{r['slug']}/"

CSS = ("body{font:17px/1.65 system-ui,sans-serif;max-width:720px;margin:0 auto;padding:1rem 1.2rem;"
       "background:#f5f6f2;color:#1f2a26}h1,h2{font-family:Georgia,serif;line-height:1.2}"
       "a{color:#2f3fc4}header a{font-weight:700;text-decoration:none}.bc{font-size:.85rem;color:#5d6a64}"
       ".list{padding:0;list-style:none}.list li{padding:.55rem 0;border-bottom:1px solid #dde1da}"
       ".list span{color:#5d6a64;font-size:.88rem;margin-left:.4rem}footer{margin:3rem 0 1rem;font-size:.82rem;color:#5d6a64}"
       "iframe{width:100%;aspect-ratio:16/9;border:0}"
       "@media(prefers-color-scheme:dark){body{background:#17201c;color:#e3e8e4}a{color:#9aa7ff}"
       ".list li{border-color:#2c3832}.bc,.list span,footer{color:#9aa7a0}}")
pages = []

def write(path, title, desc, body, crumbs, extra=None):
    url = "/" + path
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u}
        for i, (n, u) in enumerate(crumbs)]}]
    if extra:
        ld.append(extra)
    ld_html = "".join('<script type="application/ld+json">' + json.dumps(x) + "</script>" for x in ld)
    nav = " › ".join(f'<a href="{u}">{e(n)}</a>' for n, u in crumbs[:-1])
    nav += (" › " if len(crumbs) > 1 else "") + e(crumbs[-1][0])
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title>
<meta name="description" content="{e(desc)}"><link rel="canonical" href="{SITE}{url}">
<style>{CSS}</style>{ld_html}</head><body><header><a href="/">Exercise Library</a></header>
<main><nav class="bc">{nav}</nav>{body}</main>
<footer>General information only, not a substitute for a qualified trainer.</footer></body></html>"""
    os.makedirs(os.path.join(OUT, path), exist_ok=True)
    open(os.path.join(OUT, path, "index.html"), "w", encoding="utf-8").write(doc)
    pages.append(url)

def lst(xs):
    return '<ul class="list">' + "".join(
        f'<li><a href="{x["url"]}">{e(x["name"])}</a><span>{e(x["equipment"])}, {e(x["level"])}</span></li>'
        for x in xs) + "</ul>"

def facet_title(m, kind, v):
    M = m.title()
    if kind == "level":
        return f"{v.title()} {M} Exercises"
    if v == "bodyweight":
        return f"Bodyweight {M} Exercises (No Equipment)"
    return f"{M} Exercises with {EQ.get(v, v)}"

shutil.rmtree(OUT, ignore_errors=True)
by_m = defaultdict(list)
for r in rows:
    by_m[r["muscle"]].append(r)

for m, xs in by_m.items():
    ms, M = slug(m), m.title()
    fs = []
    for kind in ("equipment", "level"):
        g = defaultdict(list)
        for x in xs:
            g[x[kind]].append(x)
        for v, ys in g.items():
            if len(ys) >= MIN_FACET:
                fs.append((kind, v, facet_title(m, kind, v), f"exercises/{ms}/{kind}/{slug(v)}/", ys))

    fpaths = {(k, v): p for k, v, t, p, _ in fs}

    for k, v, t, p, ys in fs:
        names = ", ".join(y["name"] for y in ys[:3])

        if k == "equipment":
            desc = f"{len(ys)} {m} exercises using {EQ.get(v, v)}, including {names}. Explore step-by-step instructions for each exercise."
        else:
            desc = f"{len(ys)} {v} {m} exercises, including {names}. Explore step-by-step instructions for each exercise."

        write(p, f"{t} | Exercise Library", desc,
              f"<h1>{e(t)}</h1>{lst(ys)}<p><a href='/exercises/{ms}/'>All {e(m)} exercises</a></p>",
              [("Home", "/"), (f"{M} exercises", f"/exercises/{ms}/"), (t, "/" + p)])

    links = "".join(f'<li><a href="/{p}">{e(t)}</a></li>' for _, _, t, p, _ in fs)
    write(f"exercises/{ms}/", f"{M} Exercises: Instructions and Variations | Exercise Library",
          f"{len(xs)} {m} exercises with step-by-step instructions, common mistakes and equipment options.",
          f"<h1>{M} Exercises</h1><p>{len(xs)} exercises for the {e(m)}.</p>"
          + (f"<h2>Narrow it down</h2><ul>{links}</ul>" if links else "") + "<h2>All exercises</h2>" + lst(xs),
          [("Home", "/"), (f"{M} exercises", f"/exercises/{ms}/")])

    for i, r in enumerate(xs):
        rel = [xs[(i + k) % len(xs)] for k in range(1, min(4, len(xs)))]
        eqtxt = "It needs no equipment." if r["equipment"] == "bodyweight" else f"It uses {r['equipment']}."
        sec = f", with help from the {', '.join(r['sec'])}" if r["sec"] else ""
        intro = f"The {r['name']} is a {r['level']} {r['type']} exercise for the {r['muscle']}{sec}. {eqtxt}"
        video = (f'<h2>Video</h2><iframe loading="lazy" src="https://www.youtube-nocookie.com/embed/{e(r["video"])}" '
                 f'title="{e(r["name"])} video" allowfullscreen></iframe>') if r["video"] else ""
        more = "".join(f'<li><a href="/{fpaths[k]}">{facet_title(m, *k)}</a></li>'
                       for k in (("equipment", r["equipment"]), ("level", r["level"])) if k in fpaths)
        body = (f"<h1>{e(r['name'])}</h1><p>{e(intro)}</p><h2>How to do it</h2><ol>"
                + "".join(f"<li>{e(s)}</li>" for s in r["steps"]) + "</ol><h2>Common mistakes</h2><ul>"
                + "".join(f"<li>{e(s)}</li>" for s in r["mistakes"]) + f"</ul>{video}"
                + (f"<h2>Related exercises</h2>{lst(rel)}" if rel else "")
                + (f"<h2>More like this</h2><ul>{more}</ul>" if more else ""))
        howto = {"@context": "https://schema.org", "@type": "HowTo", "name": f"How to do the {r['name']}",
                 "step": [{"@type": "HowToStep", "text": s} for s in r["steps"]]}
        write(r["url"][1:], f"{r['name']}: How to, Muscles Worked and Mistakes | Exercise Library",
              f"How to do the {r['name']}: step-by-step instructions and common mistakes. {r['level'].title()} {m} exercise.",
              body, [("Home", "/"), (f"{M} exercises", f"/exercises/{ms}/"), (r["name"], r["url"])], howto)

hub = "".join(f'<li><a href="/exercises/{slug(m)}/">{m.title()} exercises</a><span>{len(xs)} exercises</span></li>'
              for m, xs in by_m.items())
write("", "Exercise Library: Exercises by Muscle Group for Trainers",
      f"{len(rows)} exercises sorted by muscle group, equipment and level, with instructions for building client workouts.",
      f"<h1>Exercises by muscle group</h1><p>Pick a muscle group, narrow by equipment or level, and build a workout for your client.</p><ul class='list'>{hub}</ul>",
      [("Home", "/")])

open(f"{OUT}/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                                      + "".join(f"<url><loc>{SITE}{u}</loc></url>" for u in pages) + "</urlset>")
open(f"{OUT}/robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
print(f"Built {len(pages)} pages into {OUT}/")
