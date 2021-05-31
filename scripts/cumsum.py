from db import *
from util import *
from config import *
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

DAILY_STATS_CSV = '../results/daily_stats.csv'

df = pd.read_csv(DAILY_STATS_CSV, index_col=0)

system_names = [system.name for system in systems.select(not_(systems.c.name.in_(NOT_PARTICIPATED))).execute().fetchall()]

# df.loc[['livivo_base_clicks',
#         'livivo_rank_pyserini_clicks',
#         'lemuren_elastic_only_clicks',
#         'lemuren_elastic_preprocessing_clicks']].transpose().cumsum().plot.line()

df = df.transpose()
df['Clicks'] = df['livivo_base_clicks'].fillna(0)
df['Sessions'] = 0
df['Impressions'] = 0

for c in ['lemuren_elk_clicks', 'tekmas_clicks', 'save_fami_clicks', 'livivo_rank_pyserini_clicks']:
    df['Clicks'] = df['Clicks'] + df[c].fillna(0)

for s in ['lemuren_elk_sessions', 'tekmas_sessions', 'save_fami_sessions', 'livivo_rank_pyserini_sessions']:
    df['Sessions'] = df['Sessions'] + df[s].fillna(0)

for i in ['lemuren_elk_impressions', 'tekmas_impressions', 'save_fami_impressions', 'livivo_rank_pyserini_impressions']:
    df['Impressions'] = df['Impressions'] + df[i].fillna(0)

df[['Clicks', 'Sessions', 'Impressions']][: 28].cumsum().plot.line()

plt.title('Cumulative Clicks, Sessions, and Impressions at LIVIVO in Round 1')
plt.axvspan(0, 13, color='blue', alpha=0.1)
plt.axvspan(13, 28, color='green', alpha=0.1)
plt.savefig(os.path.join(RESULT_DIR, 'cumsum.pdf'), bbox_isnches='tight')
plt.show()