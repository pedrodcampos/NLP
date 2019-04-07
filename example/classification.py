
# %%
from sklearn import metrics
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag

import contractions
from string import punctuation


# %%
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
stop_words = stopwords.words('english')
stop_punctuation = [p for p in punctuation]
stoppers = stop_words+stop_punctuation
stoppers.remove('not')


def clean_and_tokenize(txt):
    def get_wordnet_pos(tag):
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}

        return tag_dict.get(tag[0], wordnet.NOUN)

    sentences = sent_tokenize(txt)
    cleaned_txt = []
    for sentence in sentences:
        expanded_sentences = contractions.fix(sentence)
        tokens = [token for token in word_tokenize(expanded_sentences)]
        tagged_tokens = pos_tag(tokens)
        for token, tag in tagged_tokens:
            if len(token) > 2:
                lemma_word = lemmatizer.lemmatize(token, get_wordnet_pos(tag))
                if lemma_word not in stoppers:
                    stemmed_word = stemmer.stem(lemma_word)
                    cleaned_txt.append(stemmed_word)
    return " ".join(cleaned_txt)


# %%
training_data = np.array([['a dog barks', 'dog'],
                          ['dogs are friendly animals', 'dog'],
                          ['her pet won\'t stop barking', 'dog'],
                          ['bob is waggling his tail', 'dog'],
                          ['her dog rarely barks', 'dog'],
                          ['my dog barks', 'dog'],
                          ['cats are anti-social animals', 'cat'],
                          ['a cat snores', 'cat'],
                          ['my pet sleeps all day long', 'cat'],
                          ['his pet is not really social', 'cat'],
                          ['tom snores a lot', 'cat'],
                          ['her cat barks', 'cat']
                          ])


# %%
stoppers = stoppers + ['pet', 'bob', 'tom']


# %%
stemmed_txt = [clean_and_tokenize(text) for text in training_data[:, 0]]


# %%
tfidf = TfidfVectorizer(analyzer="word",
                        sublinear_tf=True,
                        use_idf=True,
                        norm='l2',
                        ngram_range=(1, 2))

features = tfidf.fit_transform(stemmed_txt).toarray()


# %%
labels = training_data[:, 1]


# %%
print(f"Total words in dictionary:{len(tfidf.vocabulary_)}")
print(f"Top 10 most frequent words:")
top_10 = sorted(tfidf.vocabulary_, key=lambda x: x[1], reverse=True)[:10]
print("\t> "+"\n\t> ".join(top_10))


# %%
clf = RandomForestClassifier()
clf.fit(features, labels)


# %%
test_data = np.array([
    ['Max always waggles his tail when I arrive home. He is really friendly.', 'dog'],
    ['Sophie is always sleeping when I arrive home. She is not much into socialization.', 'cat'],
    ['My dog is so old that he can not do anything else but sleep.', 'dog'],
    ['I like friendly animals. All-day-sleeping pets is not my thing.', 'dog']
])


# %%
X_test = [clean_and_tokenize(text) for text in test_data[:, 0]]


# %%
X_test = tfidf.transform(X_test)


# %%
y_test = test_data[:, 1]


# %%
y_test, y_pred


# %%
y_pred = clf.predict(X_test)


# %%
print(metrics.classification_report(y_test, y_pred))


# %%
