import string
import re
import contractions
import tqdm
from langdetect import detect

filters = [
    {"regexp": r"(http[s]?:\/\/)?[^\s([\"<,>]*\.[^\s[\",><]+",
     "replace": ""},
    {"regexp": r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
     "replace": ""},
    {"regexp": r"([{][\s\S]+?[}])|([\[][\s\S]+?[\]])",
     "replace": ""},
    {"regexp": r"\b[\w]*[0-9=|_%+]+[\w]*\b", "replace": ""},
    {"regexp": r"[^.,';\w\s]|([\s][.,])|_", "replace": ""},
    {"regexp": r"[\n\r]", "replace": " "},
    {"regexp": r"\s{2,}", "replace": " "},
    {"regexp": r"\b(\w+)(?:\s+\1\b)+", "replace": r"\1"},
    {"regexp": r"[,]{2,}", "replace": ", "}
]


def is_english(text, ignore_errors=False):
    try:
        return detect(text) == 'en'
    except:
        if ignore_errors:
            return False
        else:
            print("Could not determine language for '{}'".format(text))
            raise()


def filter_english(series, ignore_errors=False):
    tqdm.tqdm.pandas()
    return series.progress_apply(lambda text: is_english(text, ignore_errors))


def clean(text, custom_filters=[]):
    if len(text) > 0:
        text = contractions.fix(text)
        reg_filters = custom_filters+filters
        for rule in reg_filters:
            text = re.sub(rule['regexp'], rule['replace'],
                          text, flags=re.IGNORECASE+re.MULTILINE)
        return text.strip()
