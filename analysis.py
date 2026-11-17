"""Clean and score synthetic feedback; this is a heuristic, not a validated model."""
import re
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from baseline import score_review

REQUIRED = {'review_id', 'reviewer_id', 'garment', 'review_text'}

def analyze(frame):
    missing = REQUIRED - set(frame.columns)
    if missing: raise ValueError('Missing columns: ' + ', '.join(sorted(missing)))
    if frame.empty: raise ValueError('The CSV has no rows.')
    df = frame.copy()
    for col in REQUIRED: df[col] = df[col].fillna('').astype(str).str.strip()
    if (df['review_id'] == '').any() or df['review_id'].duplicated().any():
        raise ValueError('review_id must be present and unique.')
    df['missing_review'] = df['review_text'].eq('')
    df['normalized_text'] = df['review_text'].str.lower().str.replace(r'\s+', ' ', regex=True).str.strip()
    # Empty answers are missing, not duplicates.
    df['duplicate_review'] = df['normalized_text'].duplicated() & ~df['missing_review']
    analyzer = SentimentIntensityAnalyzer()
    records=[]
    for row in df.itertuples(index=False):
        score=score_review(row.review_text, row.duplicate_review)
        polarity=analyzer.polarity_scores(row.review_text)['compound'] if row.review_text else None
        score['sentiment_compound']=polarity
        score['sentiment'] = ('missing' if polarity is None else 'positive' if polarity >= .05 else 'negative' if polarity <= -.05 else 'neutral')
        records.append(score)
    for key in records[0]: df[key]=[r[key] for r in records]
    # No score is asserted for missing feedback.
    df.loc[df['missing_review'], 'quality_score_0to5'] = None
    return df
