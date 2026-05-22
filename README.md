# AWS FMCSA Lakehouse

End-to-end AWS lakehouse project built around FMCSA carrier census data using a modern medallion architecture. The pipeline ingests raw transportation data from the FMCSA Socrata API into Amazon S3, transforms it into optimized Iceberg tables with dbt and Athena, and exposes analytical marts for Tableau reporting.

One of the primary goals of this project was to build and manage the cloud infrastructure manually instead of relying on ClickOps. All AWS resources (Lambda, IAM, EventBridge, S3, and Glue Catalog) were provisioned using Terraform to better understand infrastructure-as-code and serverless data engineering patterns.

---

## Project Overview

This project was designed to simulate a lightweight cloud lakehouse architecture using entirely serverless AWS services and open table formats.

The pipeline performs monthly ingestion of FMCSA carrier census data directly from the public Socrata API using AWS Lambda. Raw JSONL files are stored in an immutable bronze layer within Amazon S3.

Athena external tables expose the raw data for querying while dbt transforms the dataset into partitioned Iceberg tables stored as Parquet in the silver layer. Data marts are then built on top of the curated staging models for Tableau analytics and reporting.

The project focuses on practical data engineering concepts including:

- medallion architecture
- raw vs curated storage layers
- Iceberg table management
- partitioning strategy
- serverless ingestion patterns
- infrastructure as code
- analytical data modeling

---

## MVP

Tableau Interactive dashboard:

[FMCSA Tableau Dashboard](https://public.tableau.com/app/profile/jeremy.mccormick/viz/FMCSA_17794641692300/FMCSASummary)

---

## Architecture

```text
FMCSA API
    ↓
AWS Lambda
    ↓
S3 Bronze Layer (Raw JSONL)
    ↓
Athena External Table
    ↓
dbt + Athena Iceberg Models
    ↓
Silver / Analytics Layer
    ↓
Business Marts
    ↓
Tableau Dashboard
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Infrastructure | Terraform |
| Ingestion | AWS Lambda, Python |
| Storage | Amazon S3 |
| Query Engine | Amazon Athena |
| Table Format | Apache Iceberg |
| Transformations | dbt |
| Catalog | AWS Glue Catalog |
| Visualization | Tableau Public |

---

## Data Flow

### Bronze Layer

Raw monthly FMCSA API payloads are ingested as JSONL files into Amazon S3 using AWS Lambda.

Example:

```text
s3://spot-lakehouse-dev/bronze/fmcsa/company_census/
```

### Silver Layer

dbt transforms the raw external Athena table into curated Apache Iceberg tables optimized for analytical workloads.

Transformations include:

- type casting
- business status normalization
- date parsing
- derived year/month partition fields
- organizational type standardization

### Data Mart Layer

Analytical marts aggregate carrier activity metrics by:

- state
- business organization type
- reporting year

Metrics include:

- active carrier counts
- total drivers
- total power units

---

## Infrastructure

Terraform provisions:

- S3 lakehouse bucket
- Lambda function
- IAM roles and policies
- EventBridge monthly scheduling
- Glue Catalog database