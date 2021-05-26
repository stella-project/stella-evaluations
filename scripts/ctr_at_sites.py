from db import *
from util import *
from config import *
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')


def main():

    all_systems = systems.select().where(not_(systems.c.name.in_(NOT_PARTICIPATED))).execute().fetchall()

    sessions_livivo = 0
    impressions_livivo = 0
    clicks_livivo = 0
    sessions_gesis = 0
    impressions_gesis = 0
    clicks_gesis = 0

    start = ROUND_01_START
    end = ROUND_01_END

    for system in all_systems:
        if system.type == 'RANK':
            system_sessions = sessions.select(sessions.c.system_ranking == system.id).where(and_(sessions.c.start > start, sessions.c.end < end)).order_by(sessions.c.start).execute().fetchall()
        if system.type == 'REC':
            system_sessions = sessions.select(sessions.c.system_recommendation == system.id).where(and_(sessions.c.start > start, sessions.c.end < end)).order_by(sessions.c.start).execute().fetchall()

        if system.name in BASELINE_SYSTEMS:
            if system.type == 'RANK':
                ranking_systems = systems.select(systems.c.type=='RANK').execute().fetchall()
                system_sessions = sessions.select(sessions.c.system_ranking.in_([r.id for r in ranking_systems])).where(and_(sessions.c.start > start, sessions.c.end < end)).execute().fetchall()
            else:
                recommendation_systems = systems.select(systems.c.type == 'REC').execute().fetchall()
                system_sessions = sessions.select(sessions.c.system_recommendation.in_([r.id for r in recommendation_systems])).where(and_(sessions.c.start > start, sessions.c.end < end)).execute().fetchall()

        for session in system_sessions:
            system_feedbacks = feedbacks.select(feedbacks.c.session_id == session.id).execute().fetchall()

            if system.type == 'RANK':
                impressions_livivo += len(system_feedbacks)

                for feedback in system_feedbacks:
                    for doc in feedback.clicks.values():
                        if doc.get('clicked'):
                            clicks_livivo += 1
                # for feedback in system_feedbacks:
                    # click = False
                    # for doc in feedback.clicks.values():
                    #     if doc.get('clicked'):
                    #         click = True
                    # if click:
                    #     clicks_livivo += 1



            if system.type == 'REC':
                impressions_gesis += len(system_feedbacks)

                for feedback in system_feedbacks:
                    for doc in feedback.clicks.values():
                        if doc.get('clicked'):
                            clicks_gesis += 1
                # for feedback in system_feedbacks:
                    # click = False
                    # for doc in feedback.clicks.values():
                    #     if doc.get('clicked'):
                    #         click = True
                    # if click:
                    #     clicks_gesis += 1

        if system.type == 'RANK':
            sessions_livivo = sessions_livivo + len(system_sessions)
        if system.type == 'REC':
            sessions_gesis = sessions_gesis + len(system_sessions)


    # print(impressions_livivo)
    # print(clicks_livivo)
    # print(clicks_livivo/impressions_livivo)
    # print(impressions_gesis)
    # print(clicks_gesis)
    # print(clicks_gesis/impressions_gesis)

    df_data = [
     {'Evaluation round': 'Round 1',
      'Site': 'LIVIVO',
      'Sessions': sessions_livivo,
      'Impressions': impressions_livivo,
      'Clicks': clicks_livivo,
      'CTR': clicks_livivo/impressions_livivo},
     {'Evaluation round': 'Round 1',
      'Site': 'GESIS',
      'Sessions': sessions_gesis,
      'Impressions': impressions_gesis,
      'Clicks': clicks_gesis,
      'CTR': clicks_gesis / impressions_gesis}
     ]

    sessions_livivo = 0
    impressions_livivo = 0
    clicks_livivo = 0
    sessions_gesis = 0
    impressions_gesis = 0
    clicks_gesis = 0

    start = ROUND_02_START
    end = ROUND_02_END

    for system in all_systems:
        if system.type == 'RANK':
            system_sessions = sessions.select(sessions.c.system_ranking == system.id).where(and_(sessions.c.start > start, sessions.c.end < end)).order_by(sessions.c.start).execute().fetchall()
        if system.type == 'REC':
            system_sessions = sessions.select(sessions.c.system_recommendation == system.id).where(and_(sessions.c.start > start, sessions.c.end < end)).order_by(sessions.c.start).execute().fetchall()

        if system.name in BASELINE_SYSTEMS:
            if system.type == 'RANK':
                ranking_systems = systems.select(systems.c.type=='RANK').execute().fetchall()
                system_sessions = sessions.select(sessions.c.system_ranking.in_([r.id for r in ranking_systems])).where(and_(sessions.c.start > start, sessions.c.end < end)).execute().fetchall()
            else:
                recommendation_systems = systems.select(systems.c.type == 'REC').execute().fetchall()
                system_sessions = sessions.select(sessions.c.system_recommendation.in_([r.id for r in recommendation_systems])).where(and_(sessions.c.start > start, sessions.c.end < end)).execute().fetchall()

        for session in system_sessions:
            system_feedbacks = feedbacks.select(feedbacks.c.session_id == session.id).execute().fetchall()

            if system.type == 'RANK':
                impressions_livivo += len(system_feedbacks)

                for feedback in system_feedbacks:
                    for doc in feedback.clicks.values():
                        if doc.get('clicked'):
                            clicks_livivo += 1
                # for feedback in system_feedbacks:
                #     click = False
                #     for doc in feedback.clicks.values():
                #         if doc.get('clicked'):
                #             click = True
                #     if click:
                #         clicks_livivo += 1

            if system.type == 'REC':
                impressions_gesis += len(system_feedbacks)

                for feedback in system_feedbacks:
                    for doc in feedback.clicks.values():
                        if doc.get('clicked'):
                            clicks_gesis += 1
                # for feedback in system_feedbacks:
                #     click = False
                #     for doc in feedback.clicks.values():
                #         if doc.get('clicked'):
                #             click = True
                #     if click:
                #         clicks_gesis += 1

        if system.type == 'RANK':
            sessions_livivo = sessions_livivo + len(system_sessions)
        if system.type == 'REC':
            sessions_gesis = sessions_gesis + len(system_sessions)


    # print(impressions_livivo)
    # print(clicks_livivo)
    # print(clicks_livivo/impressions_livivo)
    # print(impressions_gesis)
    # print(clicks_gesis)
    # print(clicks_gesis/impressions_gesis)

    df_data.append({'Evaluation round': 'Round 2',
                    'Site': 'LIVIVO',
                    'Sessions': sessions_livivo,
                    'Impressions': impressions_livivo,
                    'Clicks': clicks_livivo,
                    'CTR': clicks_livivo/impressions_livivo})

    df_data.append({'Evaluation round': 'Round 2',
                    'Site': 'GESIS',
                    'Sessions': sessions_gesis,
                    'Impressions': impressions_gesis,
                    'Clicks': clicks_gesis,
                    'CTR': clicks_gesis/impressions_gesis})

    df = pd.DataFrame(df_data)
    print(df[['Evaluation round', 'Site', 'Sessions', 'Impressions', 'Clicks', 'CTR']].to_latex(index=False, float_format="%.4f"))


if __name__ == '__main__':
    main()
