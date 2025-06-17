import plotly.graph_objects as go
import duckdb
import pandas as pd
import streamlit as st
from matplotlib import cm

from pyecharts import options as opts
from pyecharts.charts import Pie
from streamlit_echarts import st_pyecharts

# Set up the page
st.set_page_config(page_title="NIC Dashboard", layout="wide")

st.markdown("""
    <style>
    div.stButton > button:first-child {
        font-size: 24px;
        padding: 12px 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Color mapping
region_colors = {
    "MIDLANDS": "#dd4345",
    "NORTH EAST AND YORKSHIRE": "#377eb8",
    "SOUTH EAST": "#4daf4a",
    "NORTH WEST": "#984ea3",
    "EAST OF ENGLAND": "#ff7f00",
    "LONDON": "#e78ac3",
    "SOUTH WEST": "#66c2a5"
}

# --- Cache and load data ---
@st.cache_data
def get_data():
    with duckdb.connect("pca_with_dbt.duckdb") as conn:
        nic_by_region = conn.execute("SELECT * FROM nic_by_icb_regions").fetchdf()
        nic_by_icb = conn.execute("SELECT * FROM nic_by_icb").fetchdf()
        nic_by_bnf_chapter = conn.execute("SELECT * FROM nic_by_bnf_chapter").fetchdf()
        nic_by_bnf_section = conn.execute("SELECT * FROM nic_by_bnf_section").fetchdf()
        nic_by_bnf_paragraph = conn.execute("SELECT * FROM nic_by_bnf_paragraph").fetchdf()
    return nic_by_region, nic_by_icb, nic_by_bnf_chapter, nic_by_bnf_section, nic_by_bnf_paragraph

nic_by_region, nic_by_icb, nic_by_bnf_chapter, nic_by_bnf_section, nic_by_bnf_paragraph = get_data()

# --- Navigation State ---
if "page" not in st.session_state:
    st.session_state.page = "Introduction"

# --- Sidebar Navigation Buttons ---
with st.sidebar:
    st.title("Navigation")
    if st.button("Introduction", use_container_width=True):
        st.session_state.page = "Introduction"
    if st.button("By British National Formulary", use_container_width=True):
        st.session_state.page = "BNF"
    if st.button("By Region", use_container_width=True):
        st.session_state.page = "Regions"

# --- Page Content ---

# --- INTRODUCTION ---
if st.session_state.page == "Introduction":
    st.title("NHS Prescription Cost Analysis Dashboard")
    st.header("2024/2025 Financial Year")
    st.write("")
    st.write("")
    st.subheader("🚀 Project Goal")
    st.markdown("""
    <p style="font-size:18px">
    This project was created to gain hands-on experience using <strong>dbt (data build tool)</strong>, a modern analytics engineering framework for transforming raw data into clean, reliable datasets. The Streamlit app you're viewing is just the user-facing layer. Behind the scenes, I set up a modular and scalable dbt project that includes well-structured staging models and testable transformation logic to ensure data quality and maintainability.
    </p>

    <p style="font-size:18px">
    The full project code, including all dbt models, sources, documentation, and this Streamlit app, is available on <a href="https://github.com/chloestipinovich/prescription-cost-analysis-with-dbt" target="_blank">my GitHub page</a>.
    </p>
    """, unsafe_allow_html=True)

    st.subheader("📊 About the Data")
    st.markdown("""
    <p style="font-size:18px">
    The data in this dashboard comes from the <strong>NHS Business Services Authority (NHSBSA)</strong>'s annual <strong>Prescription Cost Analysis (PCA)</strong> release. This dataset is an <strong>Official Statistic</strong> with <strong>National Statistics designation</strong>.
    </p>

    <p style="font-size:18px">
    It includes comprehensive information on all <strong>prescription items dispensed in community settings across England</strong>, based on reimbursement claims submitted to the NHSBSA. The data covers both <strong>financial and calendar years</strong>, and provides the most detailed level available, including item counts and associated costs.
    </p>

    <p style="font-size:18px">
    As of recent publications, it also incorporates data for items supplied through the <strong>Pharmacy First Clinical Pathways advanced service</strong>.
    </p>

    <p style="font-size:18px">
    <a href="https://opendata.nhsbsa.net/" target="_blank">Visit the NHSBSA Open Data Portal</a><br>
    <a href="https://opendata.nhsbsa.net/dataset/prescription-cost-analysis-pca-annual-statistics/resource/b8cf68a5-4a93-4940-a5c1-4064bc947ffb" target="_blank">Go directly to the PCA Annual Statistics Dataset</a>
    </p>
    """, unsafe_allow_html=True)

    st.subheader("🗂️ Glossary")
    glossary_html = """
    <table style="font-size:18px; border-collapse: collapse;">
    <tr>
        <th style="text-align:left; padding: 8px; border-bottom: 2px solid #ddd;">Acronym</th>
        <th style="text-align:left; padding: 8px; border-bottom: 2px solid #ddd;">Meaning</th>
    </tr>
    <tr>
        <td style="padding: 8px; border-bottom: 1px solid #ddd;">BNF</td>
        <td style="padding: 8px; border-bottom: 1px solid #ddd;">British National Formulary Code</td>
    </tr>
    <tr>
        <td style="padding: 8px; border-bottom: 1px solid #ddd;">SNOMED</td>
        <td style="padding: 8px; border-bottom: 1px solid #ddd;">Systemised Nomenclature of Medical Terms Code</td>
    </tr>
    <tr>
        <td style="padding: 8px;">NIC</td>
        <td style="padding: 8px;">Net Ingredient Cost</td>
    </tr>
    <tr>
        <td style="padding: 8px;">BSA</td>
        <td style="padding: 8px;">Business Services Authority</td>
    </tr>
    <tr>
        <td style="padding: 8px;">PCA</td>
        <td style="padding: 8px;">Prescription Cost Analysis</td>
    </tr>
    </table>
    """

    st.markdown(glossary_html, unsafe_allow_html=True)

    st.write("NHS Business Services Authority. Prescription Cost Analysis England 2024/25. Available at: https://www.nhsbsa.nhs.uk/statistical-collections/prescription-cost-analysis-england (Accessed: June 2025).")




# --- REGIONS ---
elif st.session_state.page == "Regions":
    # st.title("Net Ingredient Cost by Region and Integrated Care Board")
    st.markdown("<h1>Net Ingredient Cost by<br>Region and Integrated Care Board</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background-color: #e9f5ff;
        padding: 15px;
        border-radius: 5px;
        font-size: 20px;
        font-style: italic;
        color: #084298;
        margin-bottom: 20px;
    ">
    The <b>Net Ingredient Cost (NIC)</b> is measured in British Pounds Sterling (GBP), and reflects the amount that would be paid using the basic price of the prescribed drug or appliance and the quantity prescribed. For more information see the
    <a href="https://www.nhsbsa.nhs.uk/statistical-collections/prescription-cost-analysis-england" target="_blank" style="color:#084298; text-decoration: underline;">
    NHSBSA website</a>.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="
        background-color: #fff8de;
        padding: 15px;
        border-radius: 5px;
        font-size: 20px;
        font-style: italic;
        color: #614d02;
        margin-bottom: 20px;
    ">
     <b>Integrated Care Boards (ICBs)</b> are NHS organisations responsible for planning and commissioning healthcare services in their local areas. They work closely with partners to improve health outcomes. For more details, visit the 
    <a href="https://www.england.nhs.uk/integratedcare/integrated-care-boards/" target="_blank" style="color:#614d02; text-decoration: underline;">
    NHS England Integrated Care Boards page</a>.
    </div>
    """, unsafe_allow_html=True)

    col4, col5 = st.columns([1, 1])
    with col4:
        show_region = st.button("🌍 Regions", use_container_width=True)
    with col5:
        show_icb = st.button("🚑 Integrated Care Boards", use_container_width=True)


    st.write("---")

    if show_region or not any([show_icb]):

        nic_by_region["color"] = nic_by_region["region_name"].map(region_colors)
        nic_by_region = nic_by_region.sort_values("percentage_of_total_nic", ascending=True)

        fig_region = go.Figure(go.Bar(
            y=nic_by_region["region_name"],
            x=nic_by_region["percentage_of_total_nic"],
            orientation='h',
            marker_color=nic_by_region["color"],
            text=nic_by_region["percentage_of_total_nic"].round(2),
            textposition='outside'
        ))
        fig_region.update_layout(
            title="",
            xaxis_title="Percentage of Total Net Ingredient Cost",
            yaxis_title="",
            height=500,
            margin=dict(l=150, r=50, t=50, b=50)
        )
        st.subheader("Percentage of Total NIC by Region")
        st.markdown("""
        <h4 style="color: #777777;">
            2024/2025 Financial Year
        </h4>
        """, unsafe_allow_html=True)
        st.plotly_chart(fig_region, use_container_width=True)

    elif show_icb:
        st.subheader("Percentage of Total NIC by ICB")
        st.markdown("""
        <h4 style="color: #777777;">
            2024/2025 Financial Year
        </h4>
        """, unsafe_allow_html=True)
        st.write("")
        nic_by_icb["color"] = nic_by_icb["region_name"].map(region_colors)
        nic_by_icb = nic_by_icb.sort_values("percentage_of_total_nic", ascending=False)

        display_cols = ["icb_name", "region_name", "percentage_of_total_nic"]
        df = nic_by_icb[display_cols].rename(columns={
            "icb_name": "ICB",
            "region_name": "Region",
            "percentage_of_total_nic": "Percent of Total NIC"
        })

        df["Percent of Total NIC"] = df["Percent of Total NIC"].round(2).astype(str) + "%"

        # Reset index so it won't be displayed
        df_reset = df.reset_index(drop=True)

        styled_df = (
            df_reset.style
            .set_table_styles([
                {'selector': 'th', 'props': [('font-weight', 'bold')]},
                {'selector': 'td:nth-child(4)', 'props': [('text-align', 'center')]},
                {'selector': 'th:nth-child(4)', 'props': [('text-align', 'center')]},
            ])
        )

        st.markdown(styled_df.to_html(), unsafe_allow_html=True)


# Add this to your script (outside the function ideally)
section_descriptions = {
    "Endocrine System": "Hormones, anti‑diabetics, thyroid agents",
    "Central Nervous System": "Analgesics, antidepressants, antipsychotics, anticonvulsants",
    "Cardiovascular System": "Antihypertensives, anti‑anginals, anticoagulants",
    "Respiratory System": "Bronchodilators, corticosteroids, antitussives",
    "Nutrition and Blood": "Vitamins, minerals, blood products",
    "Appliances": "Nebulisers, infusion pumps, feeding tubes",
    "Gastro‑Intestinal System": "Antacids, laxatives, anti‑emetics",
    "Stoma Appliances": "Colostomy and ileostomy bags and accessories",
    "Skin": "Topical steroids, emollients, acne treatments",
    "Obstetrics, Gynaecology & Urinary‑Tract": "Contraceptives, tocolytics, diuretics",
    "Infections": "Antibiotics, antivirals, antifungals",
    "Malignant Disease & Immunosuppression": "Chemotherapy, immunosuppressants, targeted therapies",
    "Dressings": "Gauze, foam, hydrocolloid and other wound dressings",
    "Eye": "Topical antibiotics, glaucoma treatments, ocular lubricants",
    "Immunological Products & Vaccines": "Vaccines, immunoglobulins, allergy desensitisation agents",
    "Musculoskeletal & Joint Diseases": "NSAIDs, disease‑modifying antirheumatic drugs (DMARDs)",
    "Ear, Nose & Oropharynx": "Ear drops, nasal sprays, throat lozenges",
    "Incontinence Appliances": "Pads, sheaths, catheters",
    "Anaesthesia": "Induction agents, volatile anaesthetics, neuromuscular blockers",
    "Other Drugs & Preparations": "Rarely used or miscellaneous agents",
    "Preparations Used in Diagnosis": "Contrast media, diagnostic dyes, barium preparations"
}


if st.session_state.page == "BNF":
    st.markdown("<h1>Net Ingredient Cost by<br>British National Formulary Classification</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background-color: #e9f5ff;
        padding: 15px;
        border-radius: 5px;
        font-size: 20px;
        font-style: italic;
        color: #084298;
        margin-bottom: 20px;
    ">
    The <b>Net Ingredient Cost (NIC)</b> is measured in British Pounds Sterling (GBP), and reflects the amount that would be paid using the basic price of the prescribed drug or appliance and the quantity prescribed. For more information see the
    <a href="https://www.nhsbsa.nhs.uk/statistical-collections/prescription-cost-analysis-england" target="_blank" style="color:#084298; text-decoration: underline;">
    NHSBSA website</a>.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="
        background-color: #f0f0f0;
        padding: 15px;
        border-radius: 5px;
        font-size: 20px;
        font-style: italic;
        color: #333333;
        margin-bottom: 20px;
    ">
    The <b>British National Formulary (BNF)</b> provides healthcare professionals with up-to-date, evidence-based information on the selection, prescribing, dispensing, and administration of medicines. BNF data is organised by <b>chapter</b>, <b>section</b> and <b>paragraph</b> as can be seen below. For detailed guidance, visit the 
    <a href="https://bnf.nice.org.uk/" target="_blank" style="color:#333333; text-decoration: underline;">
    BNF website</a>.
    </div>
    """, unsafe_allow_html=True)



    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        show_chapter = st.button("🫀 Chapter", use_container_width=True)
    with col2:
        show_section = st.button("🩺 Section", use_container_width=True)
    with col3:
        show_paragraph = st.button("💊 Paragraph", use_container_width=True)

    st.write("---")

    def format_and_display_chapter(df, level_name):
        df = df.copy()
        
        # Format numeric columns
        df["% of Total NIC"] = df["percentage_of_total_nic"].round(2)
        df["NIC (£)"] = df[df.columns[1]].round().astype(int).apply(lambda x: f"{x:,}".replace(",", " "))

        # Rename columns
        bnf_col = f"BNF {level_name.capitalize()}"
        df = df.rename(columns={df.columns[0]: bnf_col})
        # Add an info icon with tooltip HTML to the BNF column
        df[bnf_col] = df[bnf_col].apply(lambda x: (
            f"{x}"
            f"<span class='info-tooltip' title='Including things like {section_descriptions.get(x, 'No description available')}'>ℹ️</span>"
        ))

        df = df[[bnf_col, "% of Total NIC", "NIC (£)"]]
        df = df.sort_values("% of Total NIC", ascending=False)

        # Create styled HTML table
        table_html = df.to_html(
            index=False,
            escape=False,
            justify="center",
            classes="nic-table"
        )

        # Inject custom CSS to style the table
        st.markdown("""
            <style>
            .nic-table {
                width: 70% !important;
                margin-left: auto;
                margin-right: auto;
                border-collapse: collapse;
            }
            .nic-table th, .nic-table td {
                padding: 8px 12px;
            }
            .nic-table th {
                text-align: center;
                background-color: #f0f2f6;
            }
            .nic-table td:nth-child(2), .nic-table td:nth-child(3) {
                text-align: center;
            }
            .info-tooltip {
                cursor: help;
                font-size: 0.9em;
                margin-left: 5px;
                color: #555;
            }
            .info-tooltip:hover {
                text-decoration: underline dotted;
            }
            </style>
        """, unsafe_allow_html=True)


        # Display styled table
        st.markdown(table_html, unsafe_allow_html=True)
    
    def format_and_display_interactive(df, level_name):
        df = df.copy()

        if "bnf_section" in df.columns:
            df = df.rename(columns={"bnf_section": "BNF Section"})
        if "bnf_chapter" in df.columns:
            df = df.rename(columns={"bnf_chapter": "BNF Chapter"})
        if "bnf_paragraph" in df.columns:
            df = df.rename(columns={"bnf_paragraph": "BNF Paragraph"})

        # Format numeric columns
        df["% of Total NIC"] = df["percentage_of_total_nic"].round(2)
        nic_by = 'nic_by_' + level_name
        df["NIC (£)"] = df[nic_by].round().astype(int).apply(lambda x: f"{x:,}".replace(",", " "))

        # Drop unwanted columns
        df = df.drop(columns=["nic_by_section", "percentage_of_total_nic"], errors='ignore')
        if level_name == 'paragraph':
            df = df.drop(columns=["nic_by_paragraph"], errors='ignore')

        # Convert to HTML with nic-table class, no index, centered justification
        table_html = df.to_html(
            index=False,
            escape=False,
            justify="center",
            classes="nic-table"
        )

        # Number of columns, to target last two
        n_cols = len(df.columns)

        # Inject custom CSS
        st.markdown(f"""
            <style>
            .nic-table {{
                width: 100% !important;
                margin-left: auto;
                margin-right: auto;
                border-collapse: collapse;
            }}
            .nic-table th, .nic-table td {{
                padding: 8px 12px;
            }}
            .nic-table th {{
                text-align: center;
                background-color: #f0f2f6;
                font-weight: bold;
            }}
            /* Center last two columns */
            .nic-table td:nth-child({n_cols - 1}), .nic-table td:nth-child({n_cols}) {{
                text-align: center;
            }}
            .nic-table th:nth-child({n_cols - 1}), .nic-table th:nth-child({n_cols}) {{
                text-align: center;
            }}
            </style>
        """, unsafe_allow_html=True)

        st.markdown(table_html, unsafe_allow_html=True)


# CHAPTER ----------------------------
    if show_chapter or not any([show_section, show_paragraph]):
        # 
        st.subheader("🫀 NIC Costs by BNF Chapter")
        st.markdown("""
        <h4 style="color: #777777; text-indent: 2em;">
            2024/2025 Financial Year
        </h4>
        """, unsafe_allow_html=True)

        st.write("")
        st.markdown("""
            <i><span style='font-size:18px'>
            A BNF Chapter is the broadest classification grouping related therapeutic areas or body systems.<br>
            For example, the <b>Endocrine System</b> is a chapter.
            </span></i>
            """, unsafe_allow_html=True)

        # --- PIE CHART ---
        chapter_data = (
            nic_by_bnf_chapter.sort_values("percentage_of_total_nic", ascending=False)
            [["bnf_chapter", "percentage_of_total_nic"]]
        )
        chapter_data["percentage_of_total_nic"] = chapter_data["percentage_of_total_nic"].round(2)
        data_pairs = list(chapter_data.itertuples(index=False, name=None))

        pie = (
            Pie()
            .add(
                "",
                data_pair=data_pairs,
                radius=["0%", "80%"]  # Full-size pie (no hole), bigger radius
            )
            .set_global_opts(
                # title_opts=opts.TitleOpts(title="NIC by BNF Chapter"),
                legend_opts=opts.LegendOpts(is_show=False),
                toolbox_opts=opts.ToolboxOpts(is_show=True),  # Optional
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(formatter="{b}: {c}%", font_size=14)  # Optional: bigger labels
            )
        )
        st_pyecharts(pie, height=1000)
        st.write("")
        format_and_display_chapter(nic_by_bnf_chapter, "chapter")

# SECTION ----------------------------
    elif show_section:
        # 
        st.subheader("🩺 NIC Costs by BNF Section")
        st.markdown("""
        <h4 style="color: #777777; text-indent: 2em;">
            2024/2025 Financial Year
        </h4>
        """, unsafe_allow_html=True)
        st.markdown("""
        <i><span style='font-size:18px'>
        A BNF section is a subdivision within a chapter that categorizes medicines by more specific clinical indications or drug classes.<br>
        For example, the <b>Endocrine System</b> chapter has a section called <b>Drugs Used in Diabetes</b>.
        </span></i>
        """, unsafe_allow_html=True)

        st.write("")
        format_and_display_interactive(nic_by_bnf_section, "section")

# PARAGRAPH ----------------------------
    elif show_paragraph:
        st.subheader("💊 NIC Costs by BNF Paragraph")
        st.markdown("""
        <h4 style="color: #777777; text-indent: 2em;">
            2024/2025 Financial Year
        </h4>
        """, unsafe_allow_html=True)
        st.markdown("""
        <i><span style='font-size:18px'>
        A BNF Paragraph is the most detailed level, specifying individual drugs or closely related groups within a section.<br>
        For example, <b>Antidiabetic Drugs</b> is a paragaph in the <b>Drugs Used in Diabetes</b> section of the <b>Endocrine System</b>chapter.
        </span></i>
        """, unsafe_allow_html=True)
        st.markdown("<i><span style='font-size:18px'></span></i>", unsafe_allow_html=True)
        st.write("")
        format_and_display_interactive(nic_by_bnf_paragraph, "paragraph")