from nltk.corpus.reader import wordnet
from nltk.corpus import stopwords
from nltk import pos_tag, word_tokenize, sent_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
import numpy as np
from .path import get_resource_file

stemmer = SnowballStemmer('english')
lemma = WordNetLemmatizer()


def get_us_names():
    csv_file = get_resource_file('us_names')
    with open(csv_file, 'r') as us_names:
        us_names = us_names.read()
        return us_names.split('\n')


def remove_stopwords(words, stopwords):
    if len(stopwords) > 0 and len(words) > 0:
        condition = np.where(np.isin(np.char.lower(words), stopwords))
        return np.delete(words, condition)
    return words


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def tag_stopwords(stopwords):
    return [stemmer.stem(lemma.lemmatize(pos[0], get_wordnet_pos(pos[1]))).lower()+"_"+get_wordnet_pos(pos[1])
            for sample, position in stopwords
            for idx, pos in enumerate(pos_tag(word_tokenize(sample)))
            if idx == position and get_wordnet_pos(pos[1]) not in [wordnet.ADJ, wordnet.ADV]]


def get_stopwords(extra=[], exception_words=[]):
    us_names = get_us_names()

    custom_stopwords = stopwords.words('english')
    custom_stopwords.extend(us_names)
    custom_stopwords.extend(extra)
    for word in exception_words:
        try:
            custom_stopwords.remove(word)
        except:
            pass
    custom_stopwords.sort()
    return custom_stopwords


def remove_stopwords(words, stopwords):
    if len(stopwords) > 0 and len(words) > 0:
        return np.delete(words, np.where(np.isin(np.char.lower(words), stopwords)))
    return words


def lemmatize(tagged_words, lowercase, min_len):

    for word, tag in tagged_words:
        if word.isalpha() and len(word) >= min_len:

            wordnet_pos = get_wordnet_pos(tag)

            if wordnet_pos == wordnet.ADJ or wordnet_pos == wordnet.ADV:
                continue

            lemmatized = lemma.lemmatize(word, wordnet_pos)

            if lowercase:
                lemmatized = lemmatized.lower()
            yield (lemmatized, wordnet_pos)


def tag_and_stem(corpus, lowercase=True, min_len=3, stopwords=[], tagged_stopwords=[]):
    sentences = sent_tokenize(corpus)
    tokens = [word for sent in sentences for word in word_tokenize(sent)]
    tokens = remove_stopwords(tokens, stopwords)
    pos_tags = pos_tag(tokens)
    tagged = [item for item in lemmatize(pos_tags, lowercase, min_len)]
    stemmed = [stemmer.stem(word)+'_'+pos for word,
               pos in tagged if word.isalpha()]
    stemmed = remove_stopwords(stemmed, tagged_stopwords)
    return ' '.join(stemmed)
