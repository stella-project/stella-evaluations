from db import *
from util import *
from config import *
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')


def main():
    mkdir(RESULT_DIR)
    data = {}

    all_systems = systems.select().where(not_(systems.c.name.in_(NOT_PARTICIPATED))).execute().fetchall()
    for system in all_systems:
        if system.type == 'RANK':
            system_sessions = sessions.select(sessions.c.system_ranking == system.id).where(and_(sessions.c.start > ROUND_01_START, sessions.c.end < ROUND_02_END)).execute().fetchall()
        if system.type == 'REC':
            system_sessions = sessions.select(sessions.c.system_recommendation == system.id).where(and_(sessions.c.start > ROUND_01_START, sessions.c.end < ROUND_02_END)).execute().fetchall()

        if system.name in BASELINE_SYSTEMS:
            if system.type == 'RANK':
                ranking_systems = systems.select(systems.c.type=='RANK').execute().fetchall()
                system_sessions = sessions.select(sessions.c.system_ranking.in_([r.id for r in ranking_systems])).where(and_(sessions.c.start > ROUND_01_START, sessions.c.end < ROUND_02_END)).execute().fetchall()
            else:
                recommendation_systems = systems.select(systems.c.type == 'REC').execute().fetchall()
                system_sessions = sessions.select(sessions.c.system_recommendation.in_([r.id for r in recommendation_systems])).where(and_(sessions.c.start > ROUND_01_START, sessions.c.end < ROUND_02_END)).execute().fetchall()

        system_sessions_ids = [r.id for r in system_sessions]
        system_feedbacks = feedbacks.select(feedbacks.c.session_id.in_(system_sessions_ids)).execute().fetchall()

        sessions_cnt = {}
        impressions_cnt = {}
        clicks_cnt = {}
        clicks_base_cnt = {}

        for session in system_sessions:
            if sessions_cnt.get(session.start.strftime('%Y-%m-%d')):
                sessions_cnt[session.start.strftime('%Y-%m-%d')] += 1
            else:
                sessions_cnt[session.start.strftime('%Y-%m-%d')] = 1

        for feedback in system_feedbacks:
            if impressions_cnt.get(feedback.start.strftime('%Y-%m-%d')):
                impressions_cnt[feedback.start.strftime('%Y-%m-%d')] += 1
            else:
                impressions_cnt[feedback.start.strftime('%Y-%m-%d')] = 1

            for doc in feedback.clicks.values():
                if doc.get('clicked') and doc.get('type') == 'EXP':
                    if clicks_cnt.get(feedback.start.strftime('%Y-%m-%d')):
                        clicks_cnt[feedback.start.strftime('%Y-%m-%d')] += 1
                    else:
                        clicks_cnt[feedback.start.strftime('%Y-%m-%d')] = 1

                if doc.get('clicked') and doc.get('type') == 'BASE':
                    if clicks_base_cnt.get(feedback.start.strftime('%Y-%m-%d')):
                        clicks_base_cnt[feedback.start.strftime('%Y-%m-%d')] += 1
                    else:
                        clicks_base_cnt[feedback.start.strftime('%Y-%m-%d')] = 1

        data['_'.join([system.name, 'sessions'])] = sessions_cnt
        data['_'.join([system.name, 'impressions'])] = impressions_cnt
        data['_'.join([system.name, 'clicks'])] = clicks_cnt
        data['_'.join([system.name, 'clicks_base'])] = clicks_base_cnt

    pd.DataFrame.from_dict(data).transpose().to_csv(os.path.join(RESULT_DIR, 'daily_stats.csv'))


if __name__ == '__main__':
    main()
