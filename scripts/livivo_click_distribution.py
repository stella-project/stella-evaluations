from db import *
from util import *
from config import *
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

FILENAME = 'livivo_click_distribution.pdf'


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


def main():

    mkdir(RESULT_DIR)

    ranking_systems = [s.id for s in systems.select().where(and_(systems.c.type != 'REC', systems.c.name != 'livivo_base')).execute().fetchall()]
    ranking_sessions = sessions.select(sessions.c.system_ranking.in_(ranking_systems)).execute().fetchall()
    ranking_sessions_ids = [r.id for r in ranking_sessions]
    ranking_feedbacks = system_feedbacks = feedbacks.select(feedbacks.c.session_id.in_(ranking_sessions_ids)).execute().fetchall()

    lcd = livivo_click_distribution(ranking_feedbacks)
    lcd = dict(sorted(lcd.items(), key=lambda item: item[1], reverse=True))

    df = pd.DataFrame.from_dict(lcd, orient='index', columns=['Number of clicks'])
    df['CTR'] = df['Number of clicks'] / df['Number of clicks'].sum()

    df['CTR'].plot.bar(legend=False)
    plt.title('LIVIVO')
    plt.xlabel('SERP element')
    plt.ylabel('CTR')
    plt.savefig(os.path.join(RESULT_DIR, FILENAME), bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    main()
