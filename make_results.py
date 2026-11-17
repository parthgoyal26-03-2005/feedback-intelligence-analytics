import pandas as pd
import matplotlib.pyplot as plt
from analysis import analyze
from pathlib import Path
out=Path('results');out.mkdir(exist_ok=True)
df=analyze(pd.read_csv('sample_feedback.csv'))
df.to_csv(out/'scored_feedback.csv',index=False)
fig,axs=plt.subplots(1,2,figsize=(11,4))
df.quality_score_0to5.value_counts().sort_index().reindex(range(6),fill_value=0).plot.bar(ax=axs[0],color='#3f6b84')
axs[0].set(title='Synthetic feedback quality distribution',xlabel='Heuristic score (0-5)',ylabel='Reviews')
axs[1].scatter(df.sentiment_compound,df.quality_score_0to5,color='#b25937',alpha=.7)
axs[1].set(title='Sentiment versus feedback quality',xlabel='VADER compound sentiment',ylabel='Heuristic score (0-5)')
fig.tight_layout();fig.savefig(out/'analysis.png',dpi=160)
