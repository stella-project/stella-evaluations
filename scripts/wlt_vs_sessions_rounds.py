from db import *
from util import *
from config import *
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')


def get_wlt(feedbacks, base=False):

    win = 0
    loss = 0
    tie = 0

    for feedback in feedbacks:
        exp_click = 0
        base_click = 0

        for doc in feedback.clicks.values():
            if doc.get('clicked') and doc.get('type') == 'EXP':
                exp_click += 1
            if doc.get('clicked') and doc.get('type') == 'BASE':
                base_click += 1

        if exp_click == base_click and exp_click > 0:
            tie += 1
        if exp_click > base_click:
            if base:
                loss += 1
            else:
                win += 1
        if base_click > exp_click:
            if base:
                win += 1
            else:
                loss += 1

    return {'win': win,
            'loss': loss,
            'tie': tie}


def main():
    mkdir(RESULT_DIR)
    all_systems = systems.select().where(not_(systems.c.name.in_(NOT_PARTICIPATED))).execute().fetchall()

    start = ROUND_01_START
    end = ROUND_01_END

    for system in all_systems:

        result_dir_sys = os.path.join(RESULT_DIR, system.name)
        mkdir(result_dir_sys)

        cnt = 0
        wlt = {}

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
            # wlt[session.start] = get_wlt(system_feedbacks, base=system.name in BASELINE_SYSTEMS)
            wlt[cnt] = get_wlt(system_feedbacks, base=system.name in BASELINE_SYSTEMS)
            cnt += 1
        df = pd.DataFrame.from_dict(wlt)
        if not df.empty:
            if OUTCOME:
                df = df.transpose().cumsum()
                df['outcome'] = df['win'] / (df['win'] + df['loss'])
                ax = df.plot(secondary_y=['outcome'], mark_right=False)
                lines = ax.get_lines() + ax.right_ax.get_lines()
                ax.legend(lines,
                          [l.get_label() for l in lines], bbox_to_anchor=(0.5, -0.25),
                          loc='lower center',
                          ncol=len(df.columns))

                # ax.legend(loc='center left', bbox_to_anchor=(1.2, 0.5))
                ax.set_ylabel('Total number of Wins, Losses, Ties')
                ax.right_ax.set_ylabel('Outcome')
                ax.set_xlabel('Number of Sessions')
                # df[['win', 'loss', 'tie']].plot()
                # ax = df['outcome'].plot(secondary_y=True)
                plt.title(' - '.join([system.name, 'Cumulative Wins, Losses, and Ties + Outcome']))
                plt.savefig(os.path.join(result_dir_sys, '_'.join([system.name, 'wlt_vs_sessions_outcome_round1.pdf'])),
                            format='pdf', bbox_inches='tight')
                plt.savefig(os.path.join(result_dir_sys, '_'.join([system.name, 'wlt_vs_sessions_outcome_round1.svg'])),
                            format='svg', bbox_inches='tight')
                plt.show()

            else:
                df.transpose().cumsum().plot.line()
                plt.title(' - '.join([system.name, 'Cumulative Wins, Losses, and Ties']))
                plt.savefig(os.path.join(result_dir_sys, '_'.join([system.name, 'wlt_vs_sessions_round1.pdf'])),
                            format='pdf', bbox_inches='tight')
                plt.savefig(os.path.join(result_dir_sys, '_'.join([system.name, 'wlt_vs_sessions_round1.svg'])),
                            format='svg', bbox_inches='tight')
                plt.show()



    start = ROUND_02_START
    end = ROUND_02_END

    for system in all_systems:

        result_dir_sys = os.path.join(RESULT_DIR, system.name)
        mkdir(result_dir_sys)

        cnt = 0
        wlt = {}

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
            # wlt[session.start] = get_wlt(system_feedbacks, base=system.name in BASELINE_SYSTEMS)
            wlt[cnt] = get_wlt(system_feedbacks, base=system.name in BASELINE_SYSTEMS)
            cnt += 1
        df = pd.DataFrame.from_dict(wlt)
        if not df.empty:
            if OUTCOME:
                df = df.transpose().cumsum()
                df['outcome'] = df['win'] / (df['win'] + df['loss'])
                ax = df.plot(secondary_y=['outcome'], mark_right=False)
                lines = ax.get_lines() + ax.right_ax.get_lines()
                ax.legend(lines,
                          [l.get_label() for l in lines], bbox_to_anchor=(0.5, -0.25),
                          loc='lower center',
                          ncol=len(df.columns))

                # ax.legend(loc='center left', bbox_to_anchor=(1.2, 0.5))
                ax.set_ylabel('Total number of Wins, Losses, Ties')
                ax.right_ax.set_ylabel('Outcome')
                ax.set_xlabel('Number of Sessions')
                # df[['win', 'loss', 'tie']].plot()
                # ax = df['outcome'].plot(secondary_y=True)
                plt.title(' - '.join([system.name, 'Cumulative Wins, Losses, and Ties + Outcome']))
                plt.savefig(os.path.join(result_dir_sys, '_'.join([system.name, 'wlt_vs_sessions_outcome_round2.pdf'])),
                            format='pdf', bbox_inches='tight')
                plt.savefig(os.path.join(result_dir_sys, '_'.join([system.name, 'wlt_vs_sessions_outcome_round2.svg'])),
                            format='svg', bbox_inches='tight')
                plt.show()

            else:
                df.transpose().cumsum().plot.line()
                plt.title(' - '.join([system.name, 'Cumulative Wins, Losses, and Ties']))
                plt.savefig(os.path.join(result_dir_sys, '_'.join([system.name, 'wlt_vs_sessions_round2.pdf'])),
                            format='pdf', bbox_inches='tight')
                plt.savefig(os.path.join(result_dir_sys, '_'.join([system.name, 'wlt_vs_sessions_round2.svg'])),
                            format='svg', bbox_inches='tight')
                plt.show()


if __name__ == '__main__':
    main()
