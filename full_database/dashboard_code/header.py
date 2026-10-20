from html import escape
from colors import MULTIPLE_COLORS, CORE_COLOR, FARBEN_4_ABSTUFUNGEN
import base64
from config import STYLE

def give_subtitle_block(subtitle):
  if STYLE == "gfs":
    return f"""
    <div style="
      font-size: 0.80rem;
      letter-spacing: 0.08em;
      color: #7a7269;
      margin-bottom: 6px;
      font-weight: 600;
    "><br>
      {subtitle}
    </div>
    """
  if STYLE == "cool_black":
    return f"""
    <div style="
      font-size: 0.86rem;
      letter-spacing: 0.02em;
      color: rgba(234, 240, 255, 0.50);
      margin-top: 14px;
      margin-bottom: 0;
      font-weight: 400;
      max-width: 58ch;
      line-height: 1.5;
    ">
      {subtitle}
    </div>
    """
  if STYLE == "leavy":
    return f"""
    <div style="
      font-family: 'EB Garamond', Georgia, serif;
      font-size: 1.02rem;
      font-style: italic;
      letter-spacing: 0.01em;
      color: {FARBEN_4_ABSTUFUNGEN["grün"]["dunkel"]};
      margin-top: 14px;
      margin-bottom: 0;
      font-weight: 400;
      max-width: 56ch;
      line-height: 1.5;
    ">
      {subtitle}
    </div>
    """
  if STYLE == "comic_brutalist":
    return f"""
    <div style="
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.74rem;
      letter-spacing: 0.04em;
      line-height: 1.6;
      color: #14161a;
      opacity: 0.78;
      margin-top: 16px;
      margin-bottom: 0;
      max-width: 46ch;
      border-left: 4px solid {MULTIPLE_COLORS[0]};
      padding-left: 12px;
    ">
      {subtitle}
    </div>
    """
  if STYLE == "black_white":
    return f"""
    <div style="
      font-family: 'Inter', Helvetica, sans-serif;
      font-size: 0.72rem;
      font-weight: 400;
      letter-spacing: 0.02em;
      line-height: 1.5;
      color: #f2f0ec;
      margin-top: 0;
      margin-bottom: 0;
      max-width: 30ch;
    ">
      {subtitle}
    </div>
    """

def give_header_css(window, year, title, subtitle_block, image_b64):
  if STYLE == "gfs":
    return f"""
      <div style="
      background: #ffffff;
      border: 0px solid {FARBEN_4_ABSTUFUNGEN["blau"]["sehr_dunkel"]};
      border-radius: 2px;
      padding: 34px 56px 28px 56px;
      margin-bottom: 22px;
      box-shadow: 0 10px 30px rgba(80, 60, 40, 0.20);
      ">

      <!-- Horizontale Zeile: Text links, Logo rechts -->
      <div style="
      display: flex;
      flex-direction: row;
      align-items: center;
      gap: 20px;
      ">

      <!-- Linke Spalte: Badge + Titel + Subtitle -->
      <div style="
      flex: 1 1 auto;
      min-width: 0;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      ">

      <div style="
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: {CORE_COLOR[0]};
      background: {CORE_COLOR[9]};
      padding: 7px 12px;
      border-radius: 999px;
      margin-bottom: 14px;
      width: fit-content;
      ">
      <span>{window}</span>
      <span style="opacity: 0.45;">•</span>
      <span>Schweiz {year}</span>
      </div>

      <div style="
      font-size: 2.5rem;
      font-weight: 700;
      color: {MULTIPLE_COLORS[5]};
      line-height: 1.08;
      letter-spacing: 0.02em;
      margin: 0;
      ">
      {title}
      </div>

      {subtitle_block}

      </div>

      <!-- Rechte Spalte: Logo -->
      <div style="
      flex: 0 0 auto;
      display: flex;
      align-items: center;
      ">
      <img src="data:image/png;base64,{image_b64}" alt="GFS" style="
      max-height: 110px;
      width: auto;
      display: block;
      object-fit: contain;
      border-radius: 12px;
      ">
      </div>
      </div>
      """

  if STYLE == "cool_black":
    return f"""
      <div style="
      background: transparent;
      border: none;
      border-bottom: 1px solid rgba(234, 240, 255, 0.12);
      padding: 8px 0 30px 0;
      margin-bottom: 30px;
      position: relative;
      ">

      <!-- Glow hinter dem Titel -->
      <div style="
      position: absolute;
      top: -40px; left: -60px;
      width: 420px; height: 220px;
      background: radial-gradient(closest-side, {CORE_COLOR[0]}, transparent);
      opacity: 0.13;
      filter: blur(40px);
      pointer-events: none;
      "></div>

      <!-- Horizontale Zeile: Text links, Logo rechts -->
      <div style="
      display: flex;
      flex-direction: row;
      align-items: center;
      gap: 20px;
      position: relative;
      ">

      <!-- Linke Spalte: Badge + Titel + Subtitle -->
      <div style="
      flex: 1 1 auto;
      min-width: 0;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      ">

      <div style="
      display: inline-flex;
      align-items: center;
      gap: 10px;
      font-size: 0.66rem;
      font-weight: 700;
      letter-spacing: 0.22em;
      text-transform: uppercase;
      color: {CORE_COLOR[0]};
      background: {CORE_COLOR[9]};
      border: 1px solid {CORE_COLOR[7]};
      padding: 6px 14px;
      border-radius: 999px;
      margin-bottom: 18px;
      width: fit-content;
      box-shadow: 0 0 24px {CORE_COLOR[8]};
      ">
      <span>{window}</span>
      <span style="opacity: 0.45;">/</span>
      <span>Schweiz {year}</span>
      </div>

      <div style="
      font-family: 'Archivo', 'Inter', sans-serif;
      font-variation-settings: 'wdth' 112;
      font-size: 4.2rem;
      font-weight: 800;
      line-height: 0.94;
      letter-spacing: -0.03em;
      margin: 0;
      text-transform: uppercase;
      background: linear-gradient(100deg,
                  {MULTIPLE_COLORS[5]} 0%,
                  {MULTIPLE_COLORS[5]} 38%,
                  {MULTIPLE_COLORS[0]} 78%,
                  {MULTIPLE_COLORS[4]} 100%);
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
      color: {MULTIPLE_COLORS[5]};
      ">
      {title}
      </div>

      {subtitle_block}

      </div>

      <!-- Rechte Spalte: Logo -->
      <div style="
      flex: 0 0 auto;
      display: flex;
      align-items: center;
      ">
      <img src="data:image/png;base64,{image_b64}" alt="GFS" style="
      max-height: 90px;
      width: auto;
      display: block;
      object-fit: contain;
      filter: brightness(0) invert(1);
      opacity: 0.85;
      ">
      </div>
      </div>
      </div>
      """

  if STYLE == "leavy":
    return f"""
      <div style="
      background: #fdfaf3;
      border: 1px solid {FARBEN_4_ABSTUFUNGEN["grün"]["basis"]};
      border-radius: 0;
      padding: 40px 56px 34px 56px;
      margin-bottom: 26px;
      position: relative;
      box-shadow: inset 0 0 0 1px #fdfaf3,
                  inset 0 0 0 5px {FARBEN_4_ABSTUFUNGEN["grün"]["basis"]},
                  0 2px 4px rgba(34, 32, 27, 0.10);
      ">

      <!-- Zierkreis, wie ein Siegel -->
      <div style="
      position: absolute;
      top: 50%; left: 50%;
      width: 300px; height: 300px;
      margin: -150px 0 0 -150px;
      border: 1px solid {FARBEN_4_ABSTUFUNGEN["grün"]["basis"]};
      border-radius: 50%;
      opacity: 0.07;
      pointer-events: none;
      "></div>

      <!-- Horizontale Zeile: Text links, Logo rechts -->
      <div style="
      display: flex;
      flex-direction: row;
      align-items: center;
      gap: 20px;
      position: relative;
      ">

      <!-- Linke Spalte: Badge + Titel + Subtitle -->
      <div style="
      flex: 1 1 auto;
      min-width: 0;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      ">

      <div style="
      display: inline-flex;
      align-items: center;
      gap: 10px;
      font-family: 'EB Garamond', Georgia, serif;
      font-size: 0.70rem;
      font-weight: 600;
      letter-spacing: 0.28em;
      text-transform: uppercase;
      color: {CORE_COLOR[0]};
      background: transparent;
      border-top: 1px solid {CORE_COLOR[7]};
      border-bottom: 1px solid {CORE_COLOR[7]};
      padding: 7px 2px;
      border-radius: 0;
      margin-bottom: 18px;
      width: fit-content;
      ">
      <span>{window}</span>
      <span style="opacity: 0.5;">&#10022;</span>
      <span>Schweiz {year}</span>
      </div>

      <div style="
      font-family: 'Playfair Display', 'EB Garamond', Georgia, serif;
      font-size: 3.4rem;
      font-weight: 700;
      color: {MULTIPLE_COLORS[5]};
      line-height: 1.06;
      letter-spacing: -0.01em;
      margin: 0;
      ">
      {title}
      </div>

      <div style="
      width: 74px;
      height: 1px;
      background: {CORE_COLOR[0]};
      margin-top: 16px;
      opacity: 0.6;
      "></div>

      {subtitle_block}

      </div>

      <!-- Rechte Spalte: Logo -->
      <div style="
      flex: 0 0 auto;
      display: flex;
      align-items: center;
      ">
      <img src="data:image/png;base64,{image_b64}" alt="GFS" style="
      max-height: 104px;
      width: auto;
      display: block;
      object-fit: contain;
      opacity: 0.9;
      ">
      </div>
      </div>
      </div>
      """

  if STYLE == "comic_brutalist":
    return f"""
      <div style="
      background: #f4f1e8;
      border: 5px solid #14161a;
      border-radius: 0;
      padding: 0;
      margin-bottom: 26px;
      position: relative;
      overflow: hidden;
      box-shadow: 12px 12px 0 0 {MULTIPLE_COLORS[1]},
                  12px 12px 0 5px #14161a;
      ">

      <!-- Halbtonfeld hinter dem Titel -->
      <div style="
      position: absolute;
      left: 0; top: 0;
      width: 38%; height: 100%;
      background-image: radial-gradient(#14161a 1.6px, transparent 1.7px);
      background-size: 10px 10px;
      opacity: 0.13;
      pointer-events: none;
      "></div>

      <!-- Technischer Streifen an der Oberkante -->
      <div style="
      display: flex;
      align-items: stretch;
      border-bottom: 5px solid #14161a;
      position: relative;
      ">
      <div style="
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.66rem;
      font-weight: 700;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: #f4f1e8;
      background: {MULTIPLE_COLORS[1]};
      padding: 9px 16px;
      border-right: 5px solid #14161a;
      white-space: nowrap;
      ">{window}</div>
      <div style="
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.66rem;
      font-weight: 700;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: #14161a;
      padding: 9px 16px;
      opacity: 0.65;
      ">/// Schweiz {year} ///</div>
      <div style="
      margin-left: auto;
      background: {MULTIPLE_COLORS[2]};
      border-left: 5px solid #14161a;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.66rem;
      font-weight: 700;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: #14161a;
      padding: 9px 16px;
      white-space: nowrap;
      ">System Status &#9632; Live</div>
      </div>

      <!-- Hauptzeile: Titel links, Logo rechts -->
      <div style="
      display: flex;
      flex-direction: row;
      align-items: stretch;
      gap: 0;
      position: relative;
      ">

      <div style="
      flex: 1 1 auto;
      min-width: 0;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      justify-content: center;
      padding: 26px 28px 30px 28px;
      ">

      <div style="
      font-family: 'Anton', 'Archivo', Impact, sans-serif;
      font-size: 5.2rem;
      font-weight: 400;
      color: {MULTIPLE_COLORS[5]};
      line-height: 0.84;
      letter-spacing: -0.015em;
      text-transform: uppercase;
      margin: 0;
      text-shadow: 5px 5px 0 {MULTIPLE_COLORS[0]}33;
      ">
      {title}
      </div>

      {subtitle_block}

      </div>

      <!-- Logo in einem eigenen Kasten -->
      <div style="
      flex: 0 0 auto;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 22px 26px;
      border-left: 5px solid #14161a;
      background: #ece8dc;
      ">
      <img src="data:image/png;base64,{image_b64}" alt="GFS" style="
      max-height: 96px;
      width: auto;
      display: block;
      object-fit: contain;
      ">
      </div>
      </div>
      </div>
      """

  if STYLE == "black_white":
    return f"""
      <div style="
      background: #111111;
      border: none;
      border-radius: 0;
      padding: 0;
      margin-bottom: 26px;
      position: relative;
      overflow: hidden;
      font-family: 'Archivo Black', 'Archivo', Helvetica, sans-serif;
      ">

      <!-- Schwarze Flaeche als Form. Sie wird angeschnitten, der Text nie. -->
      <div style="
      position: absolute;
      right: -6%; top: -40%;
      width: 30%; height: 190%;
      background: #f2f0ec;
      transform: rotate(14deg);
      pointer-events: none;
      "></div>

      <!-- Titel: gross und gestreckt, aber vollstaendig. Umbruch statt Schnitt. -->
      <div style="
      position: relative;
      padding: 30px 0 0 24px;
      ">
      <div style="
      font-family: 'Archivo Black', Helvetica, sans-serif;
      font-size: 4.3rem;
      font-weight: 400;
      color: {MULTIPLE_COLORS[5]};
      line-height: 0.88;
      letter-spacing: -0.045em;
      text-transform: uppercase;
      margin: 0 0 0 -0.04em;
      transform: scaleY(1.12);
      transform-origin: left top;
      max-width: 62%;
      overflow-wrap: break-word;
      ">
      {title}
      </div>
      </div>

      <!-- Fusszeile: winzige Captions gegen die Riesentype -->
      <div style="
      position: relative;
      display: flex;
      align-items: flex-end;
      gap: 28px;
      padding: 40px 24px 20px 24px;
      ">

      <div style="
      font-family: 'Inter', Helvetica, sans-serif;
      font-size: 0.58rem;
      font-weight: 500;
      letter-spacing: 0.26em;
      line-height: 1.7;
      text-transform: uppercase;
      color: #f2f0ec;
      border-top: 1px solid rgba(242, 240, 236, 0.28);
      padding-top: 9px;
      white-space: nowrap;
      ">{window}<br>Schweiz {year}</div>

      {subtitle_block}

      <div style="
      margin-left: auto;
      display: flex;
      align-items: flex-end;
      gap: 18px;
      flex: 0 0 auto;
      ">
      <div style="
      font-family: 'Archivo Black', Helvetica, sans-serif;
      font-size: 3rem;
      line-height: 0.85;
      letter-spacing: -0.04em;
      color: #111111;
      transform: scaleY(1.14);
      transform-origin: right bottom;
      ">{year}</div>
      <img src="data:image/png;base64,{image_b64}" alt="GFS" style="
      max-height: 62px;
      width: auto;
      display: block;
      object-fit: contain;
      filter: brightness(0) invert(1);
      ">
      </div>
      </div>
      </div>
      """

def header(title=None, subtitle=None, year=None, window=None, image="gfs.png"):
    title = escape(title or "Untitled Dashboard")
    subtitle = escape(subtitle or "")
    year = escape(str(year or "2026"))
    window = escape(window or "Marktforschung")
    
    


    with open(image, "rb") as f:
       
      image_b64 = base64.b64encode(f.read()).decode("utf-8")
    
    if subtitle:
      subtitle_block = give_subtitle_block(subtitle)
    else:
      subtitle_block=""

    return give_header_css(window, year, title, subtitle_block, image_b64)