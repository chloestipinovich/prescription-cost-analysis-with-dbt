-- models/stg_prescription_costs_24_25.sql
{{ config(materialized='table') }}

select
    YEAR_DESC::string as year_desc,
    REGION_NAME::string as region_name,
    REGION_CODE::string as region_code,
    ICB_NAME::string as icb_name,
    ICB_CODE::string as icb_code,
    BNF_PRESENTATION_CODE::string as bnf_presentation_code,
    BNF_PRESENTATION_NAME::string as bnf_presentation_name,
    SNOMED_CODE::string as snomed_code,  -- if very large, use varchar
    SUPPLIER_NAME::string as supplier_name,
    UNIT_OF_MEASURE::string as unit_of_measure,
    GENERIC_BNF_EQUIVALENT_CODE::string as generic_bnf_equivalent_code,
    GENERIC_BNF_EQUIVALENT_NAME::string as generic_bnf_equivalent_name,
    BNF_CHEMICAL_SUBSTANCE_CODE::string as bnf_chemical_substance_code,
    BNF_CHEMICAL_SUBSTANCE::string as bnf_chemical_substance,
    BNF_PARAGRAPH_CODE::string as bnf_paragraph_code,
    BNF_PARAGRAPH::string as bnf_paragraph,
    BNF_SECTION_CODE::string as bnf_section_code,
    BNF_SECTION::string as bnf_section,
    BNF_CHAPTER_CODE::string as bnf_chapter_code,
    BNF_CHAPTER::string as bnf_chapter,
    PREP_CLASS::string as prep_class,
    PRESCRIBED_PREP_CLASS::string as prescribed_prep_class,
    CAST(ITEMS as integer) as items,
    CAST(TOTAL_QUANTITY as integer) as total_quantity,
    CAST(NIC as double) as nic,
    CAST(NIC_PER_ITEM as double) as nic_per_item,
    CAST(NIC_PER_QUANTITY as double) as nic_per_quantity,
    CAST(QUANTITY_PER_ITEM as double) as quantity_per_item,
    PHARMACY_ADVANCED_SERVICE::string as pharmacy_advanced_service
from {{ ref('pca_icb_snomed_2024_2025') }}
