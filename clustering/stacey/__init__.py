import numpy as np
import pandas as pd
import tqdm
from . import cleaning
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import SnowballStemmer

stemmer = SnowballStemmer('english')

lemma = WordNetLemmatizer()
