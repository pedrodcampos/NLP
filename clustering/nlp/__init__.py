import numpy as np

from . import cleaning
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import SnowballStemmer

stemmer = SnowballStemmer('english')

lemma = WordNetLemmatizer()
