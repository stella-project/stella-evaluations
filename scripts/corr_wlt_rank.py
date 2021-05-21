from db import *
from util import *
from config import *
import pandas as pd
from scipy.stats import wilcoxon


def system_stats(system_name, start, end):
    total_click = 0
    win = 0
    loss = 0
    tie = 0

    outcome = []
    top_rank = []

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

        top_rank_exp = 0

        base_click_cnt = 0
        exp_click_cnt = 0
        for rank, doc in sys_feed.clicks.items():

            if doc.get('type') == 'EXP' and not top_rank_exp:
                top_rank_exp = int(rank)

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
            outcome.append(0)
            top_rank.append(top_rank_exp)

        if base_click_cnt > exp_click_cnt:
            if system_name not in BASELINE_SYSTEMS:
                loss += 1
                outcome.append(-1)
                top_rank.append(top_rank_exp)
            else:
                win += 1
                outcome.append(1)
                top_rank.append(top_rank_exp)

        if base_click_cnt < exp_click_cnt:
            if system_name not in BASELINE_SYSTEMS:
                win += 1
                outcome.append(1)
                top_rank.append(top_rank_exp)
            else:
                loss += 1
                outcome.append(-1)
                top_rank.append(top_rank_exp)

    return outcome, top_rank


def main():
    # round 1
    system_names = [system.name for system in systems.select().execute().fetchall() if system.name not in NOT_PARTICIPATED]
    overall_stats = {system_name: system_stats(system_name, start=ROUND_01_START, end=ROUND_02_END) for system_name in system_names}

    livivo_systems_exp = ['livivo_rank_pyserini', 'lemuren_elastic_only', 'lemuren_elastic_preprocessing',
                          'save_fami', 'tekmas', 'lemuren_elk']


    outcomes = []
    top_ranks = []
    for livivo_sys in livivo_systems_exp:
        outcomes += overall_stats[livivo_sys][0]
        top_ranks += overall_stats[livivo_sys][1]

    from scipy.stats import spearmanr
    print(spearmanr(outcomes, top_ranks))
    pass

    gesis_systems_exp = ['gesis_rec_pyterrier', 'gesis_rec_precom', 'tekma_n']
    outcomes = []
    top_ranks = []
    for gesis_sys in gesis_systems_exp:
        outcomes += overall_stats[gesis_sys][0]
        top_ranks += overall_stats[gesis_sys][1]

    from scipy.stats import spearmanr
    print(spearmanr(outcomes, top_ranks))


if __name__ == '__main__':
    main()

