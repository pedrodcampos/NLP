from nltk.corpus.reader import wordnet
from nltk.corpus import stopwords
import pandas as pd
from ..helpers import get_resource_path


def get_us_names():
    csv_file = get_resource_path('us_names')
    df_names = pd.read_csv(csv_file, header=None)
    return df_names[0].tolist()


def get_stopwords(extra=[], exception_words=[]):
    us_names = get_us_names()

    en_stopwords = stopwords.words('english')
    en_stopwords.extend(us_names)
    en_stopwords.extend(extra)
    en_stopwords = remove_stopwords(en_stopwords, exception_words)
    en_stopwords.sort()
    return en_stopwords


def remove_stopwords(words, stopwords):
    if len(stopwords) > 0 and len(words) > 0:
        condition = np.where(np.isin(np.char.lower(words), stopwords))
        return np.delete(words, condition)
    return words
