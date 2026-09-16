"""Genera tarjetas SVG de estadisticas reales con datos de GitHub API.

Solo stdlib (sin dependencias). Lee repos publicos del usuario,
agrega lenguajes y escribe generated/overview.svg + generated/languages.svg.

Uso:
    GITHUB_USER=cannaarryy python stats/generate.py
    GITHUB_TOKEN=...     (opcional, sube el rate limit de la API)
"""
import json
import os
import urllib.request
from datetime import date

USER = os.environ.get("GITHUB_USER", "cannaarryy")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "generated")

# Paleta del perfil
BG = "#0A0A0A"
BORDER = "#242424"
TEXT = "#F5F5F5"
MUTED = "#8A8A8A"
ACCENT = "#38BDF8"
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def api(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "cannaarryy-stats-generator",
    })
    if TOKEN:
        req.add_header("Authorization", "Bearer " + TOKEN)
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.load(res)


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fetch_repos():
    repos, page = [], 1
    while True:
        batch = api("https://api.github.com/users/%s/repos?per_page=100&page=%d" % (USER, page))
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return [r for r in repos if not r.get("fork")]


def overview_svg(n_repos, stars, forks):
    return """<svg xmlns="http://www.w3.org/2000/svg" width="440" height="200" viewBox="0 0 440 200">
  <rect width="438" height="198" x="1" y="1" rx="8" fill="{bg}" stroke="{bd}"/>
  <text x="24" y="36" font-family="{f}" font-size="13" fill="{tx}">$ stats --user {user}</text>
  <line x1="24" y1="50" x2="416" y2="50" stroke="{bd}"/>
  <text x="24" y="100" font-family="{f}" font-size="34" font-weight="bold" fill="#FFFFFF">{repos}</text>
  <text x="24" y="120" font-family="{f}" font-size="11" fill="{mu}">REPOS</text>
  <text x="180" y="100" font-family="{f}" font-size="34" font-weight="bold" fill="#FFFFFF">{stars}</text>
  <text x="180" y="120" font-family="{f}" font-size="11" fill="{mu}">STARS</text>
  <text x="330" y="100" font-family="{f}" font-size="34" font-weight="bold" fill="#FFFFFF">{forks}</text>
  <text x="330" y="120" font-family="{f}" font-size="11" fill="{mu}">FORKS</text>
  <line x1="24" y1="148" x2="416" y2="148" stroke="{bd}"/>
  <text x="24" y="170" font-family="{f}" font-size="10" fill="{mu}">via github api · updated {d}</text>
  <circle cx="404" cy="168" r="4" fill="{ac}" opacity="0.8"/>
</svg>""".format(bg=BG, bd=BORDER, tx=TEXT, mu=MUTED, ac=ACCENT, f=FONT,
                 user=esc(USER), repos=n_repos, stars=stars, forks=forks, d=date.today().isoformat())


def languages_svg(langs):
    rows = []
    y = 78
    total = sum(n for _, n in langs) or 1
    top_bytes = langs[0][1] if langs else 1
    for i, (name, nbytes) in enumerate(langs[:5]):
        pct = 100.0 * nbytes / total
        w = max(8, int(210 * nbytes / top_bytes))
        op = round(1.0 - i * 0.14, 2)
        rows.append(
            '  <text x="24" y="{y}" font-family="{f}" font-size="12" fill="{tx}">{name}</text>'
            '  <rect x="150" y="{y0}" width="{w}" height="10" rx="2" fill="{ac}" opacity="{op}"/>'
            '  <text x="372" y="{y}" font-family="{f}" font-size="11" fill="{mu}">{pct:.0f}%</text>'.format(
                y=y, y0=y - 9, w=w, name=esc(name), pct=pct, f=FONT, tx=TEXT, ac=ACCENT, mu=MUTED, op=op))
        y += 26
    if not rows:
        rows.append('  <text x="24" y="100" font-family="{f}" font-size="12" fill="{mu}">no language data yet</text>'.format(f=FONT, mu=MUTED))
    body = "\n".join(rows)
    return """<svg xmlns="http://www.w3.org/2000/svg" width="440" height="200" viewBox="0 0 440 200">
  <rect width="438" height="198" x="1" y="1" rx="8" fill="{bg}" stroke="{bd}"/>
  <text x="24" y="36" font-family="{f}" font-size="13" fill="{tx}">$ top-languages --user {user}</text>
  <line x1="24" y1="50" x2="416" y2="50" stroke="{bd}"/>
{body}
</svg>""".format(bg=BG, bd=BORDER, tx=TEXT, f=FONT, user=esc(USER), body=body)


def main():
    repos = fetch_repos()
    stars = sum(r.get("stargazers_count", 0) for r in repos)
    forks = sum(r.get("forks_count", 0) for r in repos)
    lang_bytes = {}
    for r in repos:
        try:
            for lang, n in api(r["languages_url"]).items():
                lang_bytes[lang] = lang_bytes.get(lang, 0) + n
        except Exception as e:
            print("warn: no se pudo leer lenguajes de %s (%s)" % (r.get("name"), e))
    top = sorted(lang_bytes.items(), key=lambda kv: kv[1], reverse=True)
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "overview.svg"), "w", encoding="utf-8") as f:
        f.write(overview_svg(len(repos), stars, forks))
    with open(os.path.join(OUT_DIR, "languages.svg"), "w", encoding="utf-8") as f:
        f.write(languages_svg(top))
    print("repos=%d stars=%d forks=%d langs=%s" % (
        len(repos), stars, forks, ",".join(n for n, _ in top) or "-"))


if __name__ == "__main__":
    main()
