"""Educational baseline for feedback usefulness; not a validated or trained ML model.

Usage: python analyze_feedback.py --input sample_feedback.csv --output results
"""
from __future__ import annotations
import argparse,csv,json,re,collections,statistics
from pathlib import Path

ASPECTS = {
    'fit': {'fit','size','shoulder','sleeve','waist','waistband','cuff','collar','tight','loose','length','shorter','wider','narrow'},
    'fabric': {'fabric','cotton','material','lining','stitching','seam','button','zipper','zip','pocket','wash','shrinkage'},
    'comfort': {'comfort','comfortable','uncomfortable','soft','scratches','rub','rubs','itchy','breathable','heat','walking','sitting','movement'},
    'design': {'color','colour','design','hem','neck','opening','placement','look','looks'},
}
DETAIL_WORDS = {'when','after','because','during','roughly','around','about','minutes','cm','sitting','walking','movement','skin','wrist','knee','arms','phone','washing','wash'}
ACTION_WORDS = {'recommend','suggest','consider','could','should','improve','wider','softer','shortening','shorter','extra','reduce','more','less','check'}

def tokenize(s): return re.findall(r"[a-z]+|\d+",s.lower())

def score_review(text:str,duplicate:bool=False)->dict:
    tokens=tokenize(text)
    wordset=set(tokens)
    aspect_hits={aspect:sorted(words & wordset) for aspect,words in ASPECTS.items() if words & wordset}
    n=len(tokens)
    aspect_pts=min(2,len(aspect_hits))      # 0-2: breadth of relevant detail
    detail_pts=int(len(wordset & DETAIL_WORDS)>=2 or any(t.isdigit() for t in tokens))
    action_pts=int(bool(wordset & ACTION_WORDS))
    length_pts=int(n>=16)
    penalty=int(duplicate)                   # only repeated text receives penalty
    score=max(0,min(5,aspect_pts+detail_pts+action_pts+length_pts-penalty))
    return {'quality_score_0to5':score,'word_count':n,'aspects_detected':','.join(aspect_hits),
            'detail_evidence':bool(detail_pts),'actionable_evidence':bool(action_pts),
            'duplicate_review':duplicate}

def process(src:Path,out_dir:Path)->dict:
    rows=list(csv.DictReader(src.open(encoding='utf-8-sig',newline='')))
    if not rows: raise ValueError('Input CSV is empty')
    required={'review_id','review_text','garment'}
    if not required.issubset(rows[0]): raise ValueError('Missing columns: '+', '.join(sorted(required-set(rows[0]))))
    out_dir.mkdir(parents=True,exist_ok=True)
    seen=set(); scored=[]
    for row in rows:
        norm=' '.join(tokenize(row['review_text']))
        is_duplicate=norm in seen
        seen.add(norm)
        scored.append({**row,**score_review(row['review_text'],is_duplicate)})
    with (out_dir/'scored_feedback.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(scored[0]));writer.writeheader();writer.writerows(scored)
    vals=[int(r['quality_score_0to5']) for r in scored]
    summary={'n_reviews':len(scored),'mean_heuristic_quality':round(statistics.mean(vals),2),
             'quality_distribution':{str(i):vals.count(i) for i in range(6)},
             'n_duplicates':sum(r['duplicate_review'] for r in scored),
             'note':'Synthetic reviews. Heuristic baseline, not calibrated or validated against a representative dataset. Positive/negative polarity is intentionally not a quality feature.'}
    (out_dir/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    # Basic chart only if matplotlib is available; core pipeline has no third-party deps.
    try:
        import matplotlib.pyplot as plt
        fig,ax=plt.subplots(figsize=(6.4,3.7))
        ax.bar(list(range(6)),[vals.count(i) for i in range(6)])
        ax.set(xlabel='Heuristic usefulness score (0-5)',ylabel='Number of reviews',title='Synthetic feedback quality distribution')
        fig.tight_layout();fig.savefig(out_dir/'distribution.png',dpi=180);plt.close(fig)
    except ImportError: pass
    return summary

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,default=Path('sample_feedback.csv'))
    parser.add_argument('--output',type=Path,default=Path('results'))
    args=parser.parse_args();print(json.dumps(process(args.input,args.output),indent=2))
