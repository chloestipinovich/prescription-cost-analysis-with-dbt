{{ config(materialized='view') }}

WITH icb_nic AS (
    SELECT
        REGION_NAME, ICB_NAME,
        SUM(total_nic) AS nic_by_icb
    FROM {{ ref('icb_nic_summary') }}
    GROUP BY REGION_NAME, ICB_NAME
),

icb_with_percentage AS (
    SELECT
        *,
        ROUND(
            nic_by_icb * 100.0 / SUM(nic_by_icb) OVER (),
            4
        ) AS percentage_of_total_nic
    FROM icb_nic
)

SELECT *
FROM icb_with_percentage
ORDER BY nic_by_icb DESC
