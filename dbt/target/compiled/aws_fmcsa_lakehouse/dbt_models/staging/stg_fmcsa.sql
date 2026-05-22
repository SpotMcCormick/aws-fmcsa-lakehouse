

with source as (

    select *
    from "awsdatacatalog"."fmcsa"."bronze_company_census_raw"

),

cleaned as (

    select
        cast(dot_number as bigint) as dot_number,

        legal_name,
        dba_name,

        status_code,

        case
            when status_code = 'A' then 'Active'
            when status_code = 'I' then 'Inactive'
            else 'Other'
        end as carrier_status,

        phy_city,
        phy_state,
        phy_zip,

        carrier_operation,

        cast(business_org_id as integer) as business_org_id,

        case
            when cast(business_org_id as integer) = 1 then 'Individual'
            when cast(business_org_id as integer) = 2 then 'Partnership'
            when cast(business_org_id as integer) = 3 then 'Corporation'
            else coalesce(business_org_desc, 'Other')
        end as business_org_type,

        business_org_desc,

        cast(power_units as integer) as power_units,
        cast(total_drivers as integer) as total_drivers,
        cast(mcs150_mileage as bigint) as mcs150_mileage,
        cast(mcs150_mileage_year as integer) as mcs150_mileage_year,

        mcs150_date as mcs150_date_raw,

        cast(date_parse(cast(add_date as varchar), '%Y%m%d') as date) as add_date,
        cast(substr(cast(add_date as varchar), 1, 4) as integer) as add_year,
        cast(substr(cast(add_date as varchar), 5, 2) as integer) as add_month,

        load_type,
        from_iso8601_timestamp(ingested_at_utc) as ingested_at_utc

    from source
    where add_date is not null
      and dot_number is not null

)

select *
from cleaned