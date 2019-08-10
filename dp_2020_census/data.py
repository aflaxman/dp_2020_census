"""dp_2020_census.data

Code to extract, transform, and load data on the 1940s census
* IPUMS original data
* Census TopDown data

"""
import collections

import numpy as np, matplotlib.pyplot as plt, pandas as pd
pd.set_option('display.max_rows', 10)  # make pdb output look nicer


def ipums_colspecs():
    """Create pd.series suitable for loading fixed-width file 
    of 1940s census data from IPUMS"""

    with open('data/full_ipums_1940_census_colspecs.txt') as f:
        colspec_str = f.read()

    colspecs = pd.Series()
    for line in colspec_str.split('\n'):
        name = line.split()[0].strip()
        val_str = line.split()[2]

        start_str = val_str.split('-')[0]
        start_index = int(start_str) - 1

        end_str = val_str.split('-')[-1]
        end_index = int(end_str)

        colspecs[name] = (start_index, end_index)
    return colspecs


def topdown_colnames():
    # columns are hard to find, but I've got them here
    # https://github.com/uscensusbureau/census2020-das-e2e/blob/3f2c9cf9cb3c33a4e2067bd784ff381792f7ffc0/programs/writer/e2e_1940_writer.py#L82-L84

    col_names = ('SCHEMA_TYPE_CODE, SCHEMA_BUILD_ID, STATE, COUNTY, ENUMDIST, '
                 'EUID, EPNUM, RTYPE, QREL, QSEX, QAGE, CENHISP, CENRACE, QSPANX, '
                 'QRACE1, QRACE2, QRACE3, QRACE4, QRACE5, QRACE6, QRACE7, QRACE8, CIT').split(', ')
    return col_names

def load_transform_orig():
    """Tally count from 1940s IPUMS data, stratified by
    state, county, enumeration district, group quarters type, voting age status, race, and ethnicity

    Results
    -------
    returns pd.DataFrame with the following columns
    ['state', 'county', 'enum_dist', 'gq', 'age', 'race', 'eth', 'count']

    Timing
    ------
    7s for 20_000 rows
    70s for 200_000 rows
    predict 17h for full file (170_897_729 rows)
    """

    counts = collections.Counter()

    fname = '/home/j/Project/Models/us_census/EXT1940USCB.dat'
    colspecs = ipums_colspecs()

    chunksize = 20_000
    iter = pd.read_fwf(fname, list(colspecs), header=None, names=colspecs.index,
                       chunksize=chunksize)

    for i, df_i in enumerate(iter):
        for j, se in df_i.iterrows():
            if se.RECTYPE == 'H': # household record, so update hh info
                state = se.STATEFIP
                county = se.COUNTY
                enum = se.ENUMDIST
                gq = se.GQ
            else: # person record, assume it refers to a person in most recently read household record
                age = 17 + (se.AGE >= 18)  # match coding from 1940s E2E test of TopDown
                race = se.RACE
                eth = se.HISPAN

                counts[(state, county, enum, gq, age, race, eth)] += 1

            if (i*chunksize + j) % 10_000 == 0:
                print('.', end=' ', flush=True)

        #if i >= 0: break
        
    counts = pd.Series(counts).reset_index()
    counts.columns = ['state', 'county', 'enum_dist', 'gq', 'age', 'race', 'eth', 'count'] # brittle pattern, don't mess it up

    print()

    return counts

def load_transform_dp(epsilon, replicate):
    """Tally counts from 1940s run through TopDown, stratified by
    state, county, enumeration district, group quarters type, voting age status, race, and ethnicity

    Parameters
    ----------
    epsilon : str, privacy budget
    replicate : int, replicate 1, 2, 3, or 4

    Results
    -------
    returns pd.DataFrame with the following columns
    ['state', 'county', 'enum_dist', 'gq', 'age', 'race', 'eth', 'count']

    Timing
    ------
    7s for 2_000_000 rows
    43s for 20_000_000 rows
    predict 5m for full file (132_404_779 rows)
    """
    counts = collections.Counter()

    fname = f'/snfs1/Project/Models/us_census/{epsilon}-RUN{replicate}/MDF_PER.txt'
    print(fname)
    colnames = topdown_colnames()

    chunksize = 2_000_000
    iter = pd.read_csv(fname, sep='|', names=colnames, header=None, comment='#', chunksize=chunksize)

    for i, df_i in enumerate(iter):
        print('.', end=' ', flush=True)
        counts_i = df_i.groupby(['STATE', 'COUNTY', 'ENUMDIST', 'RTYPE', 'QAGE', 'CENRACE', 'CENHISP']).EPNUM.count()
        counts.update(counts_i.to_dict())  # I find this method name confusing, but it adds the values 
        #if i >= 0: break
    
    counts = pd.Series(counts).reset_index()
    counts.columns = ['state', 'county', 'enum_dist', 'gq', 'age', 'race', 'eth', 'count'] # brittle pattern, don't mess it up

    print()

    return counts


def etl_all():
    """Extract, transform, and save count files for original 1940s Census
    Data and for all TopDown runs.
    """

    # process the top down output
    for epsilon in '0.25 0.50 0.75 1.0 2.0 4.0 6.0 8.0'.split():
        for run in '1234':
            fname = f'/snfs1/Project/Models/us_census/dp_counts-{epsilon}-RUN{run}.csv'
            print(fname)
            counts = load_transform_dp(epsilon, run)
            counts.to_csv(fname)

    # process the original data
    fname = '/snfs1/Project/Models/us_census/orig_counts.csv'
    print(fname)
    counts = load_transform_orig()
    counts.to_csv(fname)

if __name__== "__main__":
    etl_all()
