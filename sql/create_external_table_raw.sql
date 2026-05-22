/*
Creates an Athena external table over the raw FMCSA company census JSONL files
stored in the bronze S3 layer.

This table does not transform or copy data. It provides schema metadata so Athena
can query the raw JSON records. dbt will read from this bronze table and create
a cleaned Iceberg/Parquet staging table in the silver layer.
*/

CREATE EXTERNAL TABLE fmcsa.bronze_company_census_raw (
    mcs150_date string,
    add_date bigint,
    status_code string,
    dot_number bigint,
    dba_name string,
    legal_name string,
    phy_city string,
    phy_state string,
    phy_zip string,
    carrier_operation string,
    business_org_desc string,
    power_units bigint,
    total_drivers bigint,
    mcs150_mileage bigint,
    mcs150_mileage_year bigint,
    load_type string,
    ingested_at_utc string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
    'case.insensitive'='TRUE'
)
LOCATION 's3://spot-lakehouse-dev/bronze/fmcsa/company_census/';