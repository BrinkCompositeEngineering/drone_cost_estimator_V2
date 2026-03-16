import sys
import os
import pandas as pd
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from components.component import Component
from engine.estimator_engine import EstimatorEngine
from config.config_loader import load_config

config = load_config()
engine = EstimatorEngine(config)

st.title("Composite Tooling Cost Estimator")

# -----------------------------
# Parameter control panel for the configs
# -----------------------------

def parameter_control_panel(config):

    st.header("Estimator Parameters")

    rows = []

    for category, params in config.data.items():

        for param, value in params.items():

            rows.append({
                "Category": category,
                "Parameter": param,
                "Value": value
            })

    df = pd.DataFrame(rows)

    edited = st.data_editor(
        df,
        use_container_width=True,
        num_rows="fixed"
    )

    # Write changes back to config

    for _, row in edited.iterrows():

        config.set(
            row["Category"],
            row["Parameter"],
            row["Value"]
        )

    return config

# -----------------------------
# Session State
# -----------------------------

if "components_table" not in st.session_state:

    st.session_state.components_table = pd.DataFrame(
        columns=[
            "Name",
            "Length (mm)",
            "Width (mm)",
            "Height (mm)",
            "Material"
        ]
    )

# -----------------------------
# Component Input
# -----------------------------

st.header("Add Component")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    name = st.text_input("Component name")

with col2:
    length = st.number_input("Length (mm)", value=1000)

with col3:
    width = st.number_input("Width (mm)", value=200)

with col4:
    height = st.number_input("Height (mm)", value=50)

with col5:

    material_names = config.get("block_cost", "available_materials")

    material_choice = st.selectbox(
        "Tooling Material",
        material_names
    )

# Add component

if st.button("Add Component"):

    new_row = pd.DataFrame(
        [[name, length, width, height, material_choice]],
        columns=[
            "Name",
            "Length (mm)",
            "Width (mm)",
            "Height (mm)",
            "Material"
        ]
    )

    st.session_state.components_table = pd.concat(
        [st.session_state.components_table, new_row],
        ignore_index=True
    )

# -----------------------------
# Component Table
# -----------------------------

st.header("Project Components")

edited_table = st.data_editor(
    st.session_state.components_table,
    num_rows="dynamic",
    use_container_width=True
)

st.session_state.components_table = edited_table

# -----------------------------
# Calculate
# -----------------------------

if st.button("Calculate Project Cost"):

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
            "Material Cost (€)": result["material_cost"],
            "Milling Cost (€)": result["milling_cost"],
            "Postprocess Cost (€)": result["postprocess_cost"],
            "Total (€)": result["total_cost"],
            "Block stack": str(result["block_stack"]),
            "Blocks used": result["blocks_used"]

        })

    results_df = pd.DataFrame(results)

    st.header("Cost Results")

    st.dataframe(results_df, use_container_width=True)

    total_project_cost = results_df["Total (€)"].sum()

    st.subheader(f"Total Project Cost: €{total_project_cost:,.2f}")

    st.subheader("Remaining Stock Pieces")

    st.write(engine.block_optimizer.leftover_lengths)

# -----------------------------
# Reset
# -----------------------------

st.divider()

if st.button("Start New Project"):

    st.session_state.components_table = pd.DataFrame(
        columns=[
            "Name",
            "Length (mm)",
            "Width (mm)",
            "Height (mm)",
            "Material"
        ]
    )

    st.rerun()


config = parameter_control_panel(config)