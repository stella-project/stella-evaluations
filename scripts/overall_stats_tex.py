from db import *
from util import *
from config import *
import pandas as pd


def system_stats(system_name, start, end):
    total_click = 0
    win = 0
    loss = 0
    tie = 0

    system = systems.select(systems.c.name==system_name).execute().first()

    if system_name not in BASELINE_SYSTEMS:
        system_sessions = sessions.select(sessions.c.system_ranking == system.id).where(and_(sessions.c.start > start, sessions.c.end < end)).execute().fetchall()
        if not len(system_sessions):
            system_sessions = sessions.select(sessions.c.system_recommendation == system.id).where(and_(sessions.c.start > start, sessions.c.end < end)).execute().fetchall()

    else:
        type = 'RANK' if system_name == 'livivo_base' else 'REC'
        system_ids = [system.id for system in systems.select(systems.c.type == type).execute().fetchall()]
        if type == 'RANK':
            system_sessions = sessions.select(sessions.c.system_ranking.in_(system_ids)).where(and_(sessions.c.start > start, sessions.c.end < end)).execute().fetchall()
        else:
            system_sessions = sessions.select(sessions.c.system_recommendation.in_(system_ids)).where(and_(sessions.c.start > start, sessions.c.end < end)).execute().fetchall()

    session_ids = [s.id for s in system_sessions]
    system_feedbacks = feedbacks.select(feedbacks.c.session_id.in_(session_ids)).execute().fetchall()

    for sys_feed in system_feedbacks:
        base_click_cnt = 0
        exp_click_cnt = 0
        for rank, doc in sys_feed.clicks.items():
            if doc.get('type') == 'EXP' and doc.get('clicked'):
                exp_click_cnt += 1
                if system_name not in BASELINE_SYSTEMS:
                    total_click += 1

            if doc.get('type') == 'BASE' and doc.get('clicked'):
                base_click_cnt += 1
                if system_name in BASELINE_SYSTEMS:
                    total_click += 1

        if base_click_cnt == exp_click_cnt and base_click_cnt + exp_click_cnt > 0:
            tie += 1

        if base_click_cnt > exp_click_cnt:
            if system_name not in BASELINE_SYSTEMS:
                loss += 1
            else:
                win += 1

        if base_click_cnt < exp_click_cnt:
            if system_name not in BASELINE_SYSTEMS:
                win += 1
            else:
                loss += 1

    num_sessions = len(system_sessions)
    impressions = len(system_feedbacks)
    outcome = win / (win + loss) if win + loss > 0 else 0
    ctr = total_click / impressions if impressions > 0 else 0

    return {'Win': win,
            'Loss': loss,
            'Tie': tie,
            'Outcome': outcome,
            'Sessions': num_sessions,
            'Impressions': impressions,
            'Clicks': total_click,
            'CTR': ctr}

def main():

    # round 1
    system_names = [system.name for system in systems.select().execute().fetchall() if system.name not in NOT_PARTICIPATED]
    overall_stats = {system_name: system_stats(system_name, start=ROUND_01_START, end=ROUND_01_END) for system_name in system_names}
    df = pd.DataFrame.from_dict(overall_stats).transpose()
    df['Win'] = df['Win'].astype('int64')
    df['Loss'] = df['Loss'].astype('int64')
    df['Tie'] = df['Tie'].astype('int64')
    df['Outcome'] = df['Outcome'].map('{:,.2f}'.format)
    df['Clicks'] = df['Clicks'].astype('int64')
    df['Impressions'] = df['Impressions'].astype('int64')
    df['Sessions'] = df['Sessions'].astype('int64')
    df['CTR'] = df['CTR'].map('{:,.4f}'.format)
    df = df[['Win', 'Loss', 'Tie', 'Outcome', 'Sessions', 'Impressions', 'Clicks', 'CTR']]
    print(df.to_latex())

    # round 2
    system_names = [system.name for system in systems.select().execute().fetchall() if system.name not in NOT_PARTICIPATED]
    overall_stats = {system_name: system_stats(system_name, start=ROUND_02_START, end=ROUND_02_END) for system_name in system_names}
    df = pd.DataFrame.from_dict(overall_stats).transpose()
    df['Win'] = df['Win'].astype('int64')
    df['Loss'] = df['Loss'].astype('int64')
    df['Tie'] = df['Tie'].astype('int64')
    df['Outcome'] = df['Outcome'].map('{:,.2f}'.format)
    df['Clicks'] = df['Clicks'].astype('int64')
    df['Impressions'] = df['Impressions'].astype('int64')
    df['Sessions'] = df['Sessions'].astype('int64')
    df['CTR'] = df['CTR'].map('{:,.4f}'.format)
    df = df[['Win', 'Loss', 'Tie', 'Outcome', 'Sessions', 'Impressions', 'Clicks', 'CTR']]
    print(df.to_latex())


if __name__ == '__main__':
    main()
