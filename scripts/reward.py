import pandas as pd
import numpy as np


bookmark = 10
details = 1
fulltext = 8
instock = 8
more_links = 2
order = 10
title = 1


def main():

    df = pd.read_csv('../results/livivo_click_distribution.csv', index_col=0)

    df['clicks'] = df.sum(axis=1)

    df_rel = df.copy()

    df_rel['bookmark'] = df['bookmark'] * bookmark
    df_rel['details'] = df['details'] * details
    df_rel['fulltext'] = df['fulltext'] * fulltext
    df_rel['instock'] = df['instock'] * instock
    df_rel['more_links'] = df['more_links'] * more_links
    df_rel['order'] = df['order'] * order
    df_rel['title'] = df['title'] * title
    df_rel['reward'] = df_rel.iloc[:, :7].sum(axis=1)

    df_splits = np.array_split(df_rel, len(df_rel) / 2)
    tmp = pd.Series()
    for split in df_splits:
        total_reward = sum(split['reward'])
        split['nreward'] = split['reward'] / total_reward
        tmp = pd.concat([tmp, split['nreward']])
    df['nreward'] = tmp
    print(df.to_latex(float_format="%.4f"))


if __name__ == '__main__':
    main()
