from pathlib import Path
from statistics import mean
import json

DATA_FILE = Path(__file__).parent / "full_database" / "data" / "responses.jsonl"

from statistics import NormalDist


responses = []


def reload_responses():
    responses.clear()
    if DATA_FILE.exists():
        responses.extend(
            json.loads(line)
            for line in DATA_FILE.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    return responses


reload_responses()
# take token as an arugment everywhere

def likert_to_number(likert_item):
    num = likert_item[0]
    try:
        return int(num)
    except TypeError as e:
        print(f"this doesn't have a proper likert format, first letter is {num}")
        return None

def calculate_average(list_of_vars, token="0dbf99c72f98247392b90464ec3eb13a90f8244d9610fef4817cbc1fe327fc91"):
    list_of_vars_int = []
    for var in list_of_vars:
        user_record = next(r for r in responses if r["token"] == token)
        answer = user_record["answers"][var]
        if isinstance(answer, str):
            num = likert_to_number(answer)
            if "_r_" in var:
                num = 6-num
            list_of_vars_int.append(num)
        else:
            list_of_vars_int.append(answer)
    # We ignore Nones:
    list_of_vars_int = [answer for answer in list_of_vars_int if answer is not None]

    return mean(list_of_vars_int)


def find_questions_end_with(var="_autism", token="0dbf99c72f98247392b90464ec3eb13a90f8244d9610fef4817cbc1fe327fc91"):
    user_record = next(r for r in responses if r["token"] == token)
    answer = user_record["answers"][var]
    return [var for var in answer.keys() if var.endswith(var)]




AUTISM_GROUP_MEAN = 74.95
AUTISM_GROUP_SD = 11.56

NORM_AUTISM_GROUP_MEAN = 38.72
NORM_AUTISM_GROUP_SD = 12.84

ADHD_GROUP_MEAN = 41.57
ADHD_GROUP_SD = 9.93

NORM_ADHD_GROUP_MEAN = 19.69
NORM_ADHD_GROUP_SD = 6.68



if __name__ == "__main__":
    print(calculate_average(["absorption1", "absorption2", "absorption3"]))
