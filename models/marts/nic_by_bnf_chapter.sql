{{ config(materialized='view') }}

WITH chapter_nic AS (
    SELECT
        BNF_CHAPTER,
        SUM(total_nic) AS nic_by_chapter
    FROM {{ ref('bnf_nic_summary') }}
    GROUP BY  BNF_CHAPTER
),

chapter_with_percentage AS (
    SELECT
        *,
        ROUND(
            nic_by_chapter * 100.0 / SUM(nic_by_chapter) OVER (),
            4
        ) AS percentage_of_total_nic
    FROM chapter_nic
)

SELECT *
FROM chapter_with_percentage
ORDER BY nic_by_chapter DESC
