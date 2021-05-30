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

    ranking_systems = [s for s in systems.select().where(and_(systems.c.type != 'REC', systems.c.name != 'livivo_base')).execute().fetchall()]
    ranking_systems = [r for r in ranking_systems if r.name not in NOT_PARTICIPATED]
    ranking_systems_ids = [r.id for r in ranking_systems]
    ranking_sessions = sessions.select(sessions.c.system_ranking.in_(ranking_systems_ids)).execute().fetchall()
    ranking_sessions_ids = [r.id for r in ranking_sessions]
    ranking_feedbacks = system_feedbacks = feedbacks.select(feedbacks.c.session_id.in_(ranking_sessions_ids)).execute().fetchall()

    q_len = []

    with tqdm(total=len(ranking_feedbacks)) as pbar:
        for f in ranking_feedbacks:
            try:
                q_str = results.select(results.c.feedback_id == f.id).execute().first().q
                q_str = q_str.replace('AND', '')
                q_str = q_str.replace('OR', '')
                q_str = q_str.replace('NOT', '')
                q_len.append(len(q_str.split()))
            except Exception as e:
                print(e)
            pbar.update()


if __name__ == '__main__':
    main()
