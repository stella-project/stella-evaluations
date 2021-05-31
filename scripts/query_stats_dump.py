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

    ranking_systems = [s for s in systems.select().where(and_(systems.c.type != 'REC',
                                                              systems.c.name != 'livivo_base',
                                                              sessions.c.start > ROUND_01_START,
                                                              sessions.c.end < ROUND_02_END)).execute().fetchall()]
    ranking_systems = [r for r in ranking_systems if r.name not in NOT_PARTICIPATED]
    ranking_systems_ids = [r.id for r in ranking_systems]
    ranking_sessions = sessions.select(sessions.c.system_ranking.in_(ranking_systems_ids)).execute().fetchall()
    ranking_sessions_ids = [r.id for r in ranking_sessions]
    ranking_feedbacks = feedbacks.select(feedbacks.c.session_id.in_(ranking_sessions_ids)).execute().fetchall()

    # ranking_feedbacks = ranking_feedbacks[:1000]
    ranking_feedbacks = ranking_feedbacks


    csv_data = []


    # {
    #  'q_str_raw': '',
    #  'q_str': '',
    #  'q_len': '',
    #  'sid': '',
    #  'clicks': '',
    # }

    with tqdm(total=len(ranking_feedbacks)) as pbar:
        for f in ranking_feedbacks:
            try:
                q_str_raw = results.select(results.c.feedback_id == f.id).execute().first().q
                q_str = q_str_raw.replace('AND', '')
                q_str = q_str.replace('OR', '')
                q_str = q_str.replace('NOT', '')
                q_str = q_str.lower()

                click_cnt = 0
                for val in f.clicks.values():
                    if val.get('clicked'):
                        click_cnt += 1

                csv_data.append({'qstr_raw': q_str_raw,
                                 'qstr': q_str,
                                 'qlen': len(q_str.split()),
                                 'sid': f.session_id,
                                 'clicks': click_cnt,
                                 'bool': 'AND' in q_str_raw or 'OR' in q_str_raw or 'NOT' in q_str_raw})





            except Exception as e:
                print(e)
            pbar.update()

    # print(csv_data)

    f_out_path = os.path.join(RESULT_DIR, 'livivo_click_stats.csv')
    pd.DataFrame.from_dict(csv_data).to_csv(f_out_path, index=False)


    # number of unique queries
    # number of queries per session
    # query length


if __name__ == '__main__':
    main()
