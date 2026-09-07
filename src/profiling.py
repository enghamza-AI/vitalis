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


if __name__ == "__main__":
    profile_all()
