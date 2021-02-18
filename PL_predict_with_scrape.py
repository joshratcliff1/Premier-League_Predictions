import pandas as pd
import numpy as np


''' https://fixturedownload.com/results/epl-2020 '''

# show complete records by changing rules
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def triangle(n):
    """Calculates the triangle number. ie. 1+2+...+n"""
    return sum([x for x in range(n+1)])

# Load the dataset into the dataframe
df = pd.read_csv('epl-2020-GMTStandardTime.csv')

#