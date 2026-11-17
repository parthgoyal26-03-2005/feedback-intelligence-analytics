import pandas as pd
import pytest
from analysis import analyze

def data(texts):
    return pd.DataFrame({'review_id':[str(i) for i in range(len(texts))], 'reviewer_id':['x']*len(texts), 'garment':['shirt']*len(texts), 'review_text':texts})
def test_quality_and_sentiment_are_separate():
    out=analyze(data(['Love it!', 'The shoulder seam pulls when I raise my arms; a wider shoulder panel could improve comfort.']))
    assert out.quality_score_0to5.iloc[1] > out.quality_score_0to5.iloc[0]
def test_missing_and_duplicate():
    out=analyze(data([' Nice  shirt ', 'nice shirt', None, None]))
    assert out.duplicate_review.tolist()==[False,True,False,False]
    assert out.missing_review.sum()==2 and pd.isna(out.quality_score_0to5.iloc[2])
def test_schema_and_unique_ids():
    with pytest.raises(ValueError): analyze(pd.DataFrame({'review_text':['ok']}))
    d=data(['a','b']);d.loc[1,'review_id']='0'
    with pytest.raises(ValueError): analyze(d)
def test_sentiment_sign():
    out=analyze(data(['I love this!', 'I hate this!']))
    assert list(out.sentiment)==['positive','negative']
