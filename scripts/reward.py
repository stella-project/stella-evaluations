import pandas as pd
import numpy as np


bookmark = 10
details = 1
fulltext = 8
instock = 8
more_links = 2
order = 10
title = 1


def sum_pairs(clicks: pd.Series):
    total_clicks = []
    for i in range(0, len(clicks)-1, 2):
        sum = clicks[i] + clicks[i + 1]
        total_clicks.append(sum)
        total_clicks.append(sum)
        # total_clicks[i+1] = clicks[i] + clicks[i+1]

    return pd.Series(total_clicks, name='total_clicks', index=clicks.index)



def main():

    df = pd.read_csv('../results/livivo_click_distribution.csv', index_col=0)

    df['clicks'] = df.sum(axis=1)

    df_rel = df.copy()

    # df_rel['bookmark'] = df['bookmark'] * bookmark / df['clicks']
    # df_rel['details'] = df['details'] * details / df['clicks']
    # df_rel['fulltext'] = df['fulltext'] * fulltext / df['clicks']
    # df_rel['instock'] = df['instock'] * instock / df['clicks']
    # df_rel['more_links'] = df['more_links'] * more_links / df['clicks']
    # df_rel['order'] = df['order'] * order / df['clicks']
    # df_rel['title'] = df['title'] * title / df['clicks']

    df_rel['bookmark'] = df['bookmark'] * df['bookmark'] * bookmark / df['clicks']
    df_rel['details'] = df['details'] * df['details'] * details / df['clicks']
    df_rel['fulltext'] = df['fulltext'] * df['fulltext'] * fulltext / df['clicks']
    df_rel['instock'] = df['instock'] * df['instock'] * instock / df['clicks']
    df_rel['more_links'] = df['more_links'] * df['more_links'] * more_links / df['clicks']
    df_rel['order'] = df['order'] * df['order'] * order / df['clicks']
    df_rel['title'] = df['title'] * df['title'] * title / df['clicks']
    df_rel['rel_cum_reward'] = df_rel.iloc[:, :7].sum(axis=1)

    df_splits = np.array_split(df_rel, len(df_rel) / 2)
    tmp = pd.Series()
    for split in df_splits:
        total_clicks = sum(split['rel_cum_reward'])
        split['reward'] = split['rel_cum_reward'] / total_clicks
        tmp = pd.concat([tmp, split['reward']])
    df['reward'] = tmp
    print(df.to_latex())


if __name__ == '__main__':
    main()
