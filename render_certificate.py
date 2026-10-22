"""
Neurospicy-Visualisierung
=========================
Alle Funktionen geben fertige HTML-Snippets (SVG + eingebettetes CSS) zurück:

    render_title_html()          -> Titel "How Neurospicy are you?"
    render_adhd_html(wert)       -> ADHS-Verteilungen + Markierung der Person
    render_autism_html(wert)     -> Autismus-Verteilungen + Markierung der Person
    render_distribution_html()   -> allgemeine Variante für beliebige Gruppen

Benötigt nur die Standardbibliothek.
"""
import math
import uuid
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# 1. Kennwerte der Referenzgruppen
# ---------------------------------------------------------------------------
ADHD_GROUP_MEAN = 41.57
ADHD_GROUP_SD = 9.93

NORM_ADHD_GROUP_MEAN = 19.69
NORM_ADHD_GROUP_SD = 6.68

AUTISM_GROUP_MEAN = 74.95
AUTISM_GROUP_SD = 11.56

NORM_AUTISM_GROUP_MEAN = 38.72
NORM_AUTISM_GROUP_SD = 12.84


# ---------------------------------------------------------------------------
# 2. Gruppen (Name, Kennwerte, Farbe)
# ---------------------------------------------------------------------------
@dataclass
class Group:
    name: str
    mean: float
    sd: float
    color: str


NORM_COLOR = "#0d9488"  # Türkis für alle Normgruppen

ADHD = Group("ADHS-Gruppe", ADHD_GROUP_MEAN, ADHD_GROUP_SD, "#e11d63")
ADHD_NORM = Group("Normgruppe", NORM_ADHD_GROUP_MEAN, NORM_ADHD_GROUP_SD, NORM_COLOR)

AUTISM = Group("Autismus-Gruppe", AUTISM_GROUP_MEAN, AUTISM_GROUP_SD, "#7c3aed")
AUTISM_NORM = Group("Normgruppe", NORM_AUTISM_GROUP_MEAN, NORM_AUTISM_GROUP_SD, NORM_COLOR)


# ---------------------------------------------------------------------------
# 3. Mathe
# ---------------------------------------------------------------------------
def _pdf(x: float, mean: float, sd: float) -> float:
    """Dichte der Normalverteilung (Höhe der Kurve)."""
    return math.exp(-0.5 * ((x - mean) / sd) ** 2) / (sd * math.sqrt(2 * math.pi))


def _cdf(x: float, mean: float, sd: float) -> float:
    """Anteil der Gruppe, der unter x liegt (0..1)."""
    return 0.5 * (1 + math.erf((x - mean) / (sd * math.sqrt(2))))


# ---------------------------------------------------------------------------
# 4. CSS
#    "__UID__" wird pro Aufruf durch eine eindeutige ID ersetzt, damit sich
#    mehrere Grafiken auf derselben Seite nicht gegenseitig stylen.
# ---------------------------------------------------------------------------
_TITLE_FONT = "@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@600;700&display=swap');"

_TITLE_CSS = """
#__UID__ {
  text-align: center;
  padding: 24px 16px 16px;
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
}
#__UID__ h1 {
  margin: 0;
  font-family: 'Fredoka', system-ui, sans-serif;
  font-size: clamp(2rem, 6vw, 3.2rem);
  font-weight: 700;
  line-height: 1.1;
}
#__UID__ .grad {
  background: linear-gradient(90deg, #e11d63, #f97316, #7c3aed, #0d9488, #e11d63);
  background-size: 300% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: __UID__-shift 8s linear infinite;
}
#__UID__ .chili { display: inline-block; animation: __UID__-wiggle 1.8s ease-in-out infinite; }
#__UID__ .sub { margin: 8px 0 0; font-size: 1rem; color: #6b7280; }

@keyframes __UID__-shift  { to { background-position: 300% 0; } }
@keyframes __UID__-wiggle {
  0%, 100% { transform: rotate(-10deg); }
  50%      { transform: rotate(12deg); }
}
@media (prefers-reduced-motion: reduce) {
  #__UID__ .grad, #__UID__ .chili { animation: none; }
}
"""

_CHART_CSS = """
#__UID__ {
  /* --c-clin und --c-norm werden im HTML pro Grafik gesetzt */
  --c-user: #111827;
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  color: #374151;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 18px 20px 16px;
  margin: 0 0 20px;
  box-sizing: border-box;
}

/* Kopf: Thema + Ergebnis in einem Satz */
#__UID__ h2 {
  margin: 0;
  font-size: 13px; font-weight: 600;
  text-transform: uppercase; letter-spacing: .06em; color: #6b7280;
}
#__UID__ .result { margin: 4px 0 6px; font-size: 1.35rem; font-weight: 600; color: #111827; }
#__UID__ .result .hl { color: var(--c-hl); }

/* Grafik */
#__UID__ svg { width: 100%; height: auto; display: block; }
#__UID__ .baseline { stroke: #d1d5db; stroke-width: 1; }
#__UID__ .tick     { font-size: 12px; fill: #9ca3af; }
#__UID__ .area-clin { fill: var(--c-clin); fill-opacity: .12; }
#__UID__ .area-norm { fill: var(--c-norm); fill-opacity: .12; }
#__UID__ .line-clin { fill: none; stroke: var(--c-clin); stroke-width: 2.5; }
#__UID__ .line-norm { fill: none; stroke: var(--c-norm); stroke-width: 2.5; }
#__UID__ .lbl { font-size: 13px; font-weight: 600;
  paint-order: stroke; stroke: #fff; stroke-width: 4px; stroke-linejoin: round; }
#__UID__ .lbl-clin { fill: var(--c-clin); }
#__UID__ .lbl-norm { fill: var(--c-norm); }

/* Markierung der Person */
#__UID__ .user-line { stroke: var(--c-user); stroke-width: 2.5; }
#__UID__ .user-dot  { stroke: #fff; stroke-width: 2; }
#__UID__ .dot-clin  { fill: var(--c-clin); }
#__UID__ .dot-norm  { fill: var(--c-norm); }
#__UID__ .user-badge { fill: var(--c-user); }
#__UID__ .user-badge-text { fill: #fff; font-size: 13px; font-weight: 700; }

/* Zahlen darunter */
#__UID__ .stats { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 10px; }
#__UID__ .stat {
  flex: 1 1 200px;
  padding: 8px 12px;
  border-left: 4px solid var(--c-bar);
  background: #f9fafb;
  border-radius: 0 8px 8px 0;
}
#__UID__ .stat .name { font-size: 13px; color: #6b7280; }
#__UID__ .stat .value { font-size: 1.1rem; font-weight: 600; color: #111827; }
#__UID__ .stat .z { font-size: 12px; color: #9ca3af; }
"""


def _new_uid(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def _style_tag(css: str, uid: str, extra: str = "") -> str:
    return f"<style>{extra}{css.replace('__UID__', uid)}</style>"


# ---------------------------------------------------------------------------
# 5. Titel
# ---------------------------------------------------------------------------
def render_title_html(
    title: str = "How Neurospicy are you?",
    subtitle: str = "Wo liegst du im Vergleich zu den Referenzgruppen?",
) -> str:
    uid = _new_uid("title")
    return f"""{_style_tag(_TITLE_CSS, uid, extra=_TITLE_FONT)}
<div id="{uid}">
  <h1><span class="grad">{title}</span> <span class="chili">🌶️</span></h1>
  <p class="sub">{subtitle}</p>
</div>"""


# ---------------------------------------------------------------------------
# 6. Bausteine der Verteilungsgrafik
# ---------------------------------------------------------------------------
class _Canvas:
    """Rechnet Datenwerte (Score, Dichte) in SVG-Pixel um."""

    PAD_LEFT, PAD_RIGHT, PAD_TOP, PAD_BOTTOM = 20, 20, 44, 30

    def __init__(self, x_min, x_max, y_max, width, height):
        self.x_min, self.x_max, self.y_max = x_min, x_max, y_max
        self.width, self.height = width, height
        self.plot_w = width - self.PAD_LEFT - self.PAD_RIGHT
        self.plot_h = height - self.PAD_TOP - self.PAD_BOTTOM
        self.base_y = self.sy(0)

    def sx(self, x: float) -> float:
        return self.PAD_LEFT + (x - self.x_min) / (self.x_max - self.x_min) * self.plot_w

    def sy(self, y: float) -> float:
        return self.PAD_TOP + self.plot_h - y / self.y_max * self.plot_h


def _make_canvas(user_mean, clinical: Group, norm: Group, width, height) -> _Canvas:
    """Wählt den x-Bereich so, dass beide Kurven und die Person sichtbar sind."""
    groups = (clinical, norm)
    x_min = max(0.0, min(min(g.mean - 3.5 * g.sd for g in groups), user_mean - 5))
    x_max = max(max(g.mean + 3.5 * g.sd for g in groups), user_mean + 5)
    y_max = max(_pdf(g.mean, g.mean, g.sd) for g in groups) * 1.15
    return _Canvas(x_min, x_max, y_max, width, height)


def _curve_paths(c: _Canvas, g: Group, n: int = 240):
    """SVG-Pfade für die Kurvenlinie und die gefüllte Fläche darunter."""
    points = []
    for i in range(n + 1):
        x = c.x_min + (c.x_max - c.x_min) * i / n
        points.append(f"{c.sx(x):.1f},{c.sy(_pdf(x, g.mean, g.sd)):.1f}")
    line = "M " + " L ".join(points)
    area = f"{line} L {c.sx(c.x_max):.1f},{c.base_y:.1f} L {c.sx(c.x_min):.1f},{c.base_y:.1f} Z"
    return line, area


def _ticks_svg(c: _Canvas) -> str:
    """Zahlen auf der x-Achse."""
    span = c.x_max - c.x_min
    step = 20 if span > 120 else 10 if span > 50 else 5
    parts = []
    t = math.ceil(c.x_min / step) * step
    while t <= c.x_max:
        parts.append(
            f'<text class="tick" x="{c.sx(t):.1f}" y="{c.base_y + 18:.1f}" text-anchor="middle">{t:g}</text>'
        )
        t += step
    return "".join(parts)


def _group_label_svg(c: _Canvas, g: Group, cls: str) -> str:
    """Name der Gruppe über dem Gipfel ihrer Kurve."""
    x = c.sx(g.mean)
    peak_y = c.sy(_pdf(g.mean, g.mean, g.sd))
    return f'<text class="lbl lbl-{cls}" x="{x:.1f}" y="{peak_y - 8:.1f}" text-anchor="middle">{g.name}</text>'


def _user_marker_svg(c: _Canvas, user_mean: float, clinical: Group, norm: Group) -> str:
    """Senkrechte Linie, Punkte auf beiden Kurven und Badge 'Du: …'."""
    ux = c.sx(user_mean)
    y_clin = c.sy(_pdf(user_mean, clinical.mean, clinical.sd))
    y_norm = c.sy(_pdf(user_mean, norm.mean, norm.sd))

    text = f"Du: {user_mean:g}"
    badge_w, badge_h, badge_y = 8 * len(text) + 20, 24, 4
    badge_x = min(max(ux - badge_w / 2, 2), c.width - badge_w - 2)

    return (
        f'<line class="user-line" x1="{ux:.1f}" y1="{badge_y + badge_h:.1f}" x2="{ux:.1f}" y2="{c.base_y:.1f}"/>'
        f'<circle class="user-dot dot-norm" cx="{ux:.1f}" cy="{y_norm:.1f}" r="5.5"/>'
        f'<circle class="user-dot dot-clin" cx="{ux:.1f}" cy="{y_clin:.1f}" r="5.5"/>'
        f'<rect class="user-badge" x="{badge_x:.1f}" y="{badge_y}" width="{badge_w}" height="{badge_h}" rx="12"/>'
        f'<text class="user-badge-text" x="{badge_x + badge_w / 2:.1f}" y="{badge_y + 16.5}" text-anchor="middle">{text}</text>'
    )


def _stats_html(user_mean: float, clinical: Group, norm: Group) -> str:
    """Zwei schlichte Zahlen: Anteil jeder Gruppe, der unter der Person liegt."""
    def stat(g: Group) -> str:
        p = _cdf(user_mean, g.mean, g.sd) * 100
        z = (user_mean - g.mean) / g.sd
        p_text = f"{p:.1f}" if (p < 1 or p > 99) else f"{p:.0f}"  # nie "0 %" oder "100 %"
        return f"""
  <div class="stat" style="--c-bar:{g.color}">
    <div class="name">{g.name} (M {g.mean:g}, SD {g.sd:g})</div>
    <div class="value">höher als {p_text}&nbsp;%</div>
    <div class="z">z = {z:+.2f}</div>
  </div>"""

    return f'<div class="stats">{stat(norm)}{stat(clinical)}</div>'


def _closer_group(user_mean: float, clinical: Group, norm: Group) -> Group:
    """Gruppe, deren Mittelwert (in Standardabweichungen) näher liegt."""
    z_clin = abs(user_mean - clinical.mean) / clinical.sd
    z_norm = abs(user_mean - norm.mean) / norm.sd
    return clinical if z_clin < z_norm else norm


# ---------------------------------------------------------------------------
# 7. Öffentliche Funktionen
# ---------------------------------------------------------------------------
def render_distribution_html(
    user_mean: float,
    clinical: Group,
    norm: Group,
    heading: str,
    width: int = 760,
    height: int = 300,
) -> str:
    """Zwei Normalverteilungen + klar markierter Wert der Person."""
    uid = _new_uid("dist")
    c = _make_canvas(user_mean, clinical, norm, width, height)
    clin_line, clin_area = _curve_paths(c, clinical)
    norm_line, norm_area = _curve_paths(c, norm)
    closer = _closer_group(user_mean, clinical, norm)

    svg = f"""
<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="{heading}: zwei Normalverteilungen, markierter Wert {user_mean:g}">
  <path class="area-norm" d="{norm_area}"/>
  <path class="area-clin" d="{clin_area}"/>
  <path class="line-norm" d="{norm_line}"/>
  <path class="line-clin" d="{clin_line}"/>
  <line class="baseline" x1="{c.PAD_LEFT}" y1="{c.base_y:.1f}" x2="{width - c.PAD_RIGHT}" y2="{c.base_y:.1f}"/>
  {_ticks_svg(c)}
  {_user_marker_svg(c, user_mean, clinical, norm)}
  {_group_label_svg(c, norm, "norm")}
  {_group_label_svg(c, clinical, "clin")}
</svg>"""

    return f"""{_style_tag(_CHART_CSS, uid)}
<div id="{uid}" style="--c-clin:{clinical.color}; --c-norm:{norm.color}; --c-hl:{closer.color};">
  <h2>{heading}</h2>
  <p class="result">Dein Wert {user_mean:g} liegt näher an der <span class="hl">{closer.name}</span></p>
  {svg}
  {_stats_html(user_mean, clinical, norm)}
</div>"""


def render_adhd_html(user_mean: float) -> str:
    return render_distribution_html(user_mean, ADHD, ADHD_NORM, heading="ADHS")


def render_autism_html(user_mean: float) -> str:
    return render_distribution_html(user_mean, AUTISM, AUTISM_NORM, heading="Autismus")


# ---------------------------------------------------------------------------
# Schnelltest: python neurospicy.py  ->  schreibt preview.html
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    page = render_title_html() + render_adhd_html(38) + render_autism_html(60)
    with open("preview.html", "w", encoding="utf-8") as f:
        f.write(
            "<!doctype html><meta charset='utf-8'>"
            "<body style='margin:0;padding:24px;background:#f9fafb;max-width:820px'>"
            f"{page}</body>"
        )
    print("preview.html geschrieben")