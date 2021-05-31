from db import *
from util import *
from config import *
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')
from tqdm import tqdm


def main():

    mkdir(RESULT_DIR)
    f_in_path = os.path.join(RESULT_DIR, 'livivo_click_stats.csv')
    df = pd.read_csv(f_in_path)
    pass

    data = {'Number of Unique Queries': len(df['qstr'].unique()),
     'Average Query Length': df['qlen'].mean(),
     'Average Number of Queries per Session': df.groupby('sid').size().mean(),
     'Average Number of Clicks per Query': df['clicks'].mean()}
    print(pd.DataFrame(data, index=['LIVIVO']).transpose().to_latex())


if __name__ == '__main__':
    main()
