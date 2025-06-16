{{ config(materialized='view') }}

WITH region_nic AS (
    SELECT
        REGION_NAME,
        SUM(total_nic) AS nic_by_region
    FROM {{ ref('icb_nic_summary') }}
    GROUP BY REGION_NAME
),

region_with_percentage AS (
    SELECT
        *,
        ROUND(
            nic_by_region * 100.0 / SUM(nic_by_region) OVER (),
            2
        ) AS percentage_of_total_nic
    FROM region_nic
)

SELECT *
FROM region_with_percentage
ORDER BY nic_by_region DESC
