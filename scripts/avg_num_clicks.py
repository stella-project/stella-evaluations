from db import *
from util import *
from config import *
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

DAILY_STATS_CSV = os.path.join(RESULT_DIR, 'daily_stats.csv')

df = pd.read_csv(DAILY_STATS_CSV, index_col=0)

system_names = [system.name for system in systems.select(and_(not_(systems.c.name.in_(NOT_PARTICIPATED)),
                                                                   systems.c.type == 'REC')).execute().fetchall()]

recommenders = [system.name for system in systems.select(and_(not_(systems.c.name.in_(NOT_PARTICIPATED)),
                                                                   systems.c.type == 'REC')).execute().fetchall()]

rankers = [system.name for system in systems.select(and_(not_(systems.c.name.in_(NOT_PARTICIPATED)),
                                                              systems.c.type == 'RANK')).execute().fetchall()]

df.loc[[r + '_clicks' for r in rankers]].fillna(0).sum(axis=0).plot.bar(figsize=(14,7))
df.loc[[r + '_clicks' for r in rankers]].fillna(0).sum(axis=0).expanding().mean().plot(color='g')
plt.show()

df.loc[[r + '_clicks' for r in recommenders]].fillna(0).sum(axis=0).plot.bar(figsize=(14,7))
df.loc[[r + '_clicks' for r in recommenders]].fillna(0).sum(axis=0).expanding().mean().plot(color='g')
plt.show()

