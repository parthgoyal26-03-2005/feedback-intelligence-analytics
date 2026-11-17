import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from analysis import analyze
st.set_page_config(page_title='Feedback Intelligence', layout='wide')
st.title('Feedback Intelligence')
st.caption('Educational synthetic-data demonstration. Heuristic scores are not validated human judgments.')
upload=st.file_uploader('Upload a CSV',type=['csv'])
try:
    source=pd.read_csv(upload if upload else 'sample_feedback.csv')
    df=analyze(source)
    st.write(f"{len(df)} records | {df.missing_review.sum()} missing reviews | {df.duplicate_review.sum()} repeated reviews")
    st.subheader('Scored records')
    st.dataframe(df, hide_index=True)
    st.download_button('Download scored CSV', df.to_csv(index=False).encode('utf-8'), 'scored_feedback.csv', 'text/csv')
    st.subheader('Explore feedback')
    fig,axs=plt.subplots(1,2,figsize=(12,4))
    df['quality_score_0to5'].value_counts().sort_index().reindex(range(6),fill_value=0).plot.bar(ax=axs[0],color='#3f6b84')
    axs[0].set(title='Heuristic quality distribution',xlabel='Quality score (0-5)',ylabel='Reviews')
    valid=df.dropna(subset=['quality_score_0to5','sentiment_compound'])
    axs[1].scatter(valid['sentiment_compound'],valid['quality_score_0to5'],alpha=.65,color='#b25937')
    axs[1].set(title='Sentiment and feedback quality',xlabel='VADER compound sentiment',ylabel='Heuristic quality (0-5)')
    fig.tight_layout();st.pyplot(fig)
    st.write('Average score by garment category',df.groupby('garment')['quality_score_0to5'].mean().round(2))
    st.write('Sentiment counts',df['sentiment'].value_counts())
except (ValueError, pd.errors.ParserError, UnicodeDecodeError) as exc:
    st.error(str(exc))
