# profiling.py — profile each raw file independently before any merge.


import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")


def profile_file(path: Path) -> dict:
    df = pd.read_sas(path, format="xport")

    profile = {
        "file": path.name,
        "n_rows": len(df),
        "n_cols": df.shape[1],
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "n_unique_SEQN": df["SEQN"].nunique() if "SEQN" in df.columns else None,
        "pct_null_per_col": (df.isnull().mean() * 100).round(2).to_dict(),
    }
    return profile


def profile_all():
    results = {}
    for cycle_dir in sorted(RAW_DIR.iterdir()):
        if not cycle_dir.is_dir():
            continue
        for xpt_file in sorted(cycle_dir.glob("*.xpt")):
            key = f"{cycle_dir.name}/{xpt_file.stem}"
            results[key] = profile_file(xpt_file)
            p = results[key]
            print(f"\n=== {key} ===")
            print(f"rows: {p['n_rows']}, cols: {p['n_cols']}, unique SEQN: {p['n_unique_SEQN']}")
    return results

# catching schema drift - 
def diff_columns_across_cycles(file_stub: str, cycle_to_suffix: dict):

    col_sets = {}
    for cycle, suffix in cycle_to_suffix.items():
        path = RAW_DIR / cycle / f"{file_stub}_{suffix}.xpt"
        df = pd.read_sas(path, format="xport")
        col_sets[cycle] = set(df.columns)

    all_cols = set.union(*col_sets.values())
    common_cols = set.intersection(*col_sets.values())
    drifted = all_cols - common_cols

    print(f"\n{file_stub}: {len(common_cols)} columns common to all 3 cycles")
    print(f"{file_stub}: {len(drifted)} columns NOT present in all cycles (schema drift):")
    for col in sorted(drifted):
        present_in = [c for c, cols in col_sets.items() if col in cols]
        print(f"  {col}: present in {present_in}")


SUFFIX_MAP = {"2013-2014": "H", "2015-2016": "I", "2017-2018": "J"}

if __name__ == "__main__":
    profile_all()
    for stub in ["DEMO", "BMX", "DIQ"]:
        diff_columns_across_cycles(stub, SUFFIX_MAP)

