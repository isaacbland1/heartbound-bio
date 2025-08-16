import base64, json, pathlib, html, time
root = pathlib.Path.home()/ "OneDrive/Projects/heartbound-bio"
assets = root/"assets"
ts = str(int(time.time()))
def esc(s): return html.escape(s or "")
def datauri(img):
    if not img: 
        f = assets/"placeholder.svg"
    else:
        f = assets/pathlib.Path(img).name
        if not f.exists(): f = assets/"placeholder.svg"
    ext = f.suffix.lower().strip(".")
    mt = {"jpg":"jpeg","jpeg":"jpeg","png":"png","svg":"svg+xml","webp":"webp"}.get(ext,"octet-stream")
    b64 = base64.b64encode(f.read_bytes()).decode("ascii")
    return f"data:image/{mt};base64,{b64}"
cfg = json.loads((root/"config.json").read_text()) if (root/"config.json").exists() else {
  "brandName":"Heartbound Journeys","brandTagline":"Tools, stories, and services for long-distance love.","mainSiteUrl":"#","disclaimer":"As an Amazon Associate I earn from qualifying purchases."
}
aff = json.loads((root/"affiliates.json").read_text()) if (root/"affiliates.json").exists() else []
svc = json.loads((root/"services.json").read_text()) if (root/"services.json").exists() else []
def card(img,name,desc,url,cta):
    src = datauri(img)
    return f'''<div class="card">
  <img src="{src}" alt="{esc(name or 'Item')}"/>
  <div class="meta"><h3>{esc(name or 'Untitled')}</h3><p>{esc(desc or '')}</p></div>
  <div class="actions"><a class="btn btn-primary" target="_blank" rel="noopener" href="{esc(url or '#')}">{esc(cta)}</a></div>
</div>'''
aff_html = "\n".join(card(a.get("image"), a.get("name"), a.get("desc"), a.get("url"), "View") for a in aff)
svc_html = "\n".join(card(s.get("image"), s.get("name"), s.get("desc"), s.get("url"), "Book / Learn More") for s in svc)
html_out = f'''<!doctype html><html lang="en"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Heartbound Journeys – Links</title>
<link rel="stylesheet" href="styles/main.css?v={ts}"/>
</head><body>
<header id="header">
  <h1 id="brand">{esc(cfg.get("brandName","Heartbound Journeys"))}</h1>
  <p id="tagline">{esc(cfg.get("brandTagline",""))}</p>
  <a id="main-site-link" class="btn btn-primary" target="_blank" rel="noopener" href="{esc(cfg.get("mainSiteUrl","#"))}">Visit Main Site</a>
</header>
<main>
  <section><h2>Featured Tools & Products</h2><div id="affiliates" class="grid">{aff_html}</div></section>
  <section><h2>Our Services</h2><div id="services" class="grid">{svc_html}</div></section>
  <footer><p id="disclaimer">{esc(cfg.get("disclaimer",""))}</p></footer>
</main>
</body></html>'''
(root/"index.html").write_text(html_out)
print("OK")
