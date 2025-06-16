{{ config(materialized='view') }}

WITH section_nic AS (
    SELECT
        BNF_CHAPTER,
        BNF_SECTION,
        SUM(total_nic) AS nic_by_section
    FROM {{ ref('bnf_nic_summary') }}
    GROUP BY  BNF_CHAPTER, BNF_SECTION
),

section_with_percentage AS (
    SELECT
        *,
        ROUND(
            nic_by_section * 100.0 / SUM(nic_by_section) OVER (),
            6
        ) AS percentage_of_total_nic
    FROM section_nic
)

SELECT *
FROM section_with_percentage
ORDER BY nic_by_section DESC

