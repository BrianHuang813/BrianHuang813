"""Generate the animated SVGs used by README.md.

Palette, type and easing mirror kxhuang.dev. Edit the data below and run:
    python3 assets/build.py
"""
import base64
import random
from html import escape
from pathlib import Path

HERE = Path(__file__).parent
FONT = base64.b64encode((HERE / "outfit-latin.woff2").read_bytes()).decode()

BG, TEXT, SOFT, FAINT, LINE, LINE_STRONG = "#000000", "#f2f2f2", "#a2a2a2", "#757575", "#232323", "#363636"
EASE = "cubic-bezier(0.22,1,0.36,1)"

BASE_CSS = f"""
@font-face {{ font-family: 'Outfit'; font-weight: 300 700; src: url(data:font/woff2;base64,{FONT}) format('woff2'); }}
text {{ font-family: 'Outfit', -apple-system, 'Segoe UI', 'PingFang TC', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif; letter-spacing: -0.005em; }}
.up {{ animation: up .9s {EASE} both; }}
.draw {{ stroke-dasharray: 1; animation: draw 1.2s {EASE} both; }}
@keyframes up {{ from {{ opacity: 0; transform: translateY(8px); }} }}
@keyframes draw {{ from {{ stroke-dashoffset: 1; }} }}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
"""

# ---------------------------------------------------------------- hero

FACTS = [
    # (dt en, dt zh, dd en, dd zh); a leading "name — " is rendered bright
    ("Now", "現任",
     "Low-latency trading engine & risk control in C++ for a Tier-1 brokerage",
     "以 C++ 為一線券商開發低延遲交易引擎與風控"),
    ("Research", "研究", "SuiAudit — AI auditing for Sui Move contracts", "SuiAudit — Sui Move 合約的 AI 稽核"),
    ("Built", "作品", "Blink Market — a prediction market on Sui", "Blink Market — Sui 上的預測市場"),
    ("Stack", "技術", "C++ · Go · Rust · Python · TypeScript · Sui Move", "C++ · Go · Rust · Python · TypeScript · Sui Move"),
]
INTRO = ("Fintech &amp; blockchain developer, based in Taipei.", "金融交易與區塊鏈開發，樂於探索世界和新事物")


def dd(text):
    if " — " not in text:
        return f'<tspan fill="{TEXT}">{escape(text)}</tspan>'
    name, rest = text.split(" — ", 1)
    return f'<tspan fill="{TEXT}">{escape(name)}</tspan><tspan fill="{SOFT}"> — {escape(rest)}</tspan>'


def sparkline(x0, y0, w, h, n=48, seed=801):
    """Deterministic random walk, scaled into the box; trends up because why not."""
    rnd = random.Random(seed)
    ys, v = [], 0.0
    for _ in range(n):
        v += rnd.uniform(-1, 1.25)
        ys.append(v)
    lo, hi = min(ys), max(ys)
    pts = [(x0 + w * i / (n - 1), y0 + h - h * (y - lo) / (hi - lo)) for i, y in enumerate(ys)]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts), pts[-1]


def hero():
    W, H = 840, 430
    path, (ex, ey) = sparkline(590, 104, 210, 52)
    nav = "".join(
        f'<text x="{x}" y="45" font-size="14" fill="{SOFT}">{t}</text>'
        for x, t in [(486, "About"), (546, "Projects"), (620, "Writing"), (688, "Life")]
    )
    rows = []
    for i, (dte, dtz, dde, ddz) in enumerate(FACTS):
        y = 262 + i * 40
        rows.append(f'''
  <g class="up" style="animation-delay:{1.0 + i * .12:.2f}s">
    <line x1="40" x2="800" y1="{y - 26}" y2="{y - 26}" stroke="{LINE}"/>
    <g class="en"><text x="40" y="{y}" font-size="14" fill="{FAINT}">{dte}</text><text x="150" y="{y}" font-size="15">{dd(dde)}</text></g>
    <g class="zh"><text x="40" y="{y}" font-size="14" fill="{FAINT}">{dtz}</text><text x="150" y="{y}" font-size="15">{dd(ddz)}</text></g>
  </g>''')
    css = BASE_CSS + f"""
.en {{ animation: en 14s linear 3s infinite; }}
.zh {{ opacity: 0; animation: zh 14s linear 3s infinite; }}
.toggle {{ animation: press 14s linear 3s infinite; }}
@keyframes en {{ 0%,44% {{ opacity: 1; }} 48%,96% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}
@keyframes zh {{ 0%,44% {{ opacity: 0; }} 48%,96% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}
@keyframes press {{ 0%,41%,47%,91%,97%,100% {{ stroke: {LINE_STRONG}; }} 44%,94% {{ stroke: {TEXT}; }} }}
.tick {{ stroke-dasharray: 1; animation: tick 7s {EASE} 1.2s infinite both; }}
.dot {{ opacity: 0; animation: dot 7s linear 1.2s infinite; }}
.ring {{ transform-box: fill-box; transform-origin: center; animation: ring 1.4s ease-out infinite; }}
@keyframes tick {{ 0% {{ stroke-dashoffset: 1; opacity: 1; }} 40%,88% {{ stroke-dashoffset: 0; opacity: 1; }} 100% {{ stroke-dashoffset: 0; opacity: 0; }} }}
@keyframes dot {{ 0%,38% {{ opacity: 0; }} 42%,88% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}
@keyframes ring {{ from {{ transform: scale(1); opacity: .6; }} to {{ transform: scale(3.2); opacity: 0; }} }}
"""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Kai Xiu Huang — Fintech &amp; blockchain developer, based in Taipei.">
<style>{css}</style>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="{BG}" stroke="{LINE}"/>
<g class="up">
  <text x="40" y="45" font-size="16" font-weight="600" fill="{TEXT}">Kai Xiu Huang</text>
  {nav}
  <circle class="toggle" cx="784" cy="40" r="16" fill="none" stroke="{LINE_STRONG}"/>
  <text class="en" x="784" y="44.5" font-size="12" fill="{SOFT}" text-anchor="middle">中</text>
  <text class="zh" x="784" y="44.5" font-size="11" fill="{SOFT}" text-anchor="middle">EN</text>
</g>
<line class="draw" pathLength="1" x1="40" x2="800" y1="74" y2="74" stroke="{LINE}" style="animation-delay:.2s"/>
<g class="up" style="animation-delay:.35s">
  <text x="40" y="158" font-size="52" font-weight="600" fill="{TEXT}" letter-spacing="-1">Kai Xiu Huang<tspan font-size="22" font-weight="400" fill="{FAINT}" dx="14" letter-spacing="0">黃楷修</tspan></text>
</g>
<line x1="590" x2="800" y1="130" y2="130" stroke="{LINE}" stroke-dasharray="2 4"/>
<path class="tick" pathLength="1" d="{path}" fill="none" stroke="{TEXT}" stroke-width="1.5" stroke-linejoin="round"/>
<g class="dot"><circle cx="{ex:.1f}" cy="{ey:.1f}" r="3" fill="{TEXT}"/><circle class="ring" cx="{ex:.1f}" cy="{ey:.1f}" r="3" fill="none" stroke="{TEXT}"/></g>
<g class="up" style="animation-delay:.6s">
  <text class="en" x="40" y="200" font-size="19" fill="{SOFT}">{INTRO[0]}</text>
  <text class="zh" x="40" y="200" font-size="19" fill="{SOFT}">{INTRO[1]}</text>
</g>{"".join(rows)}
<line class="draw" pathLength="1" x1="40" x2="800" y1="396" y2="396" stroke="{LINE}" style="animation-delay:1.6s"/>
</svg>
'''


# ---------------------------------------------------------------- project cards

PROJECTS = [
    # (slug, title, date, description lines, tags)
    ("blink-market", "Blink Market", "2026 · 06",
     ["Binary prediction market on Sui: off-chain RFQ", "quotes, atomic on-chain settlement."], "Sui Move · RFQ · DeFi"),
    ("suiaudit", "SuiAudit", "2026 · 03",
     ["Offline AI auditor for Sui Move contracts, built", "on Pure1 — a fine-tuned 7B model."], "LLM fine-tuning · Sui Move"),
    ("clawd-actor", "clawd-actor", "2026 · 10",
     ["Claude Code mod: Clawd acts out what Claude", "is doing, on a little stage above the prompt."], "TypeScript · Claude Code"),
    ("crow", "Crow", "2026 · 06",
     ["Developer projects compete for survival on a", "shared 60×60 grid. Interact, or go extinct."], "TypeScript · Python · Docker"),
    ("bluelink", "BlueLink", "2025 · 10",
     ["Tokenized blue bonds on Sui — funding ocean", "conservation, with principal tracked on-chain."], "Go · Sui Move · RWA"),
    ("portfolio-manager", "Portfolio Manager", "2026 · 10",
     ["One dashboard for Schwab, OKX, Futu and", "on-chain wallets, plus a relative-strength engine."], "TypeScript · React · Quant"),
]


def card(i, title, date, lines, tags):
    W, H = 410, 180
    d = i * .12
    desc = "".join(
        f'<text x="24" y="{102 + k * 21}" font-size="14" fill="{SOFT}">{escape(line)}</text>' for k, line in enumerate(lines)
    )
    css = BASE_CSS + f"""
.arrow {{ animation: nudge 2.8s {EASE} {1 + d:.2f}s infinite; }}
@keyframes nudge {{ 0%,60%,100% {{ transform: translateX(0); }} 30% {{ transform: translateX(5px); }} }}
"""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}">
<style>{css}</style>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{BG}" stroke="{LINE}"/>
<g class="up" style="animation-delay:{d:.2f}s">
  <text x="24" y="38" font-size="13" fill="{FAINT}">{i + 1:02d}</text>
  <text x="386" y="38" font-size="13" fill="{FAINT}" text-anchor="end">{date}</text>
  <text x="24" y="76" font-size="21" font-weight="600" fill="{TEXT}" letter-spacing="-0.4">{escape(title)}</text>
  {desc}
</g>
<line class="draw" pathLength="1" x1="24" x2="386" y1="142" y2="142" stroke="{LINE}" style="animation-delay:{.3 + d:.2f}s"/>
<g class="up" style="animation-delay:{.45 + d:.2f}s">
  <text x="24" y="164" font-size="13" fill="{FAINT}">{escape(tags)}</text>
  <text class="arrow" x="386" y="164" font-size="15" fill="{TEXT}" text-anchor="end">→</text>
</g>
</svg>
'''


if __name__ == "__main__":
    (HERE / "hero.svg").write_text(hero(), encoding="utf-8")
    for i, (slug, *rest) in enumerate(PROJECTS):
        (HERE / f"project-{slug}.svg").write_text(card(i, *rest), encoding="utf-8")
    print("built", 1 + len(PROJECTS), "svgs")
