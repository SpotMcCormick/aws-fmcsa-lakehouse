from datetime import datetime, timezone
from pathlib import Path

import boto3
import polars as pl


BUCKET = "spot-lakehouse-dev"

LOCAL_CSV_PATH = Path("data/company_census.csv")
LOCAL_JSONL_PATH = Path("data/company_census_2026_03.jsonl")

SNAPSHOT_YEAR = "2026"
SNAPSHOT_MONTH = "03"
SNAPSHOT_AS_OF_DATE = "2026-03-31"
LOAD_TYPE = "initial"


S3_KEY = f"bronze/fmcsa/company_census/company_census_{SNAPSHOT_YEAR}_{SNAPSHOT_MONTH}.jsonl"



def csv_to_jsonl() -> int:
    ingested_at_utc = datetime.now(timezone.utc).isoformat()

    df = pl.read_csv(
        LOCAL_CSV_PATH,
        infer_schema_length=10000,
        ignore_errors=True,
    )

    df = df.with_columns(
        pl.lit(LOAD_TYPE).alias("load_type"),
        pl.lit(SNAPSHOT_YEAR).alias("snapshot_year"),
        pl.lit(SNAPSHOT_MONTH).alias("snapshot_month"),
        pl.lit(SNAPSHOT_AS_OF_DATE).alias("snapshot_as_of_date"),
        pl.lit(ingested_at_utc).alias("ingested_at_utc"),
    )

    LOCAL_JSONL_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.write_ndjson(LOCAL_JSONL_PATH)

    return df.height


def upload_to_s3() -> None:
    s3 = boto3.client("s3")
    s3.upload_file(str(LOCAL_JSONL_PATH), BUCKET, S3_KEY)


def main() -> None:
    row_count = csv_to_jsonl()
    upload_to_s3()

    print(f"Converted {row_count:,} rows")
    print(f"Uploaded to s3://{BUCKET}/{S3_KEY}")


if __name__ == "__main__":
    main()