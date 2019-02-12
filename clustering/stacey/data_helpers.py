from . import *


def split_dataframe(df, column, prefix):
    groups = df[column].unique()
    for group in tqdm.tqdm(groups):
        df[df[column] == group].to_csv(
            str(prefix)+'_'+str(group)+'.csv', index=False)
