{{ config(materialized='view') }}

WITH paragraph_nic AS (
    SELECT
        BNF_CHAPTER,
        BNF_SECTION,
        BNF_PARAGRAPH,
        SUM(total_nic) AS nic_by_paragraph
    FROM {{ ref('bnf_nic_summary') }}
    GROUP BY  BNF_CHAPTER, BNF_SECTION, BNF_PARAGRAPH
),

paragraph_with_percentage AS (
    SELECT
        *,
        ROUND(
            nic_by_paragraph * 100.0 / SUM(nic_by_paragraph) OVER (),
            8
        ) AS percentage_of_total_nic
    FROM paragraph_nic
)

SELECT *
FROM paragraph_with_percentage
ORDER BY nic_by_paragraph DESC

