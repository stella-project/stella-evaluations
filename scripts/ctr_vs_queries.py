from db import *
from util import *
from config import *
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

import json

FILENAME_LIVIVO = 'livivo_clicks_vs_queries.pdf'
FILENAME_GESIS = 'gesis_clicks_vs_queries.pdf'


def query_distribution(feedbacks):
    q_distr = {}

    for feedback in feedbacks:
        try:  # not all feedbacks have results
            query = results.select(results.c.feedback_id == feedback.id).execute().first().q
            for r, c in feedback.clicks.items():
                if c.get('clicked'):
                    if q_distr.get(query) is None:
                        q_distr[query] = 1
                    else:
                        q_distr[query] = q_distr[query] + 1

        except Exception as e:
            print(e)

    return q_distr


def main():
    mkdir(RESULT_DIR)
    ranking_systems = [s.id for s in systems.select().where(and_(systems.c.type != 'REC', systems.c.name != 'livivo_base')).execute().fetchall()]
    ranking_sessions = sessions.select(sessions.c.system_ranking.in_(ranking_systems)).execute().fetchall()
    ranking_sessions_ids = [r.id for r in ranking_sessions]
    ranking_feedbacks = system_feedbacks = feedbacks.select(feedbacks.c.session_id.in_(ranking_sessions_ids)).execute().fetchall()
    cd = query_distribution(ranking_feedbacks)
    df = pd.DataFrame(cd, index=['Clicks'])
    df.transpose().sort_values(by='Clicks', ascending=False).iloc[:100, :].plot.bar(figsize=(8, 3), legend=False, color=['g'])
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.ylabel('Clicks')
    plt.xlabel('Query')
    plt.title('LIVIVO')
    plt.savefig(os.path.join(RESULT_DIR, FILENAME_LIVIVO), bbox_inches='tight')
    plt.show()
    print(df.transpose().sort_values(by='Clicks', ascending=False).iloc[:10, :].to_latex())

    recommendation_systems = [s.id for s in systems.select().where(and_(systems.c.type != 'RANK')).execute().fetchall()]
    recommendation_sessions = sessions.select(sessions.c.system_recommendation.in_(recommendation_systems)).execute().fetchall()
    recommendation_sessions_ids = [r.id for r in recommendation_sessions]
    recommendation_feedbacks = feedbacks.select(feedbacks.c.session_id.in_(recommendation_sessions_ids)).execute().fetchall()
    cd = query_distribution(recommendation_feedbacks)
    df = pd.DataFrame(cd, index=['Clicks'])
    df.transpose().sort_values(by='Clicks', ascending=False).iloc[:100, :].plot.bar(figsize=(8, 3), legend=False, color=['g'])
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.ylabel('Clicks')
    plt.xlabel('Document')
    plt.title('GESIS')
    plt.savefig(os.path.join(RESULT_DIR, FILENAME_GESIS), bbox_inches='tight')
    plt.show()
    print(df.transpose().sort_values(by='Clicks', ascending=False).iloc[:10, :].to_latex())


    with open('../data/gesis-search/publication.jsonl') as f_in:
        lines = f_in.readlines()

        for docid in df.transpose().sort_values(by='Clicks', ascending=False).head(10).index:
            for line in lines:
                if json.loads(line).get('id') == docid:
                    print(docid, ' - ', json.loads(line).get('title'))


if __name__ == '__main__':
    main()
