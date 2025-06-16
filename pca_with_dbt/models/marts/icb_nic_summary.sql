{{ config(materialized='table') }}

SELECT
    REGION_NAME,
    REGION_CODE,
    ICB_NAME,
    ICB_CODE,
    SUM(CAST(NIC AS DOUBLE)) AS total_nic
FROM {{ ref('stg_prescription_costs_24_25') }}
GROUP BY REGION_NAME, REGION_CODE, ICB_NAME, ICB_CODE,
ORDER BY total_nic DESC
