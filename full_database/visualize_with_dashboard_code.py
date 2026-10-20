# ============================================================
#  Marktforschungs-Dashboard v2 · Streamlit + Plotly
#  Enthält: Linie, Donut, Stacked Bar, Spider/Radar,
#           Heatmap, Bubble, Sankey, Balken, Zufriedenheit
#
#  Installation:  pip install streamlit plotly pandas
#  Starten:       streamlit run
# ============================================================

from dashboard_code.config import STYLE
import os
from pathlib import Path
import pyreadstat
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import numpy as np
from dashboard_code.colors import MULTIPLE_COLORS, CORE_COLOR, BACKGROUND
from dashboard_code.global_css import GLOBAL
from dashboard_code.header import header
import dashboard_code.helpers as h
from dashboard_code.KpiRenderer import KpiRenderer
import pickle
import plotly.express as px
from dashboard_code.single_barchart import create_barchart
from dashboard_code.stacked_barchart import create_stacked_bar
from dashboard_code.density_chart import create_density_plot
from dashboard_code.multi_stacked_barchart import create_multi_stacked_barchart
import dashboard_code.HandleMeta
from dashboard_code.HandleMeta import load_local_thing
from dashboard_code.config import WEIGHTING, DATA_TYPE
import altair as alt
from dashboard_code.pie_chart import create_piechart
from dashboard_code.big_number import big_number
from dashboard_code.footer import footer
import plotly.express as px
from dashboard_code.card_handler import CardHandler
from dashboard_code.crunch_label import give_crunch_label
from process_df import build_df
from process_meta import transform_to_meta, DONT_KNOW
import runpy
cards = CardHandler()

# Path

here = Path(__file__).parent
data_path = here / "data" / "responses.jsonl"
DATA_TYPE = "jsonl"

if DATA_TYPE == "jsonl":
    # additionally, define where the Questionnaire is:
    meta_path = here.parent / "frabo.py"
    PAGES = runpy.run_path(meta_path)["PAGES"]

@st.cache_data()
def load_data(changed):
    if DATA_TYPE == "sav":
        df, meta = pyreadstat.read_sav(str(data_path))
    elif DATA_TYPE == "jsonl":
        # Where is the finished data?
        df = build_df(path=data_path)
        # where is the Questionnaire?
        meta = transform_to_meta(frabo=PAGES)
        
    else:
        raise ValueError(f"Unknown DATA_TYPE: {DATA_TYPE}")

    return df, meta


df, meta = load_data(os.path.getmtime(data_path))

# define weighting and your environment in the config.py file



# ── SEITEN-KONFIGURATION ────────────────────────────────────
st.set_page_config(
    page_title="gfs-Dashboard",
    layout="wide",
)

# ── GLOBALES CSS ─────────────────────────────────────────────
st.markdown(GLOBAL, unsafe_allow_html=True)

st.markdown(h.set_background(hex_color=BACKGROUND[1]), unsafe_allow_html=True)

# ── HEADER ──────────────────────────────────────────────────
st.markdown(
    header(
        title="IS LISA AUTISTIC",
        image=here / "images" / "lisa.png",
        subtitle="A licences therapist has noticed that Lisa avoids eye contact, showed poor mentalizing by not explaining context. That Lisa enjoys data, coding and numbers. As well as shows repetitive fidgeting and unexpressive facial expressions. ADHD and Autism occur together. So. Is Lisa autistic?",
        year=2026,
        window="Autism-Dashboard",
    ),
    unsafe_allow_html=True)


# # ══════════════════════════════════════════════════════════
# #  KPI-KARTEN
# # ══════════════════════════════════════════════════════════
# kpi = KpiRenderer(df)
# kpi.render_section_title()

# k1, k2, k3, k4 = st.columns(4)

# # kpi.anzahl_befragte_mit_jahr(k1)

# kpi.render(k1, "Stichprobengrösse", "1019", "+5 % Gegenüber dem letzten Jahr", "up")
# kpi.render(k2, "Methode", "MIXED", "10% weniger CATI als letztes Jahr (50/50)", "down")
# kpi.bearbeitungszeit(k3, "überdurschnittliche Zeit", "up")
# kpi.render(k4, "Befragungszeitraum", "18 Tage", "von 3. - 21.  November", "down")

# st.divider()
# # ══════════════════
# # ══════════════════════════════════════════════════════════
# #  GFS1_1 · MITTELWERTE NACH JAHR
# # ══════════════════════════════════════════════════════════


# b1, b2 = st.columns([1.5, 2.5])

# with b1:
#     with st.container(key="karte2"):
#         h.set_subtle_title(st, "GFS1_1", "Mittelwerte nach Break")
#         st.subheader(dashboard_code.HandleMeta.get_column_label(meta, "GFS1_1"))

#         break_options = {
#             "Kein Break": "tz",
#             "Gemeinde": "gemeinde_gr_break",
#             "Bildung": "education_break",
#             "Alter": "alter_break",
#             "Geschlecht": "gender_break",
#             "HH-Einkommen": "einkommen_break_spez",
#             "Siedlungsart": "siedlungsart_break"
#         }

#         selected_break_label = st.selectbox(
#             "Break auswählen",
#             list(break_options.keys())
#         )
#         current_break = break_options[selected_break_label]

#         fig = create_barchart(df, meta, "GFS1_1", current_break, horizontal=False, color_gradient="categories", height=335)
#         st.plotly_chart(fig, use_container_width=True)
#         h.set_sample_size(st, col="GFS1_1", meta=meta, df=df)


# # ── PieChart ──────────────────────────────────────────────────

# b2_1, b2_2 = b2.columns([2, 1])

# with b2_2:
#     with st.container(key="karte5"):
#         h.set_subtle_title(st, "Stichprobenzusammensetzung", "Piechart")
#         # p2_1, p2_2, p2_3 = st.columns(3)
#         st.text("Geschlecht")
#         fig = create_piechart(df, meta, "gender_break", height=120)
#         st.plotly_chart(fig, use_container_width=True)
#         st.text("Bildung")
#         fig = create_piechart(df, meta, "education_break", height=120)
#         st.plotly_chart(fig, use_container_width=True)
#         st.text("Alter")
#         fig = create_piechart(df, meta, "alter_break", height=120)
#         st.plotly_chart(fig, use_container_width=True)


# # ── Another chart ──────────────────────────────────────────────────
a1, a2 = st.columns([1, 2.7])


big_number(a1, "Anzahl", "Diese Frage haben", f"{len(df)}", "... Personen, die Lisa kennen, beantwortet.", color="grün", add_percent=False, height=280)
big_number(a1, "lisa_autistic", "Davon glauben", f"{round(df["lisa_autistic"].eq(1).sum()/len(df)*100, 1)}", "... Dass eine Autismus-Spektrumsstörung vorliegt", color="rot", add_percent=True, height=280)

with a2:
    with st.container(key="karte2"):
        h.set_subtle_title(st, "lisa_autistic", "Pie Chart")
        st.subheader(dashboard_code.HandleMeta.get_column_label(meta, "lisa_autistic"))
        fig = create_piechart(df, meta, "lisa_autistic", height=440)
        st.plotly_chart(fig, use_container_width=True)


# big_number(b2_11, "GFS2_2", "Kommunikation der Gemeinde", "22", "... sind nicht oder überhaupt nicht zufrieden", color="grün", add_percent=True, height=280)
# big_number(b2_22, "GFS2_2", "Kommunikation der Gemeinde", "39", "... nutzen Social Media-Kanäle nicht", color="gelb", add_percent=True, height=280)




# # ── Big Number Card ──────────────────────────────────────────────────
# n2_1, n2_2 = b2.columns([1, 1])


# # ── Stacked Bar Chart ──────────────────────────────────────────────────


# with b2_1.container(key="karte6"):
#     h.set_subtle_title(st, "GFS2_1", "Stacked Barchart")
#     st.subheader(dashboard_code.HandleMeta.get_column_label(meta, "GFS2_1"))
#     fig = create_stacked_bar(df, meta, "GFS2_1", height=140)
#     st.plotly_chart(fig, use_container_width=True)
#     h.set_sample_size(st, col="GFS2_1", meta=meta, df=df)

# # ──  Bar With Slider ──────────────────────────────────────────────────


# h1, h2 = st.columns([1, 1])

# with h1.container(key="karte8"):
#     h.set_subtle_title(st, "GFS2_3", "Stacked Barchart")
#     st.subheader(dashboard_code.HandleMeta.get_column_label(meta, "GFS2_3"))
#     min_age, max_age = st.slider(
#         "Gemeindegrösse wählen",
#         min_value=int(df["gemeinde_gr_break"].min()),
#         max_value=int(df["gemeinde_gr_break"].max()),
#         value=(int(df["gemeinde_gr_break"].min()), int(df["gemeinde_gr_break"].max())),
#         step=1,
#         help="Nur Personen in diesee Gemeindegrösse werden angezeigt"
#     )

#     filtered_df = df[
#         (df["gemeinde_gr_break"] >= min_age) &
#         (df["gemeinde_gr_break"] <= max_age)
#     ].reset_index(drop=True)

#     fig = create_barchart(filtered_df, meta, "GFS2_3", current_break=None, horizontal=True, color="grün", height=220, crunch_label_by=10)
#     st.plotly_chart(fig, use_container_width=True)
#     fig = create_density_plot(filtered_df, meta, "GFS2_3", color="grün", height=220, smoothness=0.66)
#     st.plotly_chart(fig, use_container_width=True)
#     h.set_sample_size(st, col="GFS2_3", meta=meta, df=filtered_df)


# # ──  Bar With Slider ──────────────────────────────────────────────────


# with h2.container(key="karte10"):
#     h.set_subtle_title(st, "GFS2", "Different Charts")
#     st.subheader("Falls Sie die folgenden Kommunikationskanäle Ihrer Gemeinde bzw. Stadt nutzen: Wie zufrieden sind Sie damit?")
#     tab1, tab2, tab3, tab4 = st.tabs(["Webseite", "Social Media-Kanäle", "Mitteilungsblatt/Gemeindeblatt", "Newsletter per E-Mail"])
#     with tab1:
#         st.subheader("Webseite der Gemeinde/Stadt")
#         fig = create_barchart(df, meta, "GFS2_1", color_gradient="categories", height=453, crunch_label_by=10)
#         st.plotly_chart(fig, use_container_width=True)

#     with tab2:
#         st.subheader("Social Media-Kanäle der Gemeinde/Stadt")
#         fig = create_barchart(df, meta, "GFS2_2", color_gradient="categories", height=453, crunch_label_by=11)
#         st.plotly_chart(fig, use_container_width=True)

#     with tab3:
#         st.subheader("Mitteilungsblatt/Gemeindeblatt")
#         fig = create_barchart(df, meta, "GFS2_3", color_gradient="categories", height=453, crunch_label_by=12)
#         st.plotly_chart(fig, use_container_width=True)

#     with tab4:
#         st.subheader("Newsletter per E-Mail")
#         fig = create_barchart(df, meta, "GFS2_4", color_gradient="categories", height=453, crunch_label_by=13)
#         st.plotly_chart(fig, use_container_width=True)

#     h.set_sample_size(st, col="GFS2_4", meta=meta, df=df)
    


# # ── New Multis ──────────────────────────────────────────────────

# x1, x2, = st.columns([2, 1])
# with x1:
#     with st.container(key="karte16"):
#         h.set_subtle_title(st, "GFS2", "Different Charts")
#         group_label = h.extract_group_label(df, meta, ["GFS2_1", "GFS2_2", "GFS2_3", "GFS2_4"])
#         st.subheader(group_label)
#         fig = create_multi_stacked_barchart(
#             df, meta,
#             ["GFS2_1", "GFS2_2", "GFS2_3", "GFS2_4"],
#             height=300,
#             crunch_label_by=13,
#             crunch_item_label_by = 12,
#             group_label=group_label,
#             farben_umkehren=False
#         )
#         st.plotly_chart(fig, use_container_width=True)


# # ── FOOTER ──────────────────────────────────────────────────

# st.divider()

# st.html(footer(
#     logos=["gfs.png", "uni.png", "kmu.png"]
# ))
# st.caption("gfs-Demo-Dashboard · Daten nicht akkurat · Erstellt von Lisa Gehrig · 22.04.2026")
