from db import *
from util import *
from config import *
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

FILENAME = 'livivo_ctr_vs_rank.pdf'


def livivo_click_distribution(feedbacks):
    click_distr = dict.fromkeys(['title',
                                 'details',
                                 'fulltext',
                                 'order',
                                 'bookmark',
                                 'more_links',
                                 'instock'])

    for feedback in feedbacks:
        livivo_clicks = [rf.get('livivo_clicks') for rf in feedback.clicks.values()]
        for lc in livivo_clicks:
            for element, click in lc.items():
                if click:
                    if click_distr.get(element) is None:
                        click_distr[element] = 1
                    else:
                        click_distr[element] = click_distr[element] + 1
    return click_distr


def click_distribution(feedbacks):
    click_distr = dict.fromkeys(list(range(1, 201)))

    for feedback in feedbacks:
        try:
            page = results.select(results.c.feedback_id == feedback.id).execute().first().page
            for r, c in feedback.clicks.items():
                if c.get('clicked'):
                    rank = page * 10 + int(r)
                    if click_distr.get(rank) is None:
                        click_distr[rank] = 1
                    else:
                        click_distr[rank] = click_distr[rank] + 1
        except Exception as e:
            print(e)

    return click_distr


def main():

    mkdir(RESULT_DIR)

    ranking_systems = [s.id for s in systems.select().where(and_(systems.c.type != 'REC', systems.c.name != 'livivo_base')).execute().fetchall()]
    ranking_sessions = sessions.select(sessions.c.system_ranking.in_(ranking_systems)).execute().fetchall()
    ranking_sessions_ids = [r.id for r in ranking_sessions]
    ranking_feedbacks = system_feedbacks = feedbacks.select(feedbacks.c.session_id.in_(ranking_sessions_ids)).execute().fetchall()
    cd = click_distribution(ranking_feedbacks)
    df = pd.DataFrame(cd, index=['ctr'])
    df_ctr = df.iloc[:, : 100].div(df.sum(axis=1), axis=0)  # ctr of first 100 ranks
    df_ctr = df_ctr.transpose()
    df_ctr.index = df_ctr.index.values.astype(int)
    ax = df_ctr.plot.bar(figsize=(8, 3), legend=False)
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if label._text not in ['1', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100']:
            label.set_visible(False)

    plt.ylabel('CTR')
    plt.xlabel('Rank')
    plt.title('LIVIVO')
    plt.savefig(os.path.join(RESULT_DIR, FILENAME), bbox_inches='tight')

    plt.show()



    pass


    # lcd = livivo_click_distribution(ranking_feedbacks)
    # lcd = dict(sorted(lcd.items(), key=lambda item: item[1], reverse=True))
    #
    # pd.DataFrame.from_dict(lcd, orient='index', columns=['Number of clicks']).plot.bar()
    # plt.xlabel('SERP element')
    # plt.ylabel('Number of clicks')
    # plt.savefig(os.path.join(RESULT_DIR, FILENAME), bbox_inches='tight')
    # plt.show()


if __name__ == '__main__':
    main()
