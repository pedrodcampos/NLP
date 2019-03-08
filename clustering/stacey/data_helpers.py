from . import *


def split_dataframe(df, column, prefix):
    groups = df[column].unique()
    for group in tqdm.tqdm(groups):
        df[df[column] == group].to_csv(path.get_data_file(
            str(prefix)+'_'+str(group)+'.csv'), index=False)


def get_unique_words(series):
    unique_words = set()
    unique_texts = series.unique()
    for text in unique_texts:
        for word in text.split():
            if word.isalpha() and len(word) > 2:
                unique_words.update([word.lower()])
    return list(unique_words)
