import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import boto3
import requests
from dateutil.relativedelta import relativedelta


API_URL = "https://data.transportation.gov/resource/az4n-8mr2.json"

BUCKET = os.environ.get("BUCKET", "spot-lakehouse-dev")
BRONZE_PREFIX = os.environ.get("BRONZE_PREFIX", "bronze/fmcsa/company_census")

LIMIT = 50000
LOCAL_FILE = Path("/tmp/company_census_monthly.jsonl")


def get_previous_month(run_date: datetime) -> tuple[str, str]:
    previous_month = run_date - relativedelta(months=1)
    return str(previous_month.year), f"{previous_month.month:02d}"


def get_month_date_range(year: str, month: str) -> tuple[str, str]:
    start_date = datetime(int(year), int(month), 1)

    next_month = start_date + relativedelta(months=1)

    start_yyyymmdd = start_date.strftime("%Y%m%d")
    end_yyyymmdd = next_month.strftime("%Y%m%d")

    return start_yyyymmdd, end_yyyymmdd


def fetch_page(start_date: str, end_date: str, offset: int) -> list[dict]:
    params = {
        "$limit": LIMIT,
        "$offset": offset,
        "$where": f"add_date >= '{start_date}' AND add_date < '{end_date}'",
    }

    response = requests.get(API_URL, params=params, timeout=60)

    if not response.ok:
        raise RuntimeError(
            f"API failed: {response.status_code} | URL: {response.url} | BODY: {response.text}"
        )

    return response.json()


def write_monthly_jsonl(year: str, month: str, start_date: str, end_date: str) -> int:
    ingested_at_utc = datetime.now(timezone.utc).isoformat()

    offset = 0
    row_count = 0

    with LOCAL_FILE.open("w", encoding="utf-8") as file:
        while True:
            records = fetch_page(start_date, end_date, offset)

            if not records:
                break

            for record in records:
                record["load_type"] = "monthly"
                record["source_year"] = year
                record["source_month"] = month
                record["ingested_at_utc"] = ingested_at_utc

                file.write(json.dumps(record) + "\n")
                row_count += 1

            offset += LIMIT
            time.sleep(0.25)

    return row_count


def upload_to_s3(year: str, month: str) -> str:
    s3 = boto3.client("s3")

    key = f"{BRONZE_PREFIX}/company_census_{year}_{month}.jsonl"

    s3.upload_file(
        Filename=str(LOCAL_FILE),
        Bucket=BUCKET,
        Key=key,
    )

    return key


def lambda_handler(event, context):
    run_date = datetime.now(timezone.utc)

    year, month = get_previous_month(run_date)
    start_date, end_date = get_month_date_range(year, month)

    row_count = write_monthly_jsonl(year, month, start_date, end_date)
    s3_key = upload_to_s3(year, month)

    return {
        "statusCode": 200,
        "load_type": "monthly",
        "target_year": year,
        "target_month": month,
        "start_date": start_date,
        "end_date": end_date,
        "row_count": row_count,
        "s3_uri": f"s3://{BUCKET}/{s3_key}",
    }