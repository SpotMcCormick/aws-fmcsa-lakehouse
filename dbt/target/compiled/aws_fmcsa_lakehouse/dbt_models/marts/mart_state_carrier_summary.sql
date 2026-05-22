

select
    phy_state,
    business_org_type,
    add_year,

    count(distinct dot_number) as active_carrier_count,
    sum(total_drivers) as active_total_drivers,
    sum(power_units) as active_power_units

from "awsdatacatalog"."fmcsa"."stg_fmcsa"

where carrier_status = 'Active'
  and phy_state is not null
  and add_year is not null

group by
    phy_state,
    add_year,
    business_org_type