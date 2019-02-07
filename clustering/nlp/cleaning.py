import string
import re
import contractions
from langdetect import detect

filters = [
    {"regexp": r"(wrote:)|(from:([\w\s\n.\t]*?)subject:)|(re:)",
     "replace": ""},
    {"regexp": r"(www|https?:)+[^\s]+[\w]", "replace": ""},
    {"regexp": r"[\w]+([.]\w)?@([\w].[\w])+(.[\w]+)+", "replace": ""},
    {"regexp": r"((on|)\s?[\w]{3}\,\s[\w]{3}\s(0[1-9]|(1|2)[0-9]|3[0-1])\,\s([0-9]{4})(\,|\s|)(at|)\s([0-1][0-9]|2[0-4]|[0-9]):[0-5][0-9])\s?(am|pm|)", "replace": ""},
    {"regexp": r"([\{\[]|---|[%])+([\w\s\n.\t]*?)([\}\]]|---|[%])+",
     "replace": ""},
    {"regexp": r"\b[\w]*[0-9=|_%]+[\w]*\b", "replace": ""},
    {"regexp": r"[^.,;\w\s]|([\s][.,])|_", "replace": ""},
    {"regexp": r"CONFIDENTIALITY\sNOTICE([\w\s\n.,])*", "replace": ""},
    {"regexp": r"(\xa0)", "replace": " "},
    {"regexp": r"\s{2,}", "replace": " "}]


def is_english(text, ignore_errors=False):
    try:
        return detect(text) == 'en'
    except:
        if ignore_errors:
            return False
        else:
            print("Could not determine language for '{}'".format(text))
            raise()


def clean(text, custom_filters=[]):
    if len(text) > 0:
        text = contractions.fix(text)
        custom_filters.extend(filters)
        for rule in custom_filters:
            text = re.sub(rule['regexp'], rule['replace'],
                          text, flags=re.IGNORECASE)
        return text.strip()
