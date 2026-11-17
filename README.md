# Feedback Intelligence

An independent educational exploration of garment-review informativeness, inspired by the Try5 problem description. This project is not affiliated with Pixophilia or Try5, and no real participant or proprietary data is used.

## Question and approach
Can review informativeness be estimated separately from emotional sentiment? A detailed complaint can contain more useful evidence than a generic compliment. `baseline.py` scores aspect coverage (0-2), detail cues (0-1), suggestion cues (0-1), and length (0-1), less a repeated-text penalty, clipped to 0-5. `analysis.py` adds VADER sentiment independently, schema checks, normalization, missing and duplicate flags. `app.py` displays records, distributions, categories and CSV export. The baseline and synthetic sample were adapted from the supplied Try5-style Feedback Quality Baseline practice ZIP; the application and validation extend that starter.

## Data and limitations
`sample_feedback.csv` is the supplied synthetic practice dataset, not a real survey. Its illustrative quality field is not independent human annotation and is not used for model evaluation. No trained model or performance claim is made: the sample is too small and labels do not establish independent ground truth. A proper study requires independently annotated diverse examples, multiple raters, agreement measurement and participant-separated held-out evaluation. Keyword heuristics miss synonyms and context, can reward verbosity, interpret suggestion words incorrectly, penalize legitimate repeated observations, and are English-centric. VADER can miss domain-specific sentiment or sarcasm. Neither score proves honesty, usefulness, or real-world validity. Missing reviews have no quality score. Repeated normalized text is flagged after the first occurrence, not automatically removed. No image, audio, or video analysis is implemented.

## Setup and usage
Python 3.10-3.12 recommended. From this folder:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
pytest -q
```

Upload UTF-8 CSV with unique nonempty `review_id`, `reviewer_id`, `garment`, and `review_text` columns. Empty text is retained and marked missing. Avoid uploading sensitive participant data to untrusted environments. Quality and sentiment are independent measures, not ground truth. Use the download button to export scored rows.

## Next steps
Collect consented data, separately annotate relevance, specificity and actionability, compare an interpretable heuristic with a TF-IDF baseline on participant-separated data, and audit errors across groups and modalities.

## Reproducible sample output
`python make_results.py` produces `results/scored_feedback.csv` and `results/analysis.png`. On the included 18 synthetic records the pipeline flags 0 missing reviews and 1 repeated text. Quality counts from 0 through 5 are 5, 2, 1, 0, 2 and 8; VADER categories are 13 positive, 4 negative and 1 neutral. These describe this synthetic sample only and do not measure prediction accuracy.
