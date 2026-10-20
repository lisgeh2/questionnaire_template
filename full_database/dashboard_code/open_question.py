from colors import FARBEN_4_ABSTUFUNGEN
from config import STYLE


def give_text_html(color, farben, height_css):
    return f"""<style>
    .answer-card.accent-{color} {{
        background: #FFFFFF;
        border: 5px solid {farben['sehr_dunkel']};
        border-radius: 8px;
        padding: 1.75rem 2rem;
        font-family: "DM Sans", -apple-system, sans-serif;
        color: {farben['dunkel']};
        overflow-y: auto;
        {height_css}
    }}
    .answer-card.accent-{color} .answer-name {{
        font-weight: 700;
        color: {farben['sehr_dunkel']};
        margin-top: 1rem;
    }}
    </style>"""


def open_text(meta, df, area, text_column, name_colummn=None, number_of_answers=5, color="grün", height=None):
    farben = FARBEN_4_ABSTUFUNGEN[color]
    if height:
        height = str(height) + "px"

    answer_dict = {}
    for index, row in df.iloc[-number_of_answers:].iloc[::-1].iterrows():
        if name_colummn != None:
            if row[name_colummn] not in answer_dict:
                answer_dict[row[name_colummn]] = {row[text_column]}
            else:
                answer_dict[row[name_colummn]].add(row[text_column])
        else:
            if "(anonymous)" not in answer_dict:
                answer_dict["(anonymous)"] = {row[text_column]}
            else:
                answer_dict["(anonymous)"].add(row[text_column])

    height_css = f"height: {height};" if height else ""

    content = ""
    for name, answers in answer_dict.items():
        content += f'<div class="answer-name">{name}</div>'
        for answer in answers:
            content += f'<p>{answer}</p>'

    area.html(
        give_text_html(color, farben, height_css)
        + f'<div class="answer-card accent-{color}">'
        f'<div class="section-title">{text_column}</div>'
        f'{content}'
        '</div>'
    )