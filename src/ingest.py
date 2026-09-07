# ingest.py - downloads raw NHANES cycle files, untouched, into data/raw/.
import requests
from pathlib import Path


FILES = {
    "2013-2014": ["DEMO_H", "BMX_H", "DIQ_H"],
    "2015-2016": ["DEMO_I", "BMX_I", "DIQ_I"],
    "2017-2018": ["DEMO_J", "BMX_J", "DIQ_J"],
}

URL_TEMPLATE = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/{year}/DataFiles/{file}.xpt"


YEAR_MAP = {"2013-2014": "2013", "2015-2016": "2015", "2017-2018": "2017"}

RAW_DIR = Path("data/raw")


def download_all():
    for cycle, files in FILES.items():
        cycle_dir = RAW_DIR / cycle
        cycle_dir.mkdir(parents=True, exist_ok=True)  

        for file_code in files:
            url = URL_TEMPLATE.format(year=YEAR_MAP[cycle], file=file_code)
            dest = cycle_dir / f"{file_code}.xpt"

            if dest.exists():
                print(f"skip (already have): {dest}")
                continue

            print(f"downloading {url}")
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()          
            dest.write_bytes(resp.content)

    print("done.")


if __name__ == "__main__":
    download_all()
