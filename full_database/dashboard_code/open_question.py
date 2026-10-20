from colors import FARBEN_4_ABSTUFUNGEN
from config import STYLE
from HandleMeta import get_column_label


def give_text_html(color, farben, height_css):
    return f"""<style>
    .answer-card.accent-{color} {{
        background: #FFFFFF;
        border: 5px solid {farben['sehr_dunkel']};
        border-radius: 8px;
        padding: 0 2rem 1.75rem;
        font-family: "DM Sans", -apple-system, sans-serif;
        color: {farben['dunkel']};
        overflow-y: auto;
        {height_css}
    }}
    .answer-card.accent-{color} .section-title {{
        position: sticky;
        top: 0;
        background: #FFFFFF;
        padding: 1.75rem 0 0.75rem;
        margin-bottom: 1.25rem;
        border-bottom: 2px solid {farben['sehr_hell']};
        font-weight: 700;
        font-size: 1.1rem;
        color: {farben['sehr_dunkel']};
    }}
    .answer-card.accent-{color} .quote {{
        margin: 0 0 1.5rem;
        padding: 0.25rem 0 0.25rem 1.25rem;
        border-left: 4px solid {farben['basis']};
    }}
    .answer-card.accent-{color} .quote:last-child {{
        margin-bottom: 0;
    }}
    .answer-card.accent-{color} .quote p {{
        margin: 0 0 0.5rem;
        font-style: italic;
        line-height: 1.5;
        text-align: center;
    }}
    .answer-card.accent-{color} .quote p::before,
    .answer-card.accent-{color} .quote p::after {{
        font-size: 2em;
        font-weight: 700;
        font-style: normal;
        color: {farben['basis']};
        line-height: 0;
        vertical-align: -0.35em;
    }}
    .answer-card.accent-{color} .quote p::before {{ content: "“"; margin-right: 0.15em; }}
    .answer-card.accent-{color} .quote p::after  {{ content: "”"; margin-left: 0.15em; }}
    .answer-card.accent-{color} .answer-name {{
        font-weight: 700;
        color: {farben['sehr_dunkel']};
        margin-top: 0.5rem;
        text-align: right;
    }}
    .answer-card.accent-{color} .answer-name::before {{ content: "– "; }}
    </style>"""


def open_text(df, meta, area, text_column, name_colummn=None, number_of_answers=5, color="grün", height=None, random_seed=None):
    column_label = get_column_label(meta, text_column)
    
    farben = FARBEN_4_ABSTUFUNGEN[color]
    if height:
        height = str(height) + "px"

    answer_dict = {}
    if random_seed is not None:
        df = df.sample(frac=1, random_state=random_seed).reset_index(drop=True)
    
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
        content += '<blockquote class="quote">'
        for answer in answers:
            content += f'<p>{answer}</p>'
        content += f'<div class="answer-name">{name}</div>'
        content += '</blockquote>'

    area.html(
        give_text_html(color, farben, height_css)
        + f'<div class="answer-card accent-{color}">'
        f'<div class="section-title">{column_label}</div>'
        f'{content}'
        '</div>'
    )