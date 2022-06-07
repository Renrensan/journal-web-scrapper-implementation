import pandas as pd
import os


def create_dataframe(dictionary):
    return pd.DataFrame(dictionary)


def create_tsv(dataframe, filename):
    filepath = os.path.join(os.getcwd()+'/results/', filename)
    return dataframe.to_csv(filepath, index=False, sep='\t')