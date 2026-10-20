"""The questionnaire itself.

Everything the survey asks lives here, so you can change the elements without
touching any Streamlit code.

A question is a dict with:
    key      unique id -- also the field name in the saved answers
    label    the text shown to the user
    type     "text" | "textarea" | "radio" | "multiselect" | "slider"
    options  list of choices          (radio / multiselect only)
    min/max  bounds                   (slider only)
    default  starting position        (slider only, defaults to `min`)
    required whether it must be filled in (default: True)
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from frabo import PAGES



DISPLAY_TYPES = {"image", "video", "markdown", "divider"}

def is_input(element) -> bool:
    return element["type"] not in DISPLAY_TYPES


def all_elements():
    return [element for page in PAGES for element in page["elements"]]


def input_elements():
    return [element for element in all_elements() if is_input(element)]


def element_keys():
    return [element["key"] for element in input_elements()]

########### EXPORT the Pages, so we can later use a DF and a dict


# {key: {type: "radion, label: "why?", item_labels: {1: "1=bc",, 2: "2=bc"}}}

DONT_KNOW = 99999997
DONT_KNOW_LABELS = {"i dont know", "dont know", "i don't know", "don't know"}

import re

ANCHOR_RE = re.compile(r"(\d+)\s*=\s*([^,.)]+)")
ANCHOR_PAREN_RE = re.compile(r"\s*\([^()]*\d+\s*=[^()]*\)")


def anchors_from_label(label):
    return {int(num): text.strip() for num, text in ANCHOR_RE.findall(label)}


def strip_anchors(label):
    cleaned = ANCHOR_PAREN_RE.sub("", label)
    cleaned = re.sub(r"([?!:])\s*\.", r"\1", cleaned)   # "?. Try" -> "? Try"
    return re.sub(r"\s{2,}", " ", cleaned).strip()

def transform_to_meta(frabo=PAGES):
    meta = {}
    for page in frabo:
        for element in page["elements"]:
            if not is_input(element):
                continue
            entry = {
                "type": element["type"],
                "label": element["label"],
            }
            
            if element["type"] == "radio":
                item_labels = {}
                i = 1
                for opt in element["options"]:
                    if opt.strip().lower() in DONT_KNOW_LABELS:
                        item_labels[DONT_KNOW] = opt
                    else:
                        item_labels[i] = opt
                        i += 1
                entry["item_labels"] = item_labels

            
            elif element["type"] == "slider":
                minimum = element["min"]
                maximum = element["max"]
                if maximum < 15:
                    labels = {i: str(i) for i in range(minimum, maximum + 1)}
                    for num, text in anchors_from_label(element["label"]).items():
                        if num in labels:
                            labels[num] = f"{num}={text}"
                    entry["item_labels"] = labels
                    entry["label"] = strip_anchors(element["label"])
                else:
                    entry["item_labels"] = {}
                
            
            
            elif element["type"] == "textarea":
                entry["item_labels"] = {}
                
            meta[element["key"]] = entry
    
    meta["tz"] = {
        "type": "hidden",
        "label": "Timezone",
        "item_labels": {1: "1"},
    }
    
    return meta


if __name__ == "__main__":
    print(transform_to_meta())

