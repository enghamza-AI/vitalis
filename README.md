# vitalis

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![scikit--learn](https://img.shields.io/badge/scikit--learn-1.4-orange)
![pandas](https://img.shields.io/badge/pandas-2.x-150458)
![Streamlit](https://img.shields.io/badge/Streamlit-app-FF4B4B)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

A health-outcome classifier trained on real CDC NHANES survey data — three survey-year cohorts, reconciled schema drift, and survey weighting handled properly instead of ignored.

## Why this is harder than a clean CSV

NHANES isn't a census — it's a stratified, multistage survey that deliberately oversamples specific groups, so each respondent row represents a different number of real people. That's what the survey weight column encodes, and dropping it silently biases any model trained on the data toward whichever groups NHANES happened to oversample.

On top of that, NHANES data is released in two-year cycles, and CDC revises its questionnaires and lab methods between cycles. Combining multiple cycles means reconciling files that don't share identical column names for the same underlying variables — a realistic stand-in for "an upstream data source changed its schema on you," rather than the fixed, pre-cleaned CSV most ML tutorials start from.

vitalis pulls three NHANES survey-year cohorts, reconciles the schema drift between them, and trains three classic classifiers on the result — with cross-validated, variance-reported evaluation instead of a single train/test split, which is especially important on complex-survey data where a naive random split can misrepresent performance.

## Algorithms

Three classic supervised classifiers, via `scikit-learn`:

- **K-Nearest Neighbors** (`KNeighborsClassifier`)
- **Naive Bayes** (`GaussianNB` / `CategoricalNB`)
- **Decision Trees** (`DecisionTreeClassifier`)

Each is evaluated with stratified k-fold cross-validation, reporting both mean and variance across folds. Alongside the main pipeline, `notebooks/side_experiments/` contains small hand-derived versions of each algorithm on toy data, worked through manually to understand what each `scikit-learn` call is doing internally — these are for understanding, not part of the trained pipeline.

## Dataset

[NHANES](https://wwwn.cdc.gov/nchs/nhanes/) (National Health and Nutrition Examination Survey), CDC/NCHS — demographics, body measures, and questionnaire data pulled across the 2015–2016, 2017–2018, and 2019–2020 survey cycles.

## Setup

```bash
git clone https://github.com/enghamza-AI/vitalis.git
cd vitalis
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_pipeline.py
```

## Try it live

🔗 [Streamlit app](https://share.streamlit.io/) — *link goes live after deployment*

## License

MIT
