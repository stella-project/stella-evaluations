from db import *
from util import *
from config import *
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

FILENAME_LIVIVO = 'livivo_ctr_vs_rank.pdf'
FILENAME_GESIS = 'gesis_ctr_vs_rank.pdf'


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
    df_ctr = df.iloc[:, : 50].div(df.sum(axis=1), axis=0)  # ctr of first 100 ranks
    df_ctr = df_ctr.transpose()
    df_ctr.index = df_ctr.index.values.astype(int)
    ax = df_ctr.plot.bar(figsize=(8, 3), legend=False, rot=0)
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if label._text not in ['1', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100']:
            label.set_visible(False)

    plt.ylabel('CTR')
    plt.xlabel('Rank')
    plt.title('LIVIVO')
    plt.savefig(os.path.join(RESULT_DIR, FILENAME_LIVIVO), bbox_inches='tight')
    plt.show()

    recommendation_systems = [s.id for s in systems.select().where(and_(systems.c.type != 'RANK')).execute().fetchall()]
    recommendation_sessions = sessions.select(sessions.c.system_recommendation.in_(recommendation_systems)).execute().fetchall()
    recommendation_sessions_ids = [r.id for r in recommendation_sessions]
    recommendation_feedbacks = feedbacks.select(feedbacks.c.session_id.in_(recommendation_sessions_ids)).execute().fetchall()
    cd = click_distribution(recommendation_feedbacks)
    df = pd.DataFrame(cd, index=['ctr'])
    df_ctr = df.iloc[:, : 6].div(df.sum(axis=1), axis=0)  # ctr of first 100 ranks
    df_ctr = df_ctr.transpose()
    df_ctr.index = df_ctr.index.values.astype(int)
    ax = df_ctr.plot.bar(figsize=(8, 3), legend=False, rot=0)
    plt.ylabel('CTR')
    plt.xlabel('Rank')
    plt.title('GESIS')
    plt.savefig(os.path.join(RESULT_DIR, FILENAME_GESIS), bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    main()
