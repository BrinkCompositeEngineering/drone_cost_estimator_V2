# {} is dict
# [] is list (simple array)

import sys
import os
import pandas as pd
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from components.component import Component
from engine.estimator_engine import EstimatorEngine
from config.config_loader import load_config
from reporting.report_generator import ReportGenerator
from reporting.pdf_report import PDFReport
import tempfile

# -----------------------------
# CONFIG & ENGINE
# -----------------------------

config_default = load_config("config/defaults.yaml")
tooling_config  = load_config("config/tooling_boards.yaml")

engine = EstimatorEngine(config_default, tooling_config)

st.set_page_config(layout="wide")
st.title("Composite Tooling Cost Estimator")



# -----------------------------
# HELPERS
# -----------------------------

# Helper for the parameter panel
def flatten_dict(d, parent_key=()):
    items = []
    for k, v in d.items():
        new_key = parent_key + (k,)
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key).items())
        else:
            items.append((new_key, v))
    return dict(items)


# -----------------------------
# PARAMETER PANEL (RIGHT SIDE)
# -----------------------------

def parameter_control_panel(config):

    st.header("⚙️ Parameters")

    search = st.text_input("Search parameter")

    for category, content in config.data.items():

        with st.expander(category.capitalize(), expanded=False):

            flat = flatten_dict(content)

            rows = []
            for key_tuple, value in flat.items():

                param_name = ".".join(key_tuple)

                if search and search.lower() not in param_name.lower():
                    continue

                rows.append({
                    "Parameter": param_name,
                    "Value": value
                })

            if not rows:
                continue

            df = pd.DataFrame(rows)

            edited = st.data_editor(
                df,
                use_container_width=True,
                num_rows="fixed",
                key=f"editor_{category}"
            )

            for _, row in edited.iterrows():
                keys = [category] + row["Parameter"].split(".")
                config.set(*keys, value=row["Value"])


def process_components_table():
    results = []

    for _, row in st.session_state.components_table.iterrows():
        comp = Component(
            row["Name"],
            row["Length (mm)"],
            row["Width (mm)"],
            row["Height (mm)"],
            row["Material"]
        )

        result = engine.process_component(comp)

        results.append({
            "Component": row["Name"],
            "Block volume": result.stacker_result.volume_m3,
            "Material Cost (€)": result.material_cost,
            "Milling Cost (€)": result.milling_cost,
            # "Postprocess Cost (€)": result["postprocess_cost"],
            "Total (€)": result.material_cost + result.milling_cost,
            # "Blocks used": result["blocks_used"]
        })

    st.session_state.results_df = pd.DataFrame(results)
    st.rerun()

# -----------------------------
# SESSION STATE
# -----------------------------

if "components_table" not in st.session_state:
    st.session_state.components_table = pd.DataFrame(
        columns=["Name", "Length (mm)", "Width (mm)", "Height (mm)", "Material"]
    )

if "results_df" not in st.session_state:
    st.session_state.results_df = pd.DataFrame()

# 🔥 KPI BAR (LIVE COST)
if not st.session_state.results_df.empty:
    total_cost = st.session_state.results_df["Total (€)"].sum()
    st.metric("Total Project Cost", f"€{total_cost:,.2f}")
else:
    st.metric("Total Project Cost", "€0.00")


# -----------------------------
# MAIN LAYOUT (75 / 25)
# -----------------------------

col_main, col_params = st.columns([3, 1])

# =============================
# LEFT SIDE (MAIN WORKFLOW)
# =============================

with col_main:




    # -----------------------------
    # TABS
    # -----------------------------
    tab1, tab2, tab3 = st.tabs(["📦 Geometry", "💰 Cost", "📊 Results"])



    # =============================
    # TAB 1 — GEOMETRY
    # =============================
    with tab1:

        st.subheader("Add Component")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            name = st.text_input("Component name")

        with col2:
            length = st.number_input("Length (mm)", value=2200)

        with col3:
            width = st.number_input("Width (mm)", value=350)

        with col4:
            height = st.number_input("Height (mm)", value=80)

        with col5:
            materials = config_default.get("tooling_blocks", "materials")
            material_names = [m["name"] for m in materials]
            material_choice = st.selectbox("Tooling Material", material_names)

        if st.button("Add Component"):
            new_row = pd.DataFrame(
                [[name, length, width, height, material_choice]],
                columns=["Name", "Length (mm)", "Width (mm)", "Height (mm)", "Material"]
            )

            st.session_state.components_table = pd.concat(
                [st.session_state.components_table, new_row],
                ignore_index=True
            )

            process_components_table()


        st.subheader("Project Components")

        edited_table = st.data_editor(
            st.session_state.components_table,
            num_rows="dynamic",
            use_container_width=True
        )

        st.session_state.components_table = edited_table
        if st.button("update table"):
            st.rerun()


    # =============================
    # TAB 2 — COST
    # =============================
    with tab2:

        st.subheader("Run Cost Calculation")

        if st.button("Calculate Project Cost"):

            process_components_table()

        if not st.session_state.results_df.empty:
            st.dataframe(st.session_state.results_df, use_container_width=True)


    # =============================
    # TAB 3 — RESULTS
    # =============================
    with tab3:

        st.subheader("📊 Project Report")

        # -----------------------------
        # ACTION BUTTONS
        # -----------------------------
        col1, col2 = st.columns([1, 1])

        with col1:
            generate_report = st.button("⚙️ Generate Report")

        # -----------------------------
        # GENERATE REPORT
        # -----------------------------
        if generate_report:

            components = []

            for _, row in st.session_state.components_table.iterrows():
                comp = Component(
                    row["Name"],
                    row["Length (mm)"],
                    row["Width (mm)"],
                    row["Height (mm)"],
                    row["Material"]
                )

                comp = engine.process_component(comp)
                components.append(comp)

            report = ReportGenerator(components)

            st.session_state.report_summary = report.generate_summary()
            st.session_state.results_df = pd.DataFrame(
                report.generate_component_table()
            )

            # Reset PDF when new report is generated
            st.session_state.pdf_bytes = None

        # -----------------------------
        # KPI SECTION
        # -----------------------------
        if "report_summary" in st.session_state:
            summary = st.session_state.report_summary

            col1, col2, col3 = st.columns(3)

            col1.metric("💰 Total Cost", f"€{summary['total_cost']:,.2f}")
            col2.metric("📦 Volume", f"{summary['total_volume']:.3f} m³")
            col3.metric("🧱 Boards", summary["total_boards"])

        # -----------------------------
        # PDF GENERATION
        # -----------------------------
        pdf_ready = st.session_state.get("pdf_bytes") is not None

        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("📄 Generate PDF", disabled="report_summary" not in st.session_state):
                import io

                buffer = io.BytesIO()

                pdf = PDFReport(buffer)
                pdf.generate(
                    st.session_state.report_summary,
                    st.session_state.results_df
                )

                st.session_state.pdf_bytes = buffer.getvalue()

        with col2:
            if st.session_state.get("pdf_bytes"):

                st.download_button(
                    label="⬇️ Download PDF",
                    data=st.session_state.pdf_bytes,
                    file_name="tooling_report.pdf",
                    mime="application/pdf"
                )
            else:
                st.button("⬇️ Download PDF", disabled=True)

        # -----------------------------
        # RESULTS TABLE
        # -----------------------------
        if not st.session_state.results_df.empty:

            st.divider()
            st.subheader("📋 Component Breakdown")

            st.dataframe(
                st.session_state.results_df,
                use_container_width=True
            )

            total_project_cost = st.session_state.results_df["Total (€)"].sum()

            st.markdown(f"### 💰 Total Project Cost: €{total_project_cost:,.2f}")

            st.subheader("♻️ Remaining Stock")
            # st.write(engine.block_optimizer.leftover_lengths)

        else:
            st.info("Generate a report to see results.")


    # -----------------------------
    # RESET
    # -----------------------------
    st.divider()

    if st.button("Start New Project"):
        st.session_state.components_table = pd.DataFrame(
            columns=["Name", "Length (mm)", "Width (mm)", "Height (mm)", "Material"]
        )
        st.session_state.results_df = pd.DataFrame()
        st.rerun()


# =============================
# RIGHT SIDE (CONTROL PANEL)
# =============================

with col_params:
    parameter_control_panel(config_default)
