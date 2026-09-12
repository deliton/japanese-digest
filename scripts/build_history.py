#!/usr/bin/env python3
"""Rebuild history/index.html from history.json — O(n) tiny list, never embeds article bodies."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "history.json"
OUT = ROOT / "history" / "index.html"


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    entries = sorted(data.get("entries", []), key=lambda e: e["date"], reverse=True)

    by_month: dict[str, list] = defaultdict(list)
    for e in entries:
        by_month[e["date"][:7]].append(e)

    months_html = []
    for month in sorted(by_month.keys(), reverse=True):
        rows = []
        for e in by_month[month]:
            topics = " · ".join(esc(t) for t in e.get("topics", [])[:6])
            rows.append(
                f"""        <li>
          <a class="row" href="{esc(e['href'])}">
            <time datetime="{esc(e['date'])}">{esc(e['date'])}</time>
            <span class="headline">{esc(e.get('headline', e['date']))}</span>
            <span class="meta"><span class="mins">~{int(e.get('minutes', 0))}′</span>
            <span class="topics">{topics}</span></span>
          </a>
        </li>"""
            )
        y, m = month.split("-")
        months_html.append(
            f"""    <section class="month" id="m-{esc(month)}">
      <h2>{esc(y)} / {esc(m)}</h2>
      <ol class="list">
{chr(10).join(rows)}
      </ol>
    </section>"""
        )

    count = len(entries)
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>読解幕 · History</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&family=Shippori+Mincho:wght@500;700&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --bg: #0a0a0a;
      --bg-card: #161616;
      --ink: #f5f5f5;
      --ink-dim: #a8a29a;
      --ink-mute: #6b6560;
      --shu: #c41e3a;
      --shu-hot: #e11d48;
      --gold: #d4a017;
      --line: #2a2a2a;
      --radius: 4px;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: "Noto Sans JP", system-ui, sans-serif;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
    }}
    .stage-bar {{
      height: 6px;
      background: repeating-linear-gradient(
        90deg,
        var(--shu) 0 48px,
        #fafafa 48px 56px,
        #111 56px 64px,
        var(--gold) 64px 72px,
        #111 72px 88px
      );
    }}
    .wrap {{
      width: min(100% - 2rem, 42rem);
      margin: 0 auto;
      padding: 1.75rem 0 3.5rem;
    }}
    .top {{
      display: flex;
      flex-wrap: wrap;
      align-items: baseline;
      justify-content: space-between;
      gap: 0.75rem;
      margin-bottom: 1.5rem;
      padding-bottom: 1rem;
      border-bottom: 1px solid var(--line);
    }}
    .brand {{
      font-family: "Shippori Mincho", serif;
      font-size: 1.55rem;
      font-weight: 700;
      margin: 0;
      letter-spacing: 0.06em;
    }}
    .brand em {{ font-style: normal; color: var(--shu); }}
    .nav a {{
      color: var(--gold);
      text-decoration: none;
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: 0.08em;
    }}
    .nav a:hover {{ color: var(--shu-hot); }}
    .lede {{
      color: var(--ink-dim);
      font-size: 0.9rem;
      margin: 0 0 1.5rem;
    }}
    .stat {{
      display: inline-block;
      border: 1px solid var(--line);
      padding: 0.2rem 0.55rem;
      font-size: 0.72rem;
      color: var(--ink-mute);
      margin-left: 0.35rem;
    }}
    .month {{ margin-bottom: 1.75rem; }}
    .month h2 {{
      margin: 0 0 0.65rem;
      font-size: 0.72rem;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--gold);
      font-weight: 700;
    }}
    .list {{
      list-style: none;
      margin: 0;
      padding: 0;
      border: 1px solid var(--line);
      background: var(--bg-card);
    }}
    .list li + li {{ border-top: 1px solid var(--line); }}
    .row {{
      display: grid;
      grid-template-columns: 6.5rem 1fr;
      gap: 0.25rem 0.85rem;
      padding: 0.75rem 0.85rem;
      text-decoration: none;
      color: inherit;
    }}
    @media (min-width: 560px) {{
      .row {{ grid-template-columns: 6.5rem 1fr auto; align-items: baseline; }}
    }}
    .row:hover {{ background: #1c1c1c; }}
    .row:hover .headline {{ color: #fff; }}
    time {{
      font-variant-numeric: tabular-nums;
      font-size: 0.78rem;
      color: var(--shu-hot);
      font-weight: 700;
      padding-top: 0.15rem;
    }}
    .headline {{
      font-size: 0.92rem;
      color: var(--ink-dim);
      line-height: 1.35;
    }}
    .meta {{
      grid-column: 2 / -1;
      display: flex;
      flex-wrap: wrap;
      gap: 0.35rem 0.75rem;
      font-size: 0.72rem;
      color: var(--ink-mute);
    }}
    @media (min-width: 560px) {{
      .meta {{
        grid-column: auto;
        flex-direction: column;
        align-items: flex-end;
        text-align: right;
        max-width: 11rem;
      }}
    }}
    .mins {{ color: var(--gold); font-weight: 700; }}
    .topics {{ overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 100%; }}
    footer {{
      margin-top: 2rem;
      font-size: 0.72rem;
      color: var(--ink-mute);
      letter-spacing: 0.06em;
    }}
  </style>
</head>
<body>
  <div class="stage-bar" aria-hidden="true"></div>
  <div class="wrap">
    <header class="top">
      <p class="brand">読解<em>幕</em> <span class="stat">{count} dias</span></p>
      <nav class="nav"><a href="../">← hoje</a></nav>
    </header>
    <p class="lede">Arquivo leve: só links. Cada dia abre o digest completo. Em 500 dias isso continua sendo uma listinha.</p>
{chr(10).join(months_html) if months_html else '    <p class="lede">Ainda sem entradas.</p>'}
    <footer>history · gerado de history.json · sem corpos de artigo nesta página</footer>
  </div>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({count} entries, {OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
