import pyreadstat
import pickle
from contextlib import contextmanager
import sys
from pathlib import Path
from config import DATA_TYPE
from os.path import commonprefix

HERE = Path(__file__).parent

def load_local_thing(path="MetaTable.pkl"):
    full_path = HERE / path   # always resolves next to the script

    @contextmanager
    def _temp_syspath(p):
        p = str(p)
        sys.path.insert(0, p)
        try:
            yield
        finally:
            sys.path.remove(p)

    _functions_parent = Path(__file__).parents[6]

    with _temp_syspath(_functions_parent):
        if str(full_path).endswith(".pkl"):
            with open(full_path, "rb") as f:
                return pickle.load(f)
        elif str(full_path).endswith(".sav"):
            return pyreadstat.read_sav(str(full_path))
        else:
            raise ValueError(f"Unsupported file type: {path}")


def get_value_labels(meta, variable_name):
    if DATA_TYPE == "metatable":
        metatable = load_local_thing(path="MetaTable.pkl")
        return metatable.columns[variable_name].item_value_labels

    if variable_name is None:
        return {}

    elif DATA_TYPE == "sav":
        value_labels = meta.variable_value_labels       # <-- fixed
        return value_labels.get(variable_name, {})      # <-- safe default
    elif DATA_TYPE == "jsonl":
        return meta[variable_name]["item_labels"]


def get_column_label(meta, variable_name):
    if DATA_TYPE == "metatable":
        metatable = load_local_thing(path="MetaTable.pkl")
        return metatable.columns[variable_name].label

    if variable_name is None:
        return {}
    
    elif DATA_TYPE == "sav":
        col_labels = meta.column_names_to_labels        # <-- fixed
        return col_labels.get(variable_name, variable_name)  # fall back to var name
    
    elif DATA_TYPE == "jsonl":
        return meta[variable_name]["label"]

def get_group_label_and_single_label(meta, group_col_list):
    if DATA_TYPE == "metatable":
        metatable = load_local_thing(path="MetaTable.pkl")
        # sth like:
        label_dict = {col: get_column_label(meta, col) for col in group_col_list}
        group = metatable.columns[group_col_list[0]].group
        group_label = metatable.groups[group].value_label

        single_labels_dict = {}
        for col, label in label_dict.items():
            single_label = label.replace(group_label, "")
            single_labels_dict[col] = single_label

        return group_label, single_labels_dict


    elif DATA_TYPE == "sav" or DATA_TYPE == "jsonl":
        label_dict = {col: get_column_label(meta, col) for col in group_col_list}
        group_label = commonprefix(list(label_dict.values()))

        single_labels_dict = {}
        for col, label in label_dict.items():
            single_label = label.replace(group_label, "")
            single_labels_dict[col] = single_label

        return group_label, single_labels_dict