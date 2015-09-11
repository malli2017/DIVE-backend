'''
Module for reading datasets given some specifier

TODO Rename either this or access.py to be more descriptive
'''

import pandas as pd
from bson.objectid import ObjectId

from .in_memory_data import InMemoryData as IMD
from .db import MongoInstance as MI


# TODO Change to get_data_as_dataframe
# Or more generally return data in different formats
def get_data(pID=None, dID=None, path=None, nrows=None):
    if IMD.hasData(dID):
        return IMD.getData(dID)
    if path:
        delim = get_delimiter(path)
        df = pd.read_table(path, sep=delim, error_bad_lines=False, nrows=nrows)
    if dID and pID:
        dataset = MI.getData({'_id' : ObjectId(dID)}, pID)[0]
        path = dataset['path']
        delim = get_delimiter(path)
        df = pd.read_table(path, sep=delim, error_bad_lines=False, nrows=nrows)
        IMD.insertData(dID, df)
    return df


def get_delimiter(path):
    ''' Utility function to detect extension and return delimiter '''
    filename = path.rsplit('/')[-1]
    extension = filename.rsplit('.', 1)[1]
    if extension == 'csv':
        delim = ','
    elif extension == 'tsv':
        delim = '\t'
    # TODO Detect separators intelligently
    elif extension == 'txt':
        delim = ','
    return delim
